"""
Oppenheimer Skill Portal (Team Oppenheimer)
Skill Gap Analysis Dashboard & Plotly Radar Visualization
"""

import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
from typing import Dict, List, Any

from load_taxonomy import get_role_requirements, get_all_skills
from database import get_all_students, get_student_skill_vector, init_db
from gap_analysis import build_vectors, compute_match_score, compute_skill_gaps, get_top_gaps
from recommend import get_recommendations_for_gaps
from charts import create_radar_chart
from login_ui import render_login_page, render_logout_button
from theme import apply_theme


# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Results - Oppenheimer Skill Portal",
    page_icon="📊",
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

# Ensure DB tables exist
init_db()


# Custom CSS for polished UI & dynamic match score widget
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    .hero-container {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glow);
        color: var(--text-primary);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(56, 189, 248, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hero-container:hover {
        border-color: var(--border-glow-hover);
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.2);
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        color: var(--text-primary);
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: var(--text-muted);
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
    }
    .badge-tag {
        display: inline-block;
        background: linear-gradient(135deg, #0284c7 0%, #7e22ce 100%);
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Dynamic Match Score Cards */
    .score-card-green {
        background: rgba(16, 185, 129, 0.12);
        border: 2px solid var(--success);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.15);
    }
    .score-card-amber {
        background: rgba(245, 158, 11, 0.12);
        border: 2px solid var(--warning);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.15);
    }
    .score-card-red {
        background: rgba(239, 68, 68, 0.12);
        border: 2px solid var(--error);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.15);
    }
    .score-val-green { font-family: 'Space Grotesk', sans-serif; font-size: 2.4rem; font-weight: 900; color: var(--success); }
    .score-val-amber { font-family: 'Space Grotesk', sans-serif; font-size: 2.4rem; font-weight: 900; color: var(--warning); }
    .score-val-red { font-family: 'Space Grotesk', sans-serif; font-size: 2.4rem; font-weight: 900; color: var(--error); }

    .score-label { font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }

    .metric-card-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        padding: 1rem 1.2rem;
        border-radius: 10px;
        height: 100%;
        color: var(--text-primary);
    }
    .severity-high { background-color: rgba(239, 68, 68, 0.25); color: #f87171; padding: 2px 8px; border-radius: 6px; font-weight: bold; }
    .severity-mod { background-color: rgba(245, 158, 11, 0.25); color: #fbbf24; padding: 2px 8px; border-radius: 6px; font-weight: bold; }
    .severity-low { background-color: rgba(56, 189, 248, 0.25); color: #38bdf8; padding: 2px 8px; border-radius: 6px; font-weight: bold; }
    .severity-met { background-color: rgba(16, 185, 129, 0.25); color: #34d399; padding: 2px 8px; border-radius: 6px; font-weight: bold; }

    .type-pill {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. Hero Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-tag">Oppenheimer Vector Engine</span>
        <h1 class="hero-title">Skill Gap Analysis & Alignment Dashboard</h1>
        <p class="hero-subtitle">Interactive Plotly multi-dimensional radar comparison and targeted skill deficit analysis.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Student Selection & Intentional Empty State Handling
# -----------------------------------------------------------------------------
all_students = get_all_students()

if not all_students:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align:center; padding:2rem;">
                <h2 style="color:var(--accent-cyan); margin-bottom:0.5rem;">⚠️ No Student Assessments Found</h2>
                <p style="color:var(--text-secondary); font-size:1.05rem; max-width:600px; margin:0 auto 1.5rem auto;">
                    There are currently no student assessment records stored in the SQLite database (<code>portal.db</code>).
                    Please complete a skill assessment first to generate multi-dimensional gap analysis reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.page_link("app.py", label="🚀 Launch Assessment Questionnaire", icon="📝", use_container_width=True)
    st.stop()

# Sidebar Student Selector
with st.sidebar:
    st.header("👤 Student Selection")
    
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
        "Choose Student Profile:",
        options=list(student_options.keys()),
        index=default_index
    )

    selected_student = student_options[selected_label]
    student_id = selected_student["student_id"]
    student_name = selected_student["name"]
    target_role = selected_student["target_role"]

# Loading State Spinner
with st.spinner("📊 Analyzing multi-dimensional skill vectors & generating gap recommendations..."):
    # Fetch data for selected student
    student_vector = get_student_skill_vector(student_id)
    role_reqs = get_role_requirements(target_role)
    all_skills_list = get_all_skills()
    all_skills_map = {s["id"]: s["name"] for s in all_skills_list}
    skill_cat_map = {s["id"]: s["category"].upper() for s in all_skills_list}

    # Compute vectors and match score
    s_vec, r_vec = build_vectors(student_vector, target_role)
    match_score = compute_match_score(s_vec, r_vec)
    all_gaps = compute_skill_gaps(student_vector, target_role)
    top_gaps = get_top_gaps(student_vector, target_role, n=5)
    actionable_gaps_count = len([g for g in all_gaps if g["gap"] > 0])

# -----------------------------------------------------------------------------
# 4. Large Color-Coded Match Score Widget & Summary
# -----------------------------------------------------------------------------
col_m1, col_m2, col_m3, col_m4 = st.columns([1.5, 1, 1, 1])

with col_m1:
    if match_score >= 75.0:
        st.markdown(
            f"""
            <div class="score-card-green">
                <div class="score-label">Target Role Match Score</div>
                <div class="score-val-green">{match_score}%</div>
                <div style="color:var(--success); font-weight:700; font-size:0.9rem;">🟢 Industry Aligned</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    elif match_score >= 50.0:
        st.markdown(
            f"""
            <div class="score-card-amber">
                <div class="score-label">Target Role Match Score</div>
                <div class="score-val-amber">{match_score}%</div>
                <div style="color:var(--warning); font-weight:700; font-size:0.9rem;">🟠 Moderate Alignment</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="score-card-red">
                <div class="score-label">Target Role Match Score</div>
                <div class="score-val-red">{match_score}%</div>
                <div style="color:var(--error); font-weight:700; font-size:0.9rem;">🔴 Actionable Gap Identified</div>
            </div>
            """,
            unsafe_allow_html=True
        )

with col_m2:
    with st.container(border=True):
        st.caption("STUDENT NAME")
        st.markdown(f"### {student_name}")
        st.caption(f"ID: #{student_id}")

with col_m3:
    with st.container(border=True):
        st.caption("TARGET TRACK")
        st.markdown(f"### {target_role}")
        st.caption("Industry Baseline Profile")

with col_m4:
    with st.container(border=True):
        st.caption("ACTIONABLE DEFICITS")
        st.markdown(f"### {actionable_gaps_count} Skills")
        st.caption("Target Improvement Priority")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Plotly Radar Chart Generation
# -----------------------------------------------------------------------------
st.subheader("🕸️ Multi-Dimensional Skill Radar Vector")

st.info(
    f"💡 **How to Read This Radar Chart:**\n\n"
    f"• **Cyan Shape (Verified Skills)**: Represents {student_name}'s current proficiency ratings across target competencies.\n"
    f"• **Coral Shape (Role Benchmark)**: Represents the required industry standard vector for **{target_role}**.\n"
    f"• **Gap Visualization**: Any area where the Coral boundary extends beyond the Cyan shape highlights an actionable skill gap."
)

fig = create_radar_chart(student_vector, role_reqs, target_role, student_name)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. Ranked Skill Gap Table & Priority Insights
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🔥 Top Actionable Skill Deficits & Target Priorities")

if not top_gaps:
    st.success(f"🎉 Fantastic work! {student_name} meets or exceeds all required skill levels for **{target_role}**.")
else:
    col_t1, col_t2 = st.columns([1.8, 1])

    with col_t1:
        st.markdown("**Ranked Skill Deficits (Sorted by Gap Magnitude):**")
        gap_table_data = []
        for item in all_gaps:
            gap_val = item['gap']
            if gap_val >= 3:
                severity_tag = "🔴 High Deficit (-" + str(gap_val) + ")"
            elif gap_val == 2:
                severity_tag = "🟠 Moderate Deficit (-2)"
            elif gap_val == 1:
                severity_tag = "🟡 Minor Deficit (-1)"
            else:
                severity_tag = "🟢 Target Met"

            gap_table_data.append({
                "Skill Name": item["skill_name"],
                "Category": skill_cat_map.get(item["skill_id"], "DOMAIN"),
                "Your Rating": f"{item['student_level']} / 5",
                "Required Baseline": f"{item['required_level']} / 5",
                "Deficit Severity": severity_tag
            })
        
        df_gaps = pd.DataFrame(gap_table_data)
        st.dataframe(
            df_gaps,
            use_container_width=True,
            hide_index=True
        )

    with col_t2:
        st.markdown("**🎯 Immediate Recommendation Targets:**")
        for idx, gap in enumerate(top_gaps, 1):
            cat = skill_cat_map.get(gap["skill_id"], "DOMAIN")
            st.markdown(
                f"""
                <div class="metric-card-box">
                    <b>#{idx}. {gap['skill_name']}</b> <span style="font-size:0.75rem; color:var(--text-muted);">({cat})</span><br>
                    Current: <code>{gap['student_level']}/5</code> | Benchmark: <code>{gap['required_level']}/5</code><br>
                    <b style="color:var(--error);">Deficit: -{gap['gap']} levels</b>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. Recommended Next Steps & Industry-Academia Product Cards
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🎓 Recommended Next Steps & Industry Product Cards")

st.caption(
    "💡 **Academia-Industry Collaboration Hub:** Recommendations combine open learning platforms "
    "and specialized Industry Partner Programs tailored for career development."
)

if top_gaps:
    gap_recommendations = get_recommendations_for_gaps(top_gaps, n_per_skill=2)

    for idx, gap in enumerate(top_gaps, 1):
        sid = gap["skill_id"]
        res_list = gap_recommendations.get(sid, [])
        cat = skill_cat_map.get(sid, "DOMAIN")

        with st.expander(
            f"📌 Priority #{idx} Deficit: {gap['skill_name']} ({cat}) — Gap: -{gap['gap']} levels "
            f"(Current: {gap['student_level']}/5 vs Target: {gap['required_level']}/5)",
            expanded=(idx <= 2)
        ):
            if not res_list:
                st.write("No specific external program mapped for this skill.")
            else:
                cols = st.columns(len(res_list))
                for col, res in zip(cols, res_list):
                    with col:
                        with st.container(border=True):
                            type_color = (
                                "#0284c7" if res["type"] == "certification"
                                else "#059669" if res["type"] == "course"
                                else "#d97706" if res["type"] == "workshop"
                                else "#7c3aed"
                            )
                            st.markdown(
                                f"""
                                <span class="type-pill" style="background-color:{type_color};">
                                    {res['type'].upper()}
                                </span>
                                <h4 style="margin-top:0.6rem; margin-bottom:0.3rem; font-size:1.05rem; color:var(--text-primary);">{res['title']}</h4>
                                <p style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.8rem; line-height:1.4;">
                                    🏛️ <b>Provider:</b> {res['provider']}<br>
                                    ⏱️ <b>Duration:</b> {res['duration']}
                                </p>
                                """,
                                unsafe_allow_html=True
                            )
                            st.link_button(
                                "🚀 View Program / Enroll",
                                url=res.get("url", "#"),
                                use_container_width=True
                            )

