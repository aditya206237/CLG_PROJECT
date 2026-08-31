"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
About, Architecture & Tech Stack Showcase Page
"""

import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="About & Architecture - Ayush Portal",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
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
        color: #d0e1f9;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
    }
    .badge-tag {
        display: inline-block;
        background-color: #2a9d8f;
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .meta-box {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
    }
    .meta-title {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: bold;
        text-transform: uppercase;
    }
    .meta-value {
        font-size: 1.15rem;
        color: #0f172a;
        font-weight: 700;
        margin-top: 0.2rem;
    }
    .tech-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
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
        <span class="badge-tag">SIH 2026 Submission</span>
        <h1 class="hero-title">About the Ayush Portal & Solution Strategy</h1>
        <p class="hero-subtitle">Comprehensive breakdown of problem statement specifications, architecture design, and technology stack.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 3. SIH Problem Statement Specifications Grid
# -----------------------------------------------------------------------------
st.subheader("🏛️ SIH Problem Statement Details")

col_p1, col_p2, col_p3, col_p4 = st.columns(4)

with col_p1:
    st.markdown(
        """
        <div class="meta-box">
            <div class="meta-title">Organization</div>
            <div class="meta-value">Ministry of Ayush</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_p2:
    st.markdown(
        """
        <div class="meta-box">
            <div class="meta-title">Department</div>
            <div class="meta-value">All India Institute of Ayurveda (AIIA)</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_p3:
    st.markdown(
        """
        <div class="meta-box">
            <div class="meta-title">Category</div>
            <div class="meta-value">Software</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_p4:
    st.markdown(
        """
        <div class="meta-box">
            <div class="meta-title">Theme</div>
            <div class="meta-value">Smart Automation</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

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
            - **Digital Portfolio & Export**: Markdown portfolio generator.
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
            <span style="font-size:0.88rem; color:#475569;">Core programming language powering data pipelines, taxonomy loaders, and vector engines.</span>
        </div>
        <div class="tech-card">
            <b>👑 Streamlit Framework</b><br>
            <span style="font-size:0.88rem; color:#475569;">Multi-page web application architecture, session state management, and custom CSS styling.</span>
        </div>
        <div class="tech-card">
            <b>🗄️ SQLite 3</b><br>
            <span style="font-size:0.88rem; color:#475569;">Zero-configuration relational database engine providing persistent storage for student profiles and skill vectors.</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with t_col2:
    st.markdown(
        """
        <div class="tech-card">
            <b>📐 Scikit-Learn & NumPy</b><br>
            <span style="font-size:0.88rem; color:#475569;">Vector transformation and high-performance Cosine Similarity mathematical computations.</span>
        </div>
        <div class="tech-card">
            <b>📊 Plotly Express & Graph Objects</b><br>
            <span style="font-size:0.88rem; color:#475569;">Interactive, high-definition Scatterpolar radar charts and cohort analytics visualizers.</span>
        </div>
        <div class="tech-card">
            <b>🐼 Pandas</b><br>
            <span style="font-size:0.88rem; color:#475569;">Data manipulation and structured DataFrame rendering for gap analysis and roster tables.</span>
        </div>
        """,
        unsafe_allow_html=True
    )
