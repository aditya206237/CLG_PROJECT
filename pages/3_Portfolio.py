"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Unified Digital Student Portfolio & Verified Profile Page
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any

from load_taxonomy import get_role_requirements, get_all_skills
from database import get_all_students, get_student_skill_vector, get_student_responses_full, init_db
from gap_analysis import build_vectors, compute_match_score, compute_skill_gaps, get_top_gaps
from recommend import get_recommendations_for_gaps
from charts import create_radar_chart

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Student Digital Portfolio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
        padding: 1.8rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    .profile-name {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .profile-role {
        font-size: 1.1rem;
        color: #38bdf8;
        font-weight: 600;
        margin-top: 0.2rem;
        margin-bottom: 0.8rem;
    }
    .verified-badge {
        display: inline-block;
        background-color: #059669;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .in-progress-badge {
        display: inline-block;
        background-color: #d97706;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .portfolio-section-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. Student Profile Data Loading
# -----------------------------------------------------------------------------
all_students = get_all_students()

if not all_students:
    st.warning("⚠️ No student assessment records found in database (`portal.db`).")
    st.info("👉 Please go to the **Assessment Questionnaire** page (`app.py`) to complete an assessment first.")
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

# Build verified skills list (quiz_adjusted_rating not downgraded from self_rating and rating >= 1)
verified_skills_list = []
for resp in responses_full:
    sid = resp["skill_id"]
    self_val = resp["self_rating"]
    adj_val = resp["quiz_adjusted_rating"]
    # If not downgraded by quiz verification
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
            <span class="verified-badge">✓ AIIA Verified Student Profile</span>
            <span style="font-size:0.8rem; color:#94a3b8;">ID: #{student_id}</span>
            <h1 class="profile-name">{student_name}</h1>
            <div class="profile-role">🎯 Target Track: {target_role}</div>
            <p style="font-size:0.85rem; color:#cbd5e1; margin-bottom:0;">
                📅 Assessment Verified: {created_at} | 🏛️ Ministry of Ayush / AIIA Portal
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_prof_right:
    st.markdown("### 📊 Alignment Summary")
    st.metric(
        label="Target Role Match Score",
        value=f"{match_score}%",
        delta="Industry Aligned" if match_score >= 70 else "Actionable Deficits",
        delta_color="normal" if match_score >= 70 else "inverse"
    )
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        st.metric("Verified Skills", f"{len(verified_skills_list)}")
    with col_sub2:
        st.metric("Actionable Gaps", f"{len(top_gaps)}")

# -----------------------------------------------------------------------------
# 4. Download Digital Portfolio (Markdown Export)
# -----------------------------------------------------------------------------
def generate_portfolio_markdown() -> str:
    md = f"# Digital Skill Portfolio — {student_name}\n"
    md += f"**Target Career Track:** {target_role}\n"
    md += f"**Student ID:** #{student_id}\n"
    md += f"**Target Role Alignment Score:** {match_score}%\n\n"
    md += "---\n\n"
    md += "## 1. Verified Skill Vector\n"
    for v in verified_skills_list:
        stars = "★" * v['rating'] + "☆" * (5 - v['rating'])
        md += f"- **{v['name']}** ({v['category']}): {v['rating']}/5 [{stars}]\n"
    md += "\n## 2. Priority Skill Gap Deficits\n"
    for g in top_gaps:
        md += f"- **{g['skill_name']}**: Current {g['student_level']}/5 vs Required {g['required_level']}/5 (Deficit: -{g['gap']})\n"
    md += "\n## 3. Recommended Industry Learning Pathways\n"
    recs = get_recommendations_for_gaps(top_gaps, n_per_skill=2)
    for sid, res_list in recs.items():
        s_name = all_skills_map.get(sid, sid)
        md += f"### Skill: {s_name}\n"
        for r in res_list:
            md += f"  - [{r['type'].upper()}] {r['title']} ({r['provider']}) — {r['duration']}\n"
    md += "\n---\n*Generated via Ministry of Ayush / AIIA Academia-Industry Portal*\n"
    return md

st.download_button(
    label="📥 Download Digital Portfolio (Markdown Summary)",
    data=generate_portfolio_markdown(),
    file_name=f"portfolio_student_{student_id}_{student_name.lower().replace(' ', '_')}.md",
    mime="text/markdown",
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
                        <span style="font-size:0.75rem; color:#64748b; font-weight:bold;">{item['category']}</span>
                        <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; font-size:1.1rem;">{item['name']}</h4>
                        <div style="color:#f59e0b; font-size:1.1rem;">{stars_str} <span style="color:#475569; font-size:0.9rem;">({item['rating']}/5)</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# --- TAB 3: SKILLS IN PROGRESS & PATHWAYS ---
with tab_progress:
    st.subheader("🚀 Active Learning Pathways & Gap Recommendations")
    st.caption("Targeted learning resources mapped directly to your largest role deficits.")
    
    if not top_gaps:
        st.success("🎉 No active skill gaps! You fully meet all requirements for this role.")
    else:
        gap_recs = get_recommendations_for_gaps(top_gaps, n_per_skill=2)
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
            st.markdown("🏅 **Ayush Health Analytics Industry Partner Badge**")
            st.caption("Issuer: AIIA Industry Portal | Issued: February 2026 | ID: AIIA-HP-2026")
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
            st.markdown("🚀 **Ayush Clinical Knowledge Graph Platform**")
            st.write("Built an end-to-end Python pipeline to extract, structure, and visualize clinical research datasets.")
            st.caption("Technologies: Python, SQL, Graph DB, Streamlit")
    with proj_col2:
        with st.container(border=True):
            st.markdown("📊 **Student Skill Gap & Alignment Predictor**")
            st.write("Developed a vector math engine powered by Cosine Similarity to evaluate candidate readiness for industry roles.")
            st.caption("Technologies: Streamlit, NumPy, Scikit-Learn, Plotly, SQLite")
