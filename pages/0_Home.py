"""
Oppenheimer Skill Portal (Team Oppenheimer)
Home & Overview Page (Editorial Design System)
"""

import streamlit as st
import json
from pathlib import Path
from load_taxonomy import get_all_skills, get_available_roles
from database import get_all_students, init_db
from login_ui import render_login_page, render_logout_button
from theme import apply_theme


# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Home - Oppenheimer Skill Portal",
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


# Custom CSS matching editorial theme
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    
    /* Hero Banner */
    .hero-container {
        background-color: var(--bg-dark-panel);
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
        border: 1px solid var(--border-dark-panel);
        color: var(--text-cream);
        padding: 2.2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0;
        color: var(--text-cream) !important;
        letter-spacing: -0.015em;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: rgba(239, 235, 223, 0.8);
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        line-height: 1.5;
        font-family: 'Inter', sans-serif;
    }
    .badge-tag {
        display: inline-block;
        background-color: rgba(143, 224, 176, 0.12);
        border: 1px solid var(--accent-mint);
        color: var(--accent-mint);
        padding: 0.25rem 0.8rem;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .scope-badge-live {
        display: inline-block;
        background-color: rgba(20, 73, 61, 0.1);
        border: 1px solid var(--accent-primary);
        color: var(--accent-primary);
        padding: 3px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .scope-badge-preview {
        display: inline-block;
        background-color: rgba(201, 162, 39, 0.12);
        border: 1px solid var(--accent-gold);
        color: var(--accent-gold);
        padding: 3px 8px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Cards & Grids */
    .role-card-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-top: 0.5rem;
        margin-bottom: 0.4rem;
    }
    .problem-box {
        background-color: var(--bg-card);
        border-left: 5px solid var(--accent-primary);
        border-radius: 8px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.8rem;
        border: 1px solid var(--border-subtle);
        border-left-width: 5px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar setup
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=70)
    st.title("Oppenheimer Skill Portal")
    st.caption("Academia-Industry Collaboration Portal")
    st.markdown("---")
    st.info("💡 **Navigation Notice**: Select any portal page from the sidebar to explore specific stakeholder views.")


# -----------------------------------------------------------------------------
# 2. Hero Header & Value Proposition
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-tag"><span class="live-dot" style="background-color:var(--accent-primary);"></span>Team Oppenheimer</span>
        <h1 class="hero-title">Oppenheimer <em class="italic-emphasis">Skill Portal</em></h1>
        <p class="hero-subtitle">
            An intelligent skill mapping, gap analysis, and placement alignment platform connecting students, 
            academic institutions, and industry partners.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Platform Mission & Overview
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="problem-box" style="background-color:var(--bg-card-light); border:1px solid var(--border-subtle); border-left:4px solid var(--accent-primary); border-radius:8px; padding:1.4rem 1.6rem; margin-bottom:1.5rem;">
        <h3 style="margin-top:0; color:var(--text-dark); font-size:1.3rem;">🚀 Platform Mission & <em class="italic-emphasis">Overview</em></h3>
        <p style="margin-bottom:0.5rem; color:var(--text-dark); font-size:0.98rem; line-height:1.5;">
            <b style="color:var(--accent-primary);">Built By:</b> Team Oppenheimer &nbsp;|&nbsp; 
            <b style="color:var(--accent-primary);">Focus:</b> Skill Verification & Placement Alignment &nbsp;|&nbsp; 
            <b style="color:var(--accent-primary);">Engine:</b> Cosine Similarity Vector Math
        </p>
        <p style="margin-bottom:0; color:var(--text-muted); font-size:0.93rem; line-height:1.6;">
            Traditional education curricula often lack real-time visibility into evolving industry demands. 
            This portal bridges the gap by providing objective skill self-assessment, quiz verification, vector-based 
            gap analysis against target career tracks, and industry opportunity matching.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 4. Real-Time Portal Stats Strip (Lighter Cream Cards)
# -----------------------------------------------------------------------------
all_skills = get_all_skills()
available_roles = get_available_roles()
all_students = get_all_students()

# Load opportunities count if file exists
opp_count = 9
opp_file = Path(__file__).parent.parent / "data" / "opportunities.json"
if opp_file.exists():
    try:
        with open(opp_file, "r", encoding="utf-8") as f:
            opp_count = len(json.load(f))
    except Exception:
        pass

col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    st.markdown(
        f"""
        <div class="metric-card-box" style="text-align:center; padding:1.1rem !important;">
            <div class="mono-label" style="color:var(--text-muted);">SKILLS TRACKED</div>
            <div style="font-family:'JetBrains Mono', monospace; color:var(--accent-primary); font-weight:700; font-size:2.2rem; margin-top:0.3rem;">{len(all_skills)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s2:
    st.markdown(
        f"""
        <div class="metric-card-box" style="text-align:center; padding:1.1rem !important;">
            <div class="mono-label" style="color:var(--text-muted);">CAREER TRACKS</div>
            <div style="font-family:'JetBrains Mono', monospace; color:var(--accent-primary); font-weight:700; font-size:2.2rem; margin-top:0.3rem;">{len(available_roles)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s3:
    st.markdown(
        f"""
        <div class="metric-card-box" style="text-align:center; padding:1.1rem !important;">
            <div class="mono-label" style="color:var(--text-muted);">STUDENTS ASSESSED</div>
            <div style="font-family:'JetBrains Mono', monospace; color:var(--accent-primary); font-weight:700; font-size:2.2rem; margin-top:0.3rem;">{len(all_students)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s4:
    st.markdown(
        f"""
        <div class="metric-card-box" style="text-align:center; padding:1.1rem !important;">
            <div class="mono-label" style="color:var(--text-muted);">INDUSTRY LISTINGS</div>
            <div style="font-family:'JetBrains Mono', monospace; color:var(--accent-primary); font-weight:700; font-size:2.2rem; margin-top:0.3rem;">{opp_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Stakeholder Portals Showcase
# -----------------------------------------------------------------------------
st.markdown("### 👥 Stakeholder Portals & <em class='italic-emphasis'>Capability Overview</em>", unsafe_allow_html=True)
st.caption("Select a portal module below to navigate directly to its workspace.")

card_col1, card_col2 = st.columns(2)

with card_col1:
    with st.container(border=True):
        st.markdown(
            """
            <span class="scope-badge-live">✓ FULLY FUNCTIONAL CORE</span>
            <div class="role-card-title">🎓 Student Assessment & Portfolio</div>
            <p style="color:var(--text-muted); font-size:0.9rem; line-height:1.5;">
                Students evaluate technical, domain, and soft skills, pass verification quizzes, view Plotly radar gap 
                visualizations against career baselines, and download verified digital portfolios.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.page_link("app.py", label="🚀 Launch Skill Assessment Questionnaire", icon="📝", use_container_width=True)

with card_col2:
    with st.container(border=True):
        st.markdown(
            """
            <span class="scope-badge-live">✓ FULLY FUNCTIONAL ENGINE</span>
            <div class="role-card-title">💼 Industry Opportunities & Matching</div>
            <p style="color:var(--text-muted); font-size:0.9rem; line-height:1.5;">
                Industry partners post internships and job opportunities. Candidates are automatically matched using 
                Cosine Similarity vector math based on their verified skill profiles.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.page_link("pages/4_Industry_Opportunities.py", label="💼 Explore Industry Opportunities", icon="💼", use_container_width=True)

card_col3, card_col4 = st.columns(2)

with card_col3:
    with st.container(border=True):
        st.markdown(
            """
            <span class="scope-badge-live">✓ COHORT ANALYTICS</span>
            <div class="role-card-title">🏛️ Institution Dashboard</div>
            <p style="color:var(--text-muted); font-size:0.9rem; line-height:1.5;">
                Academic leaders and department heads monitor cohort-wide readiness, aggregate skill deficits across 
                all assessed students, and track role distribution metrics.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.page_link("pages/5_Institution_Dashboard.py", label="📊 View Institution Analytics", icon="📊", use_container_width=True)

with card_col4:
    with st.container(border=True):
        st.markdown(
            """
            <span class="scope-badge-preview">🔍 DEMO PREVIEW & ROADMAP</span>
            <div class="role-card-title">👨‍🏫 Academician Portal</div>
            <p style="color:var(--text-muted); font-size:0.9rem; line-height:1.5;">
                Faculty members access Faculty Development Programs (FDPs), industrial training immersions, 
                consultancy projects, and collaborative research initiatives.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.page_link("pages/6_Academician_Portal.py", label="👨‍🏫 View Academician Portal", icon="👨‍🏫", use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. Implementation Scoping Overview
# -----------------------------------------------------------------------------
st.markdown("### 🛡️ Implementation Scoping Notice <em class='italic-emphasis'>(Team Oppenheimer)</em>", unsafe_allow_html=True)

st.info(
    """
    📌 **Transparent System Scoping:**
    
    • **Fully Functional Production Modules (End-to-End Working)**:
      - **Student Assessment & Micro-Quiz Engine** (`app.py`)
      - **SQLite Database Storage** (`database.py` / `portal.db`)
      - **Cosine Similarity Vector Gap Analysis** (`gap_analysis.py`)
      - **Interactive Plotly Radar & Deficit Visualization** (`pages/2_Results.py`)
      - **Verified Student Digital Portfolio** (`pages/3_Portfolio.py`)
      - **Candidate-Opportunity Cosine Vector Matcher** (`pages/4_Industry_Opportunities.py`)
      - **Real Cohort Database Aggregations** (`pages/5_Institution_Dashboard.py`)
      
    • **Preview & Demo Roadmap Modules**:
      - **Academician FDP & Consultancy Listings** (`pages/6_Academician_Portal.py` — static roadmap preview for demo complete flow).
    """
)
