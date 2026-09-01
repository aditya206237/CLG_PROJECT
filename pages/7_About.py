"""
Oppenheimer Skill Portal (Team Oppenheimer)
About, Architecture & Tech Stack Showcase Page
"""

import streamlit as st
from login_ui import render_login_page, render_logout_button
from theme import apply_theme

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="About & Architecture - Oppenheimer Skill Portal",
    page_icon="ℹ️",
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
    .meta-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        color: var(--text-primary);
    }
    .meta-title {
        font-size: 0.82rem;
        color: var(--text-muted);
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .meta-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.15rem;
        color: var(--accent-cyan);
        font-weight: 700;
        margin-top: 0.2rem;
    }
    .tech-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        color: var(--text-primary);
        transition: all 0.25s ease !important;
    }
    .tech-card:hover {
        border-color: var(--border-glow-hover);
        transform: translateY(-2px);
    }
    .tech-card b {
        color: var(--text-primary) !important;
        font-family: 'Space Grotesk', sans-serif;
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
        <span class="badge-tag">Team Oppenheimer</span>
        <h1 class="hero-title">About Oppenheimer Skill Portal & Architecture</h1>
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
    <div style="background:rgba(30, 41, 59, 0.7); border:1px solid var(--border-glow); border-left:5px solid var(--accent-cyan); border-radius:10px; padding:1.5rem; margin-bottom:1.8rem;">
        <h3 style="margin-top:0; color:var(--accent-cyan); font-size:1.3rem;">🚀 Built by Team Oppenheimer</h3>
        <p style="color:var(--text-primary); font-size:1rem; line-height:1.6; margin-bottom:0.8rem;">
            <b>Oppenheimer Skill Portal</b> is a comprehensive academia-industry skill assessment and placement alignment platform.
            Our solution bridges the gap between academic education and real-world industry requirements by providing objective, multi-dimensional skill evaluation, conceptual quiz verification, and vector-based placement matching.
        </p>
        <p style="color:var(--text-secondary); font-size:0.92rem; line-height:1.5; margin-bottom:0;">
            Developed with a focus on mathematical rigor (Cosine Similarity vector engines), clean data persistence (SQLite), and intuitive visual feedback (interactive Plotly radar charts), the portal empowers students, educators, and hiring managers alike.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 4. Solution Strategy & "Our Approach"
# -----------------------------------------------------------------------------
st.subheader("💡 Our Approach: Skill-Assessment-First Strategy")

st.markdown(
    """
    To build a truly impactful **Academia-Industry Collaboration Portal**, we prioritized an 
    **objective, mathematical foundation** rather than generic keyword matching:

    1. **Skill Taxonomy & Multi-Dimensional Vectors**:
       We defined 26 granular skills across **Technical**, **Domain**, and **Soft** categories, 
       mapped to real-world target career track baselines (Data Science, Full-Stack Web, Digital Marketing).

    2. **Verification Micro-Quizzes & Rating Calibration**:
       Self-assessment scores can often be inflated. Our engine incorporates conceptual verification questions 
       that automatically calibrate self-ratings to prevent false skill claims.

    3. **Cosine Similarity Vector Math Engine**:
       We evaluate candidate readiness using Cosine Similarity math:
       $$\\text{Cosine Similarity} = \\frac{\\mathbf{A} \\cdot \\mathbf{B}}{\\|\\mathbf{A}\\| \\|\\mathbf{B}\\|}$$
       This measures proportional skill balance rather than harsh distance penalties.

    4. **End-to-End Persistence & Stakeholder Dashboards**:
       All assessments persist in a local SQLite database (`portal.db`), powering real-time student portfolios, 
       candidate-opportunity matching, and cohort-wide institutional analytics.
    """
)

st.markdown("---")

# -----------------------------------------------------------------------------
# 5. Feature Implementation & Scope Matrix
# -----------------------------------------------------------------------------
st.subheader("🗺️ Feature Scope & Roadmap Matrix")

matrix_col1, matrix_col2 = st.columns(2)

with matrix_col1:
    with st.container(border=True):
        st.markdown("#### ✅ Working Production Features")
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
        st.markdown("#### 🔍 Planned Roadmap Features (Preview Mode)")
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
st.subheader("🛠️ Technology Stack")

t_col1, t_col2 = st.columns(2)

with t_col1:
    st.markdown(
        """
        <div class="tech-card">
            <b>🐍 Python 3.10+</b><br>
            <span style="font-size:0.88rem; color:var(--text-secondary);">Core programming language powering data pipelines, taxonomy loaders, and vector engines.</span>
        </div>
        <div class="tech-card">
            <b>👑 Streamlit Framework</b><br>
            <span style="font-size:0.88rem; color:var(--text-secondary);">Multi-page web application architecture, session state management, and custom CSS styling.</span>
        </div>
        <div class="tech-card">
            <b>🗄️ SQLite 3</b><br>
            <span style="font-size:0.88rem; color:var(--text-secondary);">Zero-configuration relational database engine providing persistent storage for student profiles and skill vectors.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with t_col2:
    st.markdown(
        """
        <div class="tech-card">
            <b>📐 Scikit-Learn & NumPy</b><br>
            <span style="font-size:0.88rem; color:var(--text-secondary);">Vector transformation and high-performance Cosine Similarity mathematical computations.</span>
        </div>
        <div class="tech-card">
            <b>📊 Plotly Express & Graph Objects</b><br>
            <span style="font-size:0.88rem; color:var(--text-secondary);">Interactive, high-definition Scatterpolar radar charts and cohort analytics visualizers.</span>
        </div>
        <div class="tech-card">
            <b>🐼 Pandas & fpdf2</b><br>
            <span style="font-size:0.88rem; color:var(--text-secondary);">Data manipulation, structured DataFrame rendering, and PDF portfolio generation.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

