"""
Oppenheimer Skill Portal (Team Oppenheimer)
Institution Cohort Analytics Dashboard
(Editorial Data Analytics Design System)
"""

import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px

from load_taxonomy import get_all_skills, get_available_roles
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

# Apply global editorial theme
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
        background-color: var(--bg-dark-panel);
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
        border: 1px solid var(--border-dark-panel);
        color: var(--text-cream);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: var(--text-cream) !important;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(239, 235, 223, 0.8);
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
    }
    .badge-tag {
        display: inline-block;
        background-color: rgba(143, 224, 176, 0.12);
        border: 1px solid var(--accent-mint);
        color: var(--accent-mint);
        padding: 0.25rem 0.75rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
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
        <span class="badge-tag"><span class="live-dot" style="background-color:var(--accent-primary);"></span>Institutional Intelligence</span>
        <h1 class="hero-title">Institution Cohort <em class="italic-emphasis">Analytics Dashboard</em></h1>
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
    st.header("Cohort Summary")
    st.markdown(f"**Total Assessed Students:** `{len(all_students)}`")
    st.markdown(f"**Cohort Avg Alignment:** `{avg_cohort_match}%`")
    st.markdown(f"**Active Career Tracks:** `{len(role_counts)}`")
    st.markdown("---")
    st.caption("Data source: Persistent SQLite DB (`portal.db`)")

# -----------------------------------------------------------------------------
# 4. Summary Metric Cards as Mini Dark Data Panels
# -----------------------------------------------------------------------------
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.markdown(
        f"""
        <div class="metric-card-dark" style="text-align:center;">
            <div class="dark-panel-label"><span class="live-dot"></span>TOTAL STUDENTS</div>
            <div class="dark-panel-number" style="margin-top:0.3rem;">{len(all_students)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_m2:
    st.markdown(
        f"""
        <div class="metric-card-dark" style="text-align:center;">
            <div class="dark-panel-label"><span class="live-dot"></span>AVG MATCH SCORE</div>
            <div class="dark-panel-number" style="margin-top:0.3rem;">{avg_cohort_match}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_m3:
    st.markdown(
        f"""
        <div class="metric-card-dark" style="text-align:center;">
            <div class="dark-panel-label"><span class="live-dot"></span>TOP DEFICIT SKILL</div>
            <div style="font-family:'JetBrains Mono', monospace; color:var(--accent-mint); font-weight:700; font-size:1rem; margin-top:0.5rem; text-transform:uppercase;">
                {top_deficit_skill[:18]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_m4:
    st.markdown(
        f"""
        <div class="metric-card-dark" style="text-align:center;">
            <div class="dark-panel-label"><span class="live-dot"></span>TARGET TRACKS</div>
            <div class="dark-panel-number" style="margin-top:0.3rem;">{len(role_counts)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Cohort Analytics Charts (Plotly Dark Theme)
# -----------------------------------------------------------------------------
col_c1, col_c2 = st.columns([1.6, 1])

with col_c1:
    st.markdown("#### Primary Competency Deficits Across Cohort")
    st.caption("Aggregated count of students experiencing actionable skill deficits per competence.")

    if not skill_gap_counts:
        st.success("All assessed students currently meet or exceed their target role requirements.")
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
            color_continuous_scale=["#14493D", "#8FE0B0"],
            title="Top 10 Actionable Skill Deficits across Cohort",
            text="Affected Students"
        )
        fig_gaps.update_layout(
            paper_bgcolor='#14120F',
            plot_bgcolor='#14120F',
            font=dict(color='#EFEBDF', family='JetBrains Mono, monospace'),
            xaxis=dict(gridcolor='rgba(239, 235, 223, 0.15)', tickfont=dict(color='#EFEBDF')),
            yaxis=dict(autorange="reversed", gridcolor='rgba(239, 235, 223, 0.15)', tickfont=dict(color='#EFEBDF')),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            coloraxis_showscale=False
        )
        fig_gaps.update_traces(textposition="outside")
        st.plotly_chart(fig_gaps, use_container_width=True)

with col_c2:
    st.markdown("#### Career Track Distribution")
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
        color_discrete_sequence=["#14493D", "#8FE0B0", "#C9A227", "#6E695C"]
    )
    fig_roles.update_layout(
        paper_bgcolor='#14120F',
        plot_bgcolor='#14120F',
        font=dict(color='#EFEBDF', family='JetBrains Mono, monospace'),
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_roles, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. Interactive Student Records Table
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### Student Assessment Roster & <em class='italic-emphasis'>Readiness Index</em>", unsafe_allow_html=True)
st.caption("Complete table of student assessments fetched from `portal.db`. Click table headers to sort.")

df_students = pd.DataFrame(student_metrics_list)
# Drop raw score column used for internal calculation
df_display = df_students.drop(columns=["Raw Score"])

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)
