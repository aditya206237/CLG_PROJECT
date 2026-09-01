"""
Oppenheimer Skill Portal (Team Oppenheimer)
Unified Digital Student Portfolio & Verified Profile Page
(Editorial Data Analytics Design System)
"""

import streamlit as st
import pandas as pd
import time
from typing import Dict, List, Any

from load_taxonomy import get_role_requirements, get_all_skills
from database import get_all_students, get_student_skill_vector, get_student_responses_full, init_db
from gap_analysis import build_vectors, compute_match_score, compute_skill_gaps, get_top_gaps
from recommend import get_recommendations_for_gaps
from charts import create_radar_chart
from pdf_export import generate_portfolio_pdf
from login_ui import render_login_page, render_logout_button
from theme import apply_theme

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Portfolio - Oppenheimer Skill Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global editorial theme
apply_theme()

# Authentication Gate
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    render_login_page()
    st.stop()

render_logout_button()

init_db()


# Custom CSS for executive portfolio styling
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    .profile-card-dark {
        background-color: var(--bg-dark-panel);
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
        border: 1px solid var(--border-dark-panel);
        color: var(--text-cream);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .profile-name {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.015em;
        color: var(--text-cream) !important;
    }
    .profile-role {
        font-size: 1.1rem;
        color: var(--accent-mint);
        font-weight: 600;
        margin-top: 0.2rem;
        margin-bottom: 0.8rem;
        font-family: 'Inter', sans-serif;
    }
    .verified-badge-gold {
        display: inline-block;
        background-color: rgba(201, 162, 39, 0.12);
        border: 1px solid var(--accent-gold);
        color: var(--accent-gold);
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .portfolio-section-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        height: 100%;
        color: var(--text-dark);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. Student Profile Data Loading & Intentional Empty State
# -----------------------------------------------------------------------------
all_students = get_all_students()

if not all_students:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align:center; padding:2rem;">
                <h2 style="color:var(--text-dark); margin-bottom:0.5rem;">⚠️ No Student Portfolios Found</h2>
                <p style="color:var(--text-muted); font-size:1.05rem; max-width:600px; margin:0 auto 1.5rem auto;">
                    There are currently no student records in the SQLite database (<code>portal.db</code>).
                    Please complete a skill assessment questionnaire to generate your verified digital portfolio.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.page_link("app.py", label="🚀 Launch Assessment Questionnaire", icon="📝", use_container_width=True)
    st.stop()

# Sidebar Selector
with st.sidebar:
    st.header("👤 Student Portfolio Selector")
    
    default_index = 0
    if "student_id" in st.session_state and st.session_state.student_id:
        for idx, s in enumerate(all_students):
            if s["student_id"] == st.session_state.student_id:
                default_index = idx
                break

    student_options = {
        f"#{s['student_id']} - {s['name']} ({s['target_role']})": s
        for s in all_students
    }

    selected_label = st.selectbox(
        "Select Active Portfolio:",
        options=list(student_options.keys()),
        index=default_index
    )

    selected_student = student_options[selected_label]
    student_id = selected_student["student_id"]
    student_name = selected_student["name"]
    target_role = selected_student["target_role"]
    created_at = selected_student.get("created_at", "N/A")

# Loading State Spinner
with st.spinner("🎓 Assembling student digital portfolio & verified credentials..."):
    # Load data & compute vectors
    student_vector = get_student_skill_vector(student_id)
    responses_full = get_student_responses_full(student_id)
    role_reqs = get_role_requirements(target_role)
    all_skills = get_all_skills()
    all_skills_map = {s["id"]: s["name"] for s in all_skills}
    skill_cat_map = {s["id"]: s["category"].upper() for s in all_skills}

    s_vec, r_vec = build_vectors(student_vector, target_role)
    match_score = compute_match_score(s_vec, r_vec)
    all_gaps = compute_skill_gaps(student_vector, target_role)
    top_gaps = get_top_gaps(student_vector, target_role, n=5)

    # Build verified skills list
    verified_skills_list = []
    for resp in responses_full:
        sid = resp["skill_id"]
        self_val = resp["self_rating"]
        adj_val = resp["quiz_adjusted_rating"]
        if adj_val >= self_val or adj_val >= 3:
            verified_skills_list.append({
                "skill_id": sid,
                "name": all_skills_map.get(sid, sid),
                "category": skill_cat_map.get(sid, "TECHNICAL"),
                "rating": adj_val
            })

# -----------------------------------------------------------------------------
# 3. Executive Profile Dark Panel Header Layout
# -----------------------------------------------------------------------------
col_prof_left, col_prof_right = st.columns([1.6, 1])

with col_prof_left:
    st.markdown(
        f"""
        <div class="hero-container" style="padding:1.6rem 1.8rem !important; margin-bottom:0 !important;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span class="verified-badge-gold">✓ VERIFIED STUDENT PROFILE</span>
                <span style="font-family:'JetBrains Mono', monospace; font-size:11px; color:var(--text-muted);">ID: #{student_id}</span>
            </div>
            <h1 class="profile-name" style="margin-top:0.4rem; color:var(--text-dark) !important;">{student_name}</h1>
            <div class="profile-role" style="color:var(--accent-primary); font-weight:600; font-size:1.05rem;">🎯 Target Track: {target_role}</div>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0; font-family:'Inter', sans-serif;">
                📅 Assessment Verified: {created_at} | 🏛️ Oppenheimer Skill Portal
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_prof_right:
    st.markdown("### 📊 Alignment <em class='italic-emphasis'>Summary</em>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class="metric-card-dark" style="text-align:center; padding:1rem !important;">
            <div class="dark-panel-label"><span class="live-dot"></span>ROLE ALIGNMENT</div>
            <div class="dark-panel-number" style="margin-top:0.2rem; font-size:2.2rem;">{match_score}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.metric("Verified Skills", f"{len(verified_skills_list)}")
    with col_sub2:
        st.metric("Actionable Deficits", f"{len(top_gaps)}")

# -----------------------------------------------------------------------------
# 4. Download Digital Portfolio (PDF Export)
# -----------------------------------------------------------------------------
student_info = {
    "student_id": student_id,
    "name": student_name,
    "target_role": target_role,
    "created_at": created_at
}
rec_data = get_recommendations_for_gaps(top_gaps, n_per_skill=2)
pdf_bytes = generate_portfolio_pdf(
    student_info=student_info,
    match_score=match_score,
    verified_skills=verified_skills_list,
    top_gaps=top_gaps,
    recommendations=rec_data
)
safe_student_name = student_name.lower().replace(" ", "_")

st.download_button(
    label="📥 Download Digital Portfolio (PDF Summary)",
    data=pdf_bytes,
    file_name=f"{safe_student_name}_portfolio.pdf",
    mime="application/pdf",
    type="secondary",
    use_container_width=False
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Multi-Tab Portfolio Content
# -----------------------------------------------------------------------------
tab_radar, tab_verified, tab_progress, tab_certs, tab_projects = st.tabs([
    "🕸️ Skill Radar Vector",
    f"✅ Verified Skills ({len(verified_skills_list)})",
    f"🚀 Skills in Progress ({len(top_gaps)})",
    "📜 Certifications & Badges",
    "💻 Featured Projects"
])

# --- TAB 1: RADAR CHART ---
with tab_radar:
    st.subheader(f"Multi-Dimensional Skill Profile [{target_role}]")
    fig = create_radar_chart(student_vector, role_reqs, target_role, student_name)
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: VERIFIED SKILLS ---
with tab_verified:
    st.markdown("### ✅ Verified Core <em class='italic-emphasis'>Competencies</em>", unsafe_allow_html=True)
    st.caption("Skills verified via self-assessment and objective micro-quiz conceptual checks.")
    
    if not verified_skills_list:
        st.info("No verified skills recorded yet.")
    else:
        v_cols = st.columns(2)
        for idx, item in enumerate(verified_skills_list):
            col_target = v_cols[idx % 2]
            stars_str = "★" * item['rating'] + "☆" * (5 - item['rating'])
            with col_target:
                st.markdown(
                    f"""
                    <div class="portfolio-section-card">
                        <span class="verified-badge-gold">✓ VERIFIED</span>
                        <span style="font-family:'JetBrains Mono', monospace; font-size:10px; color:var(--text-muted); text-transform:uppercase; margin-left:6px;">{item['category']}</span>
                        <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; font-size:1.1rem; color:var(--text-dark); font-family:'Playfair Display', serif;">{item['name']}</h4>
                        <div style="color:var(--accent-gold); font-size:1.1rem;">{stars_str} <span style="color:var(--text-muted); font-size:0.85rem; font-family:'JetBrains Mono', monospace;">({item['rating']}/5)</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)

# --- TAB 3: SKILLS IN PROGRESS & PATHWAYS ---
with tab_progress:
    st.markdown("### 🚀 Active Learning <em class='italic-emphasis'>Pathways</em> & Gap Recommendations", unsafe_allow_html=True)
    st.caption("Targeted learning resources mapped directly to your largest role deficits.")
    
    if not top_gaps:
        st.success("🎉 No active skill gaps! You fully meet all requirements for this role.")
    else:
        gap_recs = rec_data
        for idx, gap in enumerate(top_gaps, 1):
            sid = gap["skill_id"]
            res_list = gap_recs.get(sid, [])
            cat = skill_cat_map.get(sid, "DOMAIN")
            gap_val = gap["gap"]
            is_high_demand = (gap_val >= 3)
            
            badge_html = f'<span class="demand-badge-gold">HIGH DEMAND GAP</span>' if is_high_demand else f'<span class="demand-badge-neutral">STANDARD GAP</span>'

            st.markdown(
                f"##### #{idx}. {gap['skill_name']} {badge_html}",
                unsafe_allow_html=True
            )
            st.caption(f"Current Rating: **{gap['student_level']}/5** | Target Level: **{gap['required_level']}/5** | Deficit: **-{gap['gap']} levels**")

            if res_list:
                r_cols = st.columns(len(res_list))
                for r_col, res in zip(r_cols, res_list):
                    with r_col:
                        with st.container(border=True):
                            st.markdown(f"**[{res['type'].upper()}] {res['title']}**")
                            st.caption(f"🏛️ Provider: {res['provider']} | ⏱️ {res['duration']}")
                            st.link_button("🚀 View Program", url=res.get("url", "#"), use_container_width=True)
            st.divider()

# --- TAB 4: CERTIFICATIONS & ACHIEVEMENTS ---
with tab_certs:
    st.markdown("### 📜 Industry Certifications & <em class='italic-emphasis'>Academic Badges</em>", unsafe_allow_html=True)
    st.caption("Verified credentials issued by academic institutions and industry partner organizations.")
    
    cert_col1, cert_col2 = st.columns(2)
    with cert_col1:
        with st.container(border=True):
            st.markdown("<span class='verified-badge-gold'>✓ VERIFIED</span>", unsafe_allow_html=True)
            st.markdown("🎖️ **Python for Data Science & AI Certification**")
            st.caption("Issuer: NPTEL / IIT Madras | Issued: January 2026 | ID: NPTEL-PY-8849")
    with cert_col2:
        with st.container(border=True):
            st.markdown("<span class='verified-badge-gold'>✓ VERIFIED</span>", unsafe_allow_html=True)
            st.markdown("🏅 **Health Analytics Industry Partner Badge**")
            st.caption("Issuer: Industry Portal | Issued: February 2026 | ID: IND-HP-2026")

    with st.container(border=True):
        st.markdown("📂 **Upload Additional Certificate (Demo Placeholder)**")
        st.file_uploader("Upload Certificate PDF/Image", type=["pdf", "png", "jpg"], key="cert_uploader")

# --- TAB 5: FEATURED PROJECTS ---
with tab_projects:
    st.markdown("### 💻 Featured Projects & <em class='italic-emphasis'>Capstone Work</em>", unsafe_allow_html=True)
    st.caption("Applied projects demonstrating technical and domain skills in real-world scenarios.")

    proj_col1, proj_col2 = st.columns(2)
    with proj_col1:
        with st.container(border=True):
            st.markdown("🚀 **Clinical Knowledge Graph Platform**")
            st.write("Built an end-to-end Python pipeline to extract, structure, and visualize clinical research datasets.")
            st.caption("Technologies: Python, SQL, Graph DB, Streamlit")
    with proj_col2:
        with st.container(border=True):
            st.markdown("📊 **Student Skill Gap & Alignment Predictor**")
            st.write("Developed a vector math engine powered by Cosine Similarity to evaluate candidate readiness for industry roles.")
            st.caption("Technologies: Streamlit, NumPy, Scikit-Learn, Plotly, SQLite")
