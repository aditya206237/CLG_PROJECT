"""
Oppenheimer Skill Portal (Team Oppenheimer)
Skill Gap Analysis Dashboard & Plotly Radar Visualization
(Editorial Data Analytics Design System)
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

# Apply global editorial theme
apply_theme()

# Authentication Gate
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    render_login_page()
    st.stop()

render_logout_button()

# Ensure DB tables exist
init_db()


# Custom CSS matching editorial theme
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

    .metric-card-box {
        background-color: var(--bg-card);
        border: 1px solid var(--border-subtle);
        padding: 1rem 1.2rem;
        border-radius: 8px;
        height: 100%;
        color: var(--text-dark);
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
        <span class="badge-tag"><span class="live-dot" style="background-color:var(--accent-primary);"></span>Oppenheimer Vector Engine</span>
        <h1 class="hero-title">Skill Gap Analysis & <em class="italic-emphasis">Alignment Dashboard</em></h1>
        <p class="hero-subtitle">Interactive Plotly multi-dimensional radar comparison and targeted skill deficit analysis.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Student Selection & Empty State Handling
# -----------------------------------------------------------------------------
all_students = get_all_students()

if not all_students:
    with st.container(border=True):
        st.markdown(
            """
            <div style="text-align:center; padding:2rem;">
                <h2 style="color:var(--text-dark); margin-bottom:0.5rem;">⚠️ No Student Assessments Found</h2>
                <p style="color:var(--text-muted); font-size:1.05rem; max-width:600px; margin:0 auto 1.5rem auto;">
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
# 4. Large Dark Data Panel Match Score Widget & Summary
# -----------------------------------------------------------------------------
col_m1, col_m2, col_m3, col_m4 = st.columns([1.5, 1, 1, 1])

with col_m1:
    st.markdown(
        f"""
        <div class="score-card-dark" style="text-align:center;">
            <div class="dark-panel-label"><span class="live-dot"></span>MATCH SCORE • OVERALL</div>
            <div class="dark-panel-number" style="margin-top:0.4rem; font-size:3rem;">{match_score}%</div>
            <div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:var(--accent-mint); margin-top:0.4rem; text-transform:uppercase;">
                {'✓ ALIGNED' if match_score >= 75 else '• MODERATE ALIGNMENT' if match_score >= 50 else '! ACTIONABLE GAP'}
            </div>
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
# 5. Plotly Radar Chart Generation Wrapped in Dark Panel
# -----------------------------------------------------------------------------
st.subheader("🕸️ Multi-Dimensional Skill Radar Vector")

st.info(
    f"💡 **How to Read This Radar Chart:**\n\n"
    f"• **Mint Line (Verified Skills)**: Represents {student_name}'s current proficiency ratings across target competencies.\n"
    f"• **Cream Line (Role Benchmark)**: Represents the required industry standard vector for **{target_role}**.\n"
    f"• **Gap Visualization**: Any area where the Cream boundary extends beyond the Mint shape highlights an actionable skill gap."
)

fig = create_radar_chart(student_vector, role_reqs, target_role, student_name)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. Ranked Skill Gap Table & Priority Insights with Gold Badges
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 🔥 Top Actionable Skill Deficits & <em class='italic-emphasis'>Target Priorities</em>", unsafe_allow_html=True)

if not top_gaps:
    st.success(f"🎉 Fantastic work! {student_name} meets or exceeds all required skill levels for **{target_role}**.")
else:
    col_t1, col_t2 = st.columns([1.8, 1])

    with col_t1:
        st.markdown("**Ranked Skill Deficits (Sorted by Gap Magnitude & Demand Weighting):**")
        gap_table_data = []
        for item in all_gaps:
            gap_val = item['gap']
            is_high_demand = (gap_val >= 3)  # High demand weighting threshold
            
            severity_tag = "HIGH DEMAND DEFICIT (-" + str(gap_val) + ")" if is_high_demand else "STANDARD DEFICIT (-" + str(gap_val) + ")" if gap_val > 0 else "TARGET MET"

            gap_table_data.append({
                "Skill Name": item["skill_name"],
                "Category": skill_cat_map.get(item["skill_id"], "DOMAIN"),
                "Your Rating": f"{item['student_level']} / 5",
                "Required Baseline": f"{item['required_level']} / 5",
                "Priority Tag": severity_tag
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
            gap_val = gap["gap"]
            is_high_demand = (gap_val >= 3)
            
            badge_html = f'<span class="demand-badge-gold">⚡ HIGH DEMAND GAP</span>' if is_high_demand else f'<span class="demand-badge-neutral">STANDARD GAP</span>'
            
            st.markdown(
                f"""
                <div class="metric-card-box">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
                        <b>#{idx}. {gap['skill_name']}</b>
                        {badge_html}
                    </div>
                    <div style="font-size:0.85rem; color:var(--text-muted);">
                        Current: <code>{gap['student_level']}/5</code> | Benchmark: <code>{gap['required_level']}/5</code> | Deficit: <b>-{gap_val} levels</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. Recommended Next Steps & Industry Product Cards
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 🎓 Recommended Next Steps & <em class='italic-emphasis'>Industry Partner Programs</em>", unsafe_allow_html=True)

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
                            st.markdown(
                                f"""
                                <span class="badge-mono" style="color:var(--accent-primary);">
                                    [{res['type'].upper()}]
                                </span>
                                <h4 style="margin-top:0.4rem; margin-bottom:0.3rem; font-size:1.05rem; color:var(--text-dark);">{res['title']}</h4>
                                <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.8rem; line-height:1.4;">
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
