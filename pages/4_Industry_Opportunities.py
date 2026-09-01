"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Industry Opportunities & Candidate Vector Matching Engine
(Editorial Data Analytics Design System)
"""

import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Any

from load_taxonomy import get_all_skills
from database import get_all_students, get_student_skill_vector, init_db
from gap_analysis import build_vectors, compute_match_score
from login_ui import render_login_page, render_logout_button
from theme import apply_theme

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Industry Opportunities - Oppenheimer Skill Portal",
    page_icon="💼",
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
    .type-badge {
        display: inline-block;
        background-color: rgba(20, 73, 61, 0.1);
        border: 1px solid var(--accent-primary);
        color: var(--accent-primary);
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .skill-chip {
        display: inline-block;
        background-color: rgba(20, 73, 61, 0.08);
        color: var(--accent-primary);
        border: 1px solid rgba(20, 73, 61, 0.25);
        padding: 2px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        margin-right: 4px;
        margin-bottom: 4px;
        font-weight: 500;
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
        <span class="badge-tag"><span class="live-dot" style="background-color:var(--accent-primary);"></span>Cosine Vector Matcher</span>
        <h1 class="hero-title">Industry Opportunities & <em class="italic-emphasis">Placement Portal</em></h1>
        <p class="hero-subtitle">Discover internships, jobs, and apprenticeships dynamically ranked by skill vector alignment.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Load Opportunities Dataset
# -----------------------------------------------------------------------------
opp_file = Path(__file__).parent.parent / "data" / "opportunities.json"
opportunities: List[Dict[str, Any]] = []

if opp_file.exists():
    try:
        with open(opp_file, "r", encoding="utf-8") as f:
            opportunities = json.load(f)
    except Exception as e:
        st.error(f"Failed to load opportunities data: {e}")

if not opportunities:
    st.warning("No opportunities found in `data/opportunities.json`.")
    st.stop()

# -----------------------------------------------------------------------------
# 4. Student Selector & Vector Math Matcher
# -----------------------------------------------------------------------------
all_students = get_all_students()
all_skills_list = get_all_skills()
all_skills_map = {s["id"]: s["name"] for s in all_skills_list}

selected_student = None
student_id = None
student_name = ""
target_role = ""
student_vector: Dict[str, int] = {}

with st.sidebar:
    st.header("👤 Candidate Selection")
    
    if all_students:
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
            "Select Student Profile:",
            options=list(student_options.keys()),
            index=default_index
        )

        selected_student = student_options[selected_label]
        student_id = selected_student["student_id"]
        student_name = selected_student["name"]
        target_role = selected_student["target_role"]
        student_vector = get_student_skill_vector(student_id)
        
        st.markdown("---")
        st.success(f"✓ Vector Active for **{student_name}**")
        st.caption(f"Target Track: {target_role}")
    else:
        st.warning("No student profiles in database (`portal.db`).")
        st.info("Submit an assessment on `app.py` first to enable candidate vector matching.")

# Calculate match scores for all opportunities if student is selected
processed_opps = []

for opp in opportunities:
    opp_copy = dict(opp)
    
    if student_vector and len(student_vector) > 0:
        # Construct required benchmark vector dictionary for opportunity
        opp_req_dict = {sid: 4 for sid in opp["required_skills"]}
        
        # Build aligned vectors and calculate match score using cosine similarity
        s_vec, o_vec = build_vectors(student_vector, opp_req_dict)
        score = compute_match_score(s_vec, o_vec)
        opp_copy["match_score"] = score
    else:
        opp_copy["match_score"] = 0.0
        
    processed_opps.append(opp_copy)

# Sort opportunities by match score descending
processed_opps.sort(key=lambda x: x["match_score"], reverse=True)

# -----------------------------------------------------------------------------
# 5. Search & Filter Controls
# -----------------------------------------------------------------------------
filter_col1, filter_col2 = st.columns([1, 2])

with filter_col1:
    type_options = ["All Types", "internship", "job", "apprenticeship"]
    selected_type = st.selectbox(
        "Filter by Opportunity Type:",
        options=type_options,
        format_func=lambda x: x.title() if x != "All Types" else "All Types (All Postings)"
    )

with filter_col2:
    search_query = st.text_input(
        "Search Opportunities:",
        placeholder="e.g. Data Science, AIIA, Python, Clinical...",
        help="Search by title, company name, location, or description."
    )

# Apply filters
filtered_opps = []
for opp in processed_opps:
    # Type filter
    if selected_type != "All Types" and opp["type"].lower() != selected_type.lower():
        continue
    # Search query filter
    if search_query.strip():
        q = search_query.lower().strip()
        text_content = f"{opp['title']} {opp['company_name']} {opp['location']} {opp['description']}".lower()
        if q not in text_content:
            continue
    filtered_opps.append(opp)

# Summary Header Metrics
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric("Total Postings Match", f"{len(filtered_opps)} Opportunities")
with m_col2:
    if selected_student:
        st.metric("Active Candidate Profile", student_name)
    else:
        st.metric("Candidate Profile", "None Selected")
with m_col3:
    if filtered_opps and student_vector:
        top_match_val = filtered_opps[0]["match_score"]
        st.metric("Top Match Score", f"{top_match_val}% Alignment")
    else:
        st.metric("Top Match Score", "N/A")

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. Render Opportunity Cards List
# -----------------------------------------------------------------------------
if not filtered_opps:
    st.info("🔍 No opportunities match your search filters.")
else:
    for idx, opp in enumerate(filtered_opps):
        with st.container(border=True):
            header_left, header_right = st.columns([2.5, 1])
            
            with header_left:
                st.markdown(
                    f"""
                    <span class="type-badge">{opp['type']}</span>
                    <h3 style="margin-top:0.3rem; margin-bottom:0.1rem; color:var(--text-dark); font-family:'Playfair Display', serif; font-size:1.25rem;">
                        {opp['title']}
                    </h3>
                    <p style="color:var(--text-muted); font-size:0.92rem; margin-bottom:0.4rem;">
                        <b>Organization:</b> {opp['company_name']} &nbsp;•&nbsp; <b>Location:</b> {opp['location']} &nbsp;•&nbsp; <b>Duration:</b> {opp['duration']}
                    </p>
                    """,
                    unsafe_allow_html=True
                )
            
            with header_right:
                if student_vector:
                    score = opp["match_score"]
                    is_top = (idx == 0 and score > 0)
                    if is_top:
                        st.markdown(
                            f"""
                            <div style="text-align:right;">
                                <span class="demand-badge-gold">✓ {score}% MATCH • TOP RECOMMENDATION</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="text-align:right;">
                                <span class="demand-badge-neutral">{score}% MATCH ALIGNMENT</span>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            st.write(opp["description"])

            # Skill requirements chips
            st.markdown("**Required Skills Benchmark:**")
            chips_html = ""
            for sid in opp["required_skills"]:
                sname = all_skills_map.get(sid, sid)
                chips_html += f'<span class="skill-chip">{sname}</span>'
            st.markdown(chips_html, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col_act1, col_act2 = st.columns([1.2, 4])
            with col_act1:
                if st.button(f"Submit Application", key=f"apply_{opp['id']}"):
                    if selected_student:
                        st.success(f"Application submitted for **{student_name}** to **{opp['company_name']}**.")
                    else:
                        st.warning("Please select a student profile in the sidebar before applying.")
