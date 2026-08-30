"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Skill Gap Analysis Dashboard & Plotly Radar Visualization
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Any

from load_taxonomy import get_role_requirements, get_all_skills
from database import get_all_students, get_student_skill_vector, init_db
from gap_analysis import build_vectors, compute_match_score, compute_skill_gaps, get_top_gaps
from recommend import get_recommendations_for_gaps
from charts import create_radar_chart


# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Skill Gap Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure DB tables exist
init_db()

# Custom CSS for polished UI
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        color: #ffffff;
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #93c5fd;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
    }
    .badge-tag {
        display: inline-block;
        background-color: #3b82f6;
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .metric-card {
        background: #f8fafc;
        border-left: 5px solid #3b82f6;
        padding: 1rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
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
        <span class="badge-tag">AIIA Academia-Industry Engine</span>
        <h1 class="hero-title">Skill Gap Analysis & Alignment Dashboard</h1>
        <p class="hero-subtitle">Interactive Plotly multi-dimensional radar comparison and targeted skill deficit analysis.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Student Selection & Data Loading
# -----------------------------------------------------------------------------
all_students = get_all_students()

if not all_students:
    st.warning("⚠️ No student assessment submissions found in database (`portal.db`).")
    st.info("👉 Please go to the **Assessment Questionnaire** page (`app.py`) to submit a skill assessment first.")
    st.stop()

# Sidebar Student Selector
with st.sidebar:
    st.header("👤 Student Selection")
    
    # Pre-select student_id from session_state if available
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

# -----------------------------------------------------------------------------
# 4. Profile Summary Metrics
# -----------------------------------------------------------------------------
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(
        label="Overall Role Match Score",
        value=f"{match_score}%",
        delta="Aligned" if match_score >= 70 else "Gap Identified",
        delta_color="normal" if match_score >= 70 else "inverse"
    )
with col_m2:
    st.metric(label="Student Name", value=student_name)
with col_m3:
    st.metric(label="Target Career Track", value=target_role)
with col_m4:
    actionable_gaps_count = len([g for g in all_gaps if g["gap"] > 0])
    st.metric(label="Actionable Skill Deficits", value=f"{actionable_gaps_count} Skills")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Plotly Radar Chart Generation
# -----------------------------------------------------------------------------
st.subheader("🕸️ Multi-Dimensional Skill Radar Vector")

# Plain language explanation for judges
st.info(
    f"💡 **How to Read This Radar Chart (For Hackathon Judges):**\n\n"
    f"• **Teal Shape (Your Verified Skills)**: Represents {student_name}'s current proficiency ratings across target competencies.\n"
    f"• **Coral Shape (Role Benchmark)**: Represents the required industry standard vector for **{target_role}**.\n"
    f"• **Gap Visualization**: Any area where the Coral boundary extends beyond the Teal shape highlights an actionable skill gap."
)

# Prepare and render Plotly Figure via shared charts helper
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
        st.markdown("**Ranked Skill Deficits (Sorted by Gap Size):**")
        gap_table_data = []
        for item in all_gaps:
            gap_table_data.append({
                "Skill Name": item["skill_name"],
                "Category": skill_cat_map.get(item["skill_id"], "DOMAIN"),
                "Your Level": f"{item['student_level']} / 5",
                "Required Level": f"{item['required_level']} / 5",
                "Deficit Gap": f"-{item['gap']}" if item['gap'] > 0 else "0 (Met)"
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
                <div class="metric-card">
                    <b>#{idx}. {gap['skill_name']}</b> <span style="font-size:0.75rem; color:#64748b;">({cat})</span><br>
                    Current: <code>{gap['student_level']}/5</code> | Required: <code>{gap['required_level']}/5</code><br>
                    <b style="color:#ef4444;">Deficit: -{gap['gap']} levels</b>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------------------------------------------------
# 7. Recommended Next Steps & Industry-Academia Learning Pathways
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("🎓 Recommended Next Steps & Learning Pathways")

st.caption(
    "💡 **Academia-Industry Collaboration Hub:** Recommendations combine open learning platforms "
    "and specialized Industry Partner Programs tailored for the Ministry of Ayush / AIIA ecosystem."
)

if top_gaps:
    gap_recommendations = get_recommendations_for_gaps(top_gaps, n_per_skill=2)

    for idx, gap in enumerate(top_gaps, 1):
        sid = gap["skill_id"]
        res_list = gap_recommendations.get(sid, [])
        cat = skill_cat_map.get(sid, "DOMAIN")

        with st.expander(
            f"📌 #{idx} Priority Gap: {gap['skill_name']} ({cat}) — Deficit: -{gap['gap']} levels "
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
                                "#2563eb" if res["type"] == "certification"
                                else "#059669" if res["type"] == "course"
                                else "#d97706" if res["type"] == "workshop"
                                else "#7c3aed"
                            )
                            st.markdown(
                                f"""
                                <span style="background-color:{type_color}; color:white; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:bold;">
                                    {res['type'].upper()}
                                </span>
                                <h4 style="margin-top:0.6rem; margin-bottom:0.3rem; font-size:1.05rem; color:#1e293b;">{res['title']}</h4>
                                <p style="font-size:0.85rem; color:#475569; margin-bottom:0.6rem; line-height:1.4;">
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
