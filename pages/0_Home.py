"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Home & Overview Page
"""

import streamlit as st
import json
from pathlib import Path
from load_taxonomy import get_all_skills, get_available_roles
from database import get_all_students, init_db

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Home - Academia-Industry Collaboration Portal",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure DB tables exist
init_db()

# Custom CSS matching theme across app.py, 2_Results.py, and 3_Portfolio.py
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
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
        color: #ffffff;
        padding: 2.2rem 2.5rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #d0e1f9;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        line-height: 1.5;
    }
    .badge-tag {
        display: inline-block;
        background-color: #2a9d8f;
        color: #ffffff;
        padding: 0.3rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .scope-badge-live {
        background-color: #10b981;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .scope-badge-preview {
        background-color: #f59e0b;
        color: #ffffff;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: bold;
    }

    /* Cards & Grids */
    .role-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.4rem;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .role-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.12);
    }
    .role-card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 0.4rem;
        margin-bottom: 0.4rem;
    }
    .problem-box {
        background-color: #eef4fb;
        border-left: 5px solid #0d3b66;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.8rem;
    }
    .stat-box {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        border-radius: 10px;
        padding: 1.1rem;
        text-align: center;
        border: 1px solid #cbd5e1;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0d3b66;
    }
    .stat-label {
        font-size: 0.88rem;
        color: #475569;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar setup
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=70)
    st.title("Ayush / AIIA Portal")
    st.caption("Academia-Industry Collaboration Portal")
    st.markdown("---")
    st.info("💡 **Navigation Notice**: Select any portal page from the sidebar to explore specific stakeholder views.")


# -----------------------------------------------------------------------------
# 2. Hero Header & Value Proposition
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-tag">SIH Project | Ministry of Ayush / AIIA</span>
        <h1 class="hero-title">Academia-Industry Collaboration Portal</h1>
        <p class="hero-subtitle">
            An intelligent skill mapping, gap analysis, and placement alignment platform connecting students, 
            academic institutions, and industry partners in Ayush & Allied Health Sciences.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. SIH Problem Statement Summary
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="problem-box">
        <h3 style="margin-top:0; color:#0d3b66; font-size:1.2rem;">🏛️ SIH Problem Statement Overview</h3>
        <p style="margin-bottom:0.5rem; color:#1e293b; font-size:0.95rem; line-height:1.5;">
            <b>Organization:</b> Ministry of Ayush &nbsp;|&nbsp; 
            <b>Department:</b> All India Institute of Ayurveda (AIIA) &nbsp;|&nbsp; 
            <b>Category:</b> Software &nbsp;|&nbsp; 
            <b>Theme:</b> Smart Automation
        </p>
        <p style="margin-bottom:0; color:#334155; font-size:0.9rem; line-height:1.5;">
            Traditional education curricula often lack real-time visibility into evolving industry demands. 
            This portal bridges the gap by providing objective skill self-assessment, quiz verification, vector-based 
            gap analysis against target career tracks, and industry opportunity matching.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 4. Real-Time Portal Stats Strip
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
        <div class="stat-box">
            <div class="stat-number">{len(all_skills)}</div>
            <div class="stat-label">Skills Tracked</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s2:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{len(available_roles)}</div>
            <div class="stat-label">Career Tracks</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s3:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{len(all_students)}</div>
            <div class="stat-label">Students Assessed</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_s4:
    st.markdown(
        f"""
        <div class="stat-box">
            <div class="stat-number">{opp_count}</div>
            <div class="stat-label">Industry Listings</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. Stakeholder Role Cards & Navigation
# -----------------------------------------------------------------------------
st.subheader("👥 Stakeholder Portals & Capability Overview")
st.caption("Select a portal module below to navigate directly to its workspace.")

card_col1, card_col2 = st.columns(2)

with card_col1:
    with st.container(border=True):
        st.markdown(
            """
            <span class="scope-badge-live">✓ FULLY FUNCTIONAL CORE</span>
            <div class="role-card-title">🎓 Student Assessment & Portfolio</div>
            <p style="color:#475569; font-size:0.9rem; line-height:1.5;">
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
            <p style="color:#475569; font-size:0.9rem; line-height:1.5;">
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
            <p style="color:#475569; font-size:0.9rem; line-height:1.5;">
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
            <p style="color:#475569; font-size:0.9rem; line-height:1.5;">
                Faculty members access Faculty Development Programs (FDPs), industrial training immersions, 
                consultancy projects, and collaborative research initiatives.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.page_link("pages/6_Academician_Portal.py", label="👨‍🏫 View Academician Portal", icon="👨‍🏫", use_container_width=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. Honest Scoping & Evaluation Notice for Hackathon Judges
# -----------------------------------------------------------------------------
st.subheader("🛡️ Implementation Scoping Notice (For Hackathon Judges)")

st.info(
    """
    📌 **Transparent Prototype Scoping:**
    
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
