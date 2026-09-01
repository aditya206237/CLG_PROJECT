"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Institutional Cohort Skill Analytics & Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from typing import Dict, List, Any

from load_taxonomy import get_all_skills
from database import get_all_students, get_student_skill_vector, init_db
from gap_analysis import build_vectors, compute_match_score, compute_skill_gaps
from login_ui import render_login_page, render_logout_button
from theme import apply_theme

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Institution Dashboard - Oppenheimer Skill Portal",
    page_icon="🏛️",
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


# Custom CSS matching theme
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
    .chart-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        color: var(--text-primary);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. Hero Header Section
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-tag">Institutional Intelligence</span>
        <h1 class="hero-title">Institution Cohort Analytics Dashboard</h1>
        <p class="hero-subtitle">Macro-level readiness metrics, aggregate curriculum skill gaps, and role track distribution.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Data Retrieval & Cohort Aggregations
# -----------------------------------------------------------------------------
all_students = get_all_students()

if not all_students:
    st.warning("⚠️ No student assessment records found in SQLite database (`portal.db`).")
    st.info("👉 Please submit student assessments via the **Assessment Questionnaire** (`app.py`) to populate cohort analytics.")
    st.stop()

all_skills_list = get_all_skills()
all_skills_map = {s["id"]: s["name"] for s in all_skills_list}

# Process each student record
student_metrics_list = []
role_counts = Counter()
skill_gap_counts = Counter()  # skill_name -> number of students affected
skill_gap_magnitudes = Counter()  # skill_name -> sum of deficit gaps

total_match_score = 0.0

for s in all_students:
    sid = s["student_id"]
    sname = s["name"]
    target_role = s["target_role"]
    created_at = s.get("created_at", "N/A")

    role_counts[target_role] += 1

    # Fetch skill vector
    s_vec_dict = get_student_skill_vector(sid)
    s_vec, r_vec = build_vectors(s_vec_dict, target_role)
    match_score = compute_match_score(s_vec, r_vec)
    total_match_score += match_score

    # Compute skill gaps
    gaps = compute_skill_gaps(s_vec_dict, target_role)
    positive_gaps = [g for g in gaps if g["gap"] > 0]

    for g in positive_gaps:
        s_name = g["skill_name"]
        skill_gap_counts[s_name] += 1
        skill_gap_magnitudes[s_name] += g["gap"]

    student_metrics_list.append({
        "Student ID": f"#{sid}",
        "Student Name": sname,
        "Target Role Track": target_role,
        "Role Alignment Score": f"{match_score}%",
        "Raw Score": match_score,
        "Actionable Deficits": len(positive_gaps),
        "Submission Time": created_at
    })

avg_cohort_match = round(total_match_score / len(all_students), 1) if all_students else 0.0
top_deficit_skill = skill_gap_counts.most_common(1)[0][0] if skill_gap_counts else "None"

# Sidebar Quick View
with st.sidebar:
    st.header("🏛️ Cohort Summary")
    st.markdown(f"**Total Assessed Students:** `{len(all_students)}`")
    st.markdown(f"**Cohort Avg Alignment:** `{avg_cohort_match}%`")
    st.markdown(f"**Active Career Tracks:** `{len(role_counts)}`")
    st.markdown("---")
    st.caption("Data source: Persistent SQLite DB (`portal.db`)")

# -----------------------------------------------------------------------------
# 4. Summary Metric Cards
# -----------------------------------------------------------------------------
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(label="Total Students Assessed", value=f"{len(all_students)} Students")
with col_m2:
    st.metric(
        label="Cohort Average Match Score",
        value=f"{avg_cohort_match}%",
        delta="Industry Target: 75%",
        delta_color="normal" if avg_cohort_match >= 75 else "inverse"
    )
with col_m3:
    st.metric(label="Top Cohort Deficit Skill", value=top_deficit_skill)
with col_m4:
    st.metric(label="Configured Target Roles", value=f"{len(role_counts)} Tracks")

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Cohort Analytics Charts (Plotly)
# -----------------------------------------------------------------------------
col_c1, col_c2 = st.columns([1.6, 1])

with col_c1:
    st.subheader("📊 Most Common Skill Deficits Across All Students")
    st.caption("Aggregated count of students experiencing actionable skill deficits per competence.")

    if not skill_gap_counts:
        st.success("🎉 All assessed students currently meet or exceed their target role requirements!")
    else:
        df_gaps = pd.DataFrame([
            {"Skill Name": k, "Affected Students": v, "Total Deficit Volume": skill_gap_magnitudes[k]}
            for k, v in skill_gap_counts.most_common(10)
        ])

        fig_gaps = px.bar(
            df_gaps,
            x="Affected Students",
            y="Skill Name",
            orientation="h",
            color="Total Deficit Volume",
            color_continuous_scale="Reds",
            title="Top 10 Actionable Skill Deficits across Cohort",
            text="Affected Students"
        )
        fig_gaps.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f8fafc', family='Inter, sans-serif'),
            xaxis=dict(gridcolor='rgba(148, 163, 184, 0.25)', tickfont=dict(color='#cbd5e1')),
            yaxis=dict(autorange="reversed", gridcolor='rgba(148, 163, 184, 0.25)', tickfont=dict(color='#f8fafc')),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            coloraxis_showscale=False
        )
        fig_gaps.update_traces(textposition="outside")
        st.plotly_chart(fig_gaps, use_container_width=True)

with col_c2:
    st.subheader("🎯 Target Role Track Breakdown")
    st.caption("Distribution of students across target industry career tracks.")

    df_roles = pd.DataFrame([
        {"Target Role Track": k, "Student Count": v}
        for k, v in role_counts.items()
    ])

    fig_roles = px.pie(
        df_roles,
        values="Student Count",
        names="Target Role Track",
        title="Student Distribution by Target Track",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_roles.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc', family='Inter, sans-serif'),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_roles, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. Interactive Student Records Table
# -----------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Student Assessment Roster & Readiness Scores")
st.caption("Complete table of student assessments fetched from `portal.db`. Click table headers to sort.")

df_students = pd.DataFrame(student_metrics_list)
# Drop raw score column used for internal calculation
df_display = df_students.drop(columns=["Raw Score"])

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)

