"""
Oppenheimer Skill Portal (Team Oppenheimer)
Unified Digital Student Portfolio & Verified Profile Page
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

# Apply global dark futuristic theme
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
    .profile-card {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glow);
        color: var(--text-primary);
        padding: 1.8rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(56, 189, 248, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .profile-card:hover {
        border-color: var(--border-glow-hover);
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.2);
    }
    .profile-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        color: var(--text-primary);
    }
    .profile-role {
        font-size: 1.1rem;
        color: var(--accent-cyan);
        font-weight: 600;
        margin-top: 0.2rem;
        margin-bottom: 0.8rem;
    }
    .verified-badge {
        display: inline-block;
        background-color: rgba(5, 150, 105, 0.25);
        border: 1px solid #10b981;
        color: #34d399;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .score-badge-green { background-color: rgba(16, 185, 129, 0.25); border: 1px solid #10b981; color: #34d399; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .score-badge-amber { background-color: rgba(245, 158, 11, 0.25); border: 1px solid #f59e0b; color: #fbbf24; padding: 4px 12px; border-radius: 12px; font-weight: bold; }
    .score-badge-red { background-color: rgba(239, 68, 68, 0.25); border: 1px solid #ef4444; color: #f87171; padding: 4px 12px; border-radius: 12px; font-weight: bold; }

    .portfolio-section-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        height: 100%;
        color: var(--text-primary);
        transition: all 0.25s ease !important;
    }
    .portfolio-section-card:hover {
        border-color: var(--border-glow-hover);
        transform: translateY(-2px);
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
                <h2 style="color:var(--accent-cyan); margin-bottom:0.5rem;">⚠️ No Student Portfolios Found</h2>
                <p style="color:var(--text-secondary); font-size:1.05rem; max-width:600px; margin:0 auto 1.5rem auto;">
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
# 3. Executive Profile Header Layout
# -----------------------------------------------------------------------------
col_prof_left, col_prof_right = st.columns([1.6, 1])

with col_prof_left:
    st.markdown(
        f"""
        <div class="profile-card">
            <span class="verified-badge">✓ Verified Student Profile</span>
            <span style="font-size:0.8rem; color:var(--text-muted);">ID: #{student_id}</span>
            <h1 class="profile-name">{student_name}</h1>
            <div class="profile-role">🎯 Target Track: {target_role}</div>
            <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0;">
                📅 Assessment Verified: {created_at} | 🏛️ Oppenheimer Skill Portal
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_prof_right:
    st.markdown("### 📊 Alignment Summary")
    
    if match_score >= 75.0:
        badge_html = f'<span class="score-badge-green">🟢 {match_score}% Industry Aligned</span>'
    elif match_score >= 50.0:
        badge_html = f'<span class="score-badge-amber">🟠 {match_score}% Moderate Alignment</span>'
    else:
        badge_html = f'<span class="score-badge-red">🔴 {match_score}% Actionable Gap</span>'

    st.markdown(badge_html, unsafe_allow_html=True)
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
    st.subheader("✅ Verified Core Competencies")
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
                        <span class="verified-badge">✓ Verified</span>
                        <span style="font-size:0.75rem; color:var(--text-muted); font-weight:bold;">{item['category']}</span>
                        <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; font-size:1.1rem; color:var(--text-primary);">{item['name']}</h4>
                        <div style="color:#f59e0b; font-size:1.1rem;">{stars_str} <span style="color:var(--text-secondary); font-size:0.9rem;">({item['rating']}/5)</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)

# --- TAB 3: SKILLS IN PROGRESS & PATHWAYS ---
with tab_progress:
    st.subheader("🚀 Active Learning Pathways & Gap Recommendations")
    st.caption("Targeted learning resources mapped directly to your largest role deficits.")
    
    if not top_gaps:
        st.success("🎉 No active skill gaps! You fully meet all requirements for this role.")
    else:
        gap_recs = rec_data
        for idx, gap in enumerate(top_gaps, 1):
            sid = gap["skill_id"]
            res_list = gap_recs.get(sid, [])
            cat = skill_cat_map.get(sid, "DOMAIN")

            st.markdown(
                f"##### #{idx}. {gap['skill_name']} <span style='font-size:0.8rem; color:#d97706;'>[{cat}]</span>",
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

# --- TAB 4: CERTIFICATIONS & ACHIEVEMENTS (STATIC DEMO PLACEHOLDER) ---
with tab_certs:
    st.subheader("📜 Industry Certifications & Academic Badges")
    st.caption("Verified credentials issued by academic institutions and industry partner organizations.")
    
    cert_col1, cert_col2 = st.columns(2)
    with cert_col1:
        with st.container(border=True):
            st.markdown("🎖️ **Python for Data Science & AI Certification**")
            st.caption("Issuer: NPTEL / IIT Madras | Issued: January 2026 | ID: NPTEL-PY-8849")
            st.success("✓ Verified Credential")
    with cert_col2:
        with st.container(border=True):
            st.markdown("🏅 **Health Analytics Industry Partner Badge**")
            st.caption("Issuer: Industry Portal | Issued: February 2026 | ID: IND-HP-2026")
            st.success("✓ Verified Credential")

    with st.container(border=True):
        st.markdown("📂 **Upload Additional Certificate (Demo Placeholder)**")
        st.file_uploader("Upload Certificate PDF/Image", type=["pdf", "png", "jpg"], key="cert_uploader")

# --- TAB 5: FEATURED PROJECTS (STATIC DEMO PLACEHOLDER) ---
with tab_projects:
    st.subheader("💻 Featured Projects & Capstone Work")
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
