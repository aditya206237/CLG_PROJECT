"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Academician & Faculty Empowerment Portal (Preview Feature)
"""

import streamlit as st
from login_ui import render_login_page, render_logout_button
from theme import apply_theme

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Academician Portal - Oppenheimer Skill Portal",
    page_icon="👨‍🏫",
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
    .badge-preview {
        display: inline-block;
        background-color: rgba(245, 158, 11, 0.25);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        padding: 0.3rem 0.85rem;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.82rem;
        font-weight: bold;
    }
    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--accent-cyan);
        border-bottom: 2px solid var(--border-glow);
        padding-bottom: 0.4rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .acad-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        border-radius: 10px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        height: 100%;
        color: var(--text-primary);
    }
    .acad-tag {
        background-color: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.3);
        color: var(--accent-cyan);
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. Hero Header & Scoping Notice
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-preview">🔍 SIH Demo Preview Feature</span>
        <h1 class="hero-title">Academician & Faculty Empowerment Portal</h1>
        <p class="hero-subtitle">Faculty Development Programs (FDPs), Industrial Immersions, Consultancy, and Joint Research Projects.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.info(
    "💡 **Scoping & Roadmap Note (For Hackathon Judges):** This page showcases the proposed "
    "**Academician Collaboration Suite** as outlined in the Ministry of Ayush / AIIA problem statement. "
    "The listings below represent planned operational tracks for faculty enablement."
)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Section 1: Faculty Development Programs (FDPs)
# -----------------------------------------------------------------------------
st.markdown("<div class='section-title'>📚 1. Faculty Development Programs (FDPs)</div>", unsafe_allow_html=True)
st.caption("National workshops and skill enhancement programs for educators in Ayush & Health Tech.")

fdp_col1, fdp_col2 = st.columns(2)

with fdp_col1:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">National FDP</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">Artificial Intelligence & Machine Learning in Ayush Research</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Organizing Body:</b> AIIA New Delhi & IIT Delhi<br>
                📅 <b>Dates:</b> October 15–22, 2026 (1 Week Hybrid)
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Hands-on training for faculty on applying machine learning, graph neural networks, and clinical statistics to Ayurvedic clinical trial datasets.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("📝 Register Interest for FDP", key="fdp_1")

with fdp_col2:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">Pedagogy Workshop</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">Modern Curricular Design & Industry Competency Alignment</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Organizing Body:</b> Ministry of Ayush Academic Council<br>
                📅 <b>Dates:</b> November 5–8, 2026 (Online)
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Frameworks for integrating real-time industry skill gap metrics directly into undergraduate and postgraduate Ayurvedic curricula.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("📝 Register Interest for FDP", key="fdp_2")

# -----------------------------------------------------------------------------
# 4. Section 2: Industrial Training Opportunities
# -----------------------------------------------------------------------------
st.markdown("<div class='section-title'>🏭 2. Industrial Training Opportunities</div>", unsafe_allow_html=True)
st.caption("Faculty sabbatical immersion & industrial exposure programs in partner organizations.")

ind_col1, ind_col2 = st.columns(2)

with ind_col1:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">Sabbatical Immersion</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">Herbal Standardisation & Quality Control Lab Immersion</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Host Company:</b> Dabur Research & Development Center<br>
                📅 <b>Duration:</b> 4 Weeks (On-Site, Ghaziabad)
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Faculty exposure to industrial mass-spectrometry, chromatographic profiling, and regulatory compliance standards for herbal products.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("💼 Apply for Industrial Sabbatical", key="ind_1")

with ind_col2:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">Pharma Analytics Boot Camp</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">Healthcare Data Analytics & Cloud Infrastructure Training</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Host Organization:</b> National Health Authority (NHA)<br>
                📅 <b>Duration:</b> 2 Weeks (Hybrid)
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Practical training on managing large-scale electronic health records (EHR) and Ayush digital health registry standards.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("💼 Apply for Industrial Sabbatical", key="ind_2")

# -----------------------------------------------------------------------------
# 5. Section 3: Consultancy Opportunities
# -----------------------------------------------------------------------------
st.markdown("<div class='section-title'>💼 3. Consultancy Opportunities</div>", unsafe_allow_html=True)
st.caption("Industry expert consultancies and advisory roles for institution faculty.")

con_col1, con_col2 = st.columns(2)

with con_col1:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">Expert Consultancy</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">Ayurvedic Formulations Clinical Trial Protocol Auditor</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Client Organization:</b> Himalaya Wellness Company<br>
                📅 <b>Engagement:</b> 6 Months Advisory Role
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Seeking senior faculty experts to review clinical trial protocol designs and validate observational trial methodologies for herbal formulations.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("🤝 Express Consultancy Interest", key="con_1")

with con_col2:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">Tech Governance</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">AYUSH Clinical Knowledge Graph Domain Expert</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Client Organization:</b> HealthTech Innovations India<br>
                📅 <b>Engagement:</b> 3 Months Project Consultancy
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Consultancy role to supervise ontological mappings between classical Ayurvedic disease classifications and ICD-11 codes.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("🤝 Express Consultancy Interest", key="con_2")

# -----------------------------------------------------------------------------
# 6. Section 4: Collaborative Research Projects
# -----------------------------------------------------------------------------
st.markdown("<div class='section-title'>🔬 4. Collaborative Research Projects</div>", unsafe_allow_html=True)
st.caption("Joint grant calls and academia-industry collaborative research ventures.")

res_col1, res_col2 = st.columns(2)

with res_col1:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">Joint Grant Project</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">AI-Based Genomic & Metabolomic Analysis of Medicinal Plants</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Partners:</b> AIIA New Delhi & CSIR-IGIB<br>
                💰 <b>Funding Budget:</b> ₹45 Lakhs &nbsp;•&nbsp; ⏱️ <b>Duration:</b> 2 Years
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Collaborative research project to sequence high-altitude medicinal plant genomes and apply machine learning for biomarker identification.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("🔬 Submit Joint Proposal", key="res_1")

with res_col2:
    with st.container(border=True):
        st.markdown(
            """
            <span class="acad-tag">R&D Partnership</span>
            <h4 style="margin-top:0.4rem; margin-bottom:0.2rem; color:var(--text-primary);">IoT Sensors for Automated Herbal Extract Quality Monitoring</h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;">
                🏛️ <b>Partners:</b> CCRAS & Patanjali Research Foundation<br>
                💰 <b>Funding Budget:</b> ₹30 Lakhs &nbsp;•&nbsp; ⏱️ <b>Duration:</b> 18 Months
            </p>
            <p style="font-size:0.9rem; color:var(--text-secondary);">
                Development of smart micro-controller sensors and real-time dashboard monitoring systems for Ayurvedic pharmaceutical manufacturing units.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.button("🔬 Submit Joint Proposal", key="res_2")

