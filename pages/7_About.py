"""
Oppenheimer Skill Portal (Team Oppenheimer)
About Page & System Architecture Showcase
(Editorial Data Analytics Design System)
"""

import streamlit as st
from login_ui import render_login_page, render_logout_button
from theme import apply_theme

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="About - Oppenheimer Skill Portal",
    page_icon="ℹ️",
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
        font-size: 2rem;
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
    .tech-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        color: var(--text-dark);
    }
    .tech-card b {
        color: var(--accent-primary) !important;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.05rem;
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
        <span class="badge-tag"><span class="live-dot" style="background-color:var(--accent-primary);"></span>Team Oppenheimer</span>
        <h1 class="hero-title">About Oppenheimer <em class="italic-emphasis">Skill Portal</em> & Architecture</h1>
        <p class="hero-subtitle">Comprehensive breakdown of platform features, system architecture, and technology stack.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. Built by Team Oppenheimer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="background-color:var(--bg-card); border:1px solid var(--border-subtle); border-left:5px solid var(--accent-primary); border-radius:8px; padding:1.5rem; margin-bottom:1.8rem;">
        <h3 style="margin-top:0; color:var(--text-dark); font-size:1.3rem;">Developed by Team <em class="italic-emphasis">Oppenheimer</em></h3>
        <p style="color:var(--text-dark); font-size:1rem; line-height:1.6; margin-bottom:0.8rem;">
            <b>Oppenheimer Skill Portal</b> is an academia-industry skill assessment and placement alignment platform.
            Our solution bridges the gap between academic education and real-world industry requirements by providing objective, multi-dimensional skill evaluation, conceptual verification, and vector-based placement matching.
        </p>
        <p style="color:var(--text-muted); font-size:0.92rem; line-height:1.5; margin-bottom:0;">
            Engineered with a focus on mathematical rigor (Cosine Similarity vector engines), clean data persistence (SQLite), and intuitive visual feedback (interactive Plotly radar charts), the portal empowers students, educators, and hiring managers alike.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 4. Solution Strategy & "Our Approach"
# -----------------------------------------------------------------------------
st.markdown("### Methodology: Competency-First <em class='italic-emphasis'>Architecture</em>", unsafe_allow_html=True)

st.markdown(
    """
    To build an impactful **Academia-Industry Collaboration Portal**, we prioritized an 
    **objective, mathematical foundation** rather than generic keyword matching:

    1. **Standardized Skill Taxonomy & Multi-Dimensional Vectors**:
       We defined 26 granular skills across **Technical**, **Domain**, and **Soft** categories, 
       mapped to real-world target career track baselines (Data Science, Full-Stack Web, Digital Marketing).

    2. **Verification Micro-Assessments & Rating Calibration**:
       Self-assessment scores can often be inflated. Our engine incorporates conceptual verification questions 
       that automatically calibrate self-ratings to prevent unverified skill claims.

    3. **Cosine Similarity Vector Math Engine**:
       We evaluate candidate readiness using Cosine Similarity math:
       $$\\text{Cosine Similarity} = \\frac{\\mathbf{A} \\cdot \\mathbf{B}}{\\|\\mathbf{A}\\| \\|\\mathbf{B}\\|}$$
       This measures proportional skill balance rather than harsh distance penalties.

    4. **Persistent Relational Layer & Stakeholder Dashboards**:
       All assessments persist in a local SQLite database (`portal.db`), powering real-time student portfolios, 
       candidate-opportunity matching, and cohort-wide institutional analytics.
    """
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Feature Implementation & Scope Matrix
# -----------------------------------------------------------------------------
st.markdown("### Feature Capability & <em class='italic-emphasis'>Operational Scope</em>", unsafe_allow_html=True)

matrix_col1, matrix_col2 = st.columns(2)

with matrix_col1:
    with st.container(border=True):
        st.markdown("#### Verified Core Modules (Operational)")
        st.markdown(
            """
            - **Student Skill Assessment Questionnaire**: Interactive sliders and category tabs.
            - **Verification Micro-Quiz Engine**: Auto-calibration logic for inflated ratings.
            - **SQLite Database Layer**: Foreign key-enabled persistent storage in `portal.db`.
            - **Plotly Radar Chart Engine**: Dual-boundary visual comparison of student vs role benchmark.
            - **Top Actionable Gap Extractor**: Ranked deficit identification engine.
            - **Digital Portfolio & Export**: PDF portfolio generator powered by `fpdf2`.
            - **Opportunity Matching Engine**: Real-time Cosine Similarity candidate ranking.
            - **Institutional Analytics**: Aggregate cohort readiness metrics and deficit bar charts.
            """
        )

with matrix_col2:
    with st.container(border=True):
        st.markdown("#### Planned Roadmap Features (Demonstration Mode)")
        st.markdown(
            """
            - **Academician Collaboration Portal**: FDP registration, sabbatical applications, consultancy calls.
            - **Industry Employer Portal**: Employer posting verification and candidate outreach.
            - **Automated Certificate Validation**: Blockchain / QR credential verification.
            - **AI Learning Path Generator**: Personalized course recommendation model fine-tuned on course syllabi.
            """
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# 6. Technology Stack Showcase
# -----------------------------------------------------------------------------
st.markdown("### Core Architecture & <em class='italic-emphasis'>Technology Stack</em>", unsafe_allow_html=True)

t_col1, t_col2 = st.columns(2)

with t_col1:
    st.markdown(
        """
        <div class="tech-card">
            <b>Python 3.10+ Analytics Core</b><br>
            <span style="font-size:0.88rem; color:var(--text-muted);">Core programming language powering data pipelines, taxonomy loaders, and vector engines.</span>
        </div>
        <div class="tech-card">
            <b>Streamlit Enterprise UI</b><br>
            <span style="font-size:0.88rem; color:var(--text-muted);">Multi-page web application architecture, session state management, and custom CSS styling.</span>
        </div>
        <div class="tech-card">
            <b>SQLite 3 Relational Database</b><br>
            <span style="font-size:0.88rem; color:var(--text-muted);">Zero-configuration relational database engine providing persistent storage for student profiles and skill vectors.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with t_col2:
    st.markdown(
        """
        <div class="tech-card">
            <b>Scikit-Learn & NumPy Vector Engine</b><br>
            <span style="font-size:0.88rem; color:var(--text-muted);">Vector transformation and high-performance Cosine Similarity mathematical computations.</span>
        </div>
        <div class="tech-card">
            <b>Plotly Visual Intelligence</b><br>
            <span style="font-size:0.88rem; color:var(--text-muted);">Interactive, high-definition Scatterpolar radar charts and cohort analytics visualizers.</span>
        </div>
        <div class="tech-card">
            <b>Pandas & FPDF2 Reporting Engine</b><br>
            <span style="font-size:0.88rem; color:var(--text-muted);">Data manipulation, structured DataFrame rendering, and PDF portfolio generation.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
