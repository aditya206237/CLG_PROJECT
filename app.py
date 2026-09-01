"""
Oppenheimer Skill Portal (Team Oppenheimer)
Student Skill Assessment & Verification Questionnaire App with SQLite Storage
"""

import streamlit as st
import time
from typing import Dict, Any
from load_taxonomy import (
    get_all_skills,
    get_skills_by_category,
    get_available_roles,
    get_role_requirements,
)
from database import (
    init_db,
    save_student,
    save_skill_responses,
    get_all_students,
    get_student_skill_vector
)
from quiz_bank import get_question_for_skill, mark_question_used
from login_ui import render_login_page, render_logout_button
from theme import apply_theme


# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Assessment - Oppenheimer Skill Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global dark futuristic theme
apply_theme()

# Authentication Gate
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    render_login_page()
    st.stop()

render_logout_button()

# Initialize database tables once per session
if "db_initialized" not in st.session_state:
    init_db()
    st.session_state.db_initialized = True# Custom CSS for rich editorial aesthetics
st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    
    /* Editorial Dark Hero Panel */
    .hero-container {
        background-color: var(--bg-dark-panel);
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E");
        border: 1px solid var(--border-dark-panel);
        color: var(--text-cream);
        padding: 2rem 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.3rem;
        font-weight: 700;
        margin: 0;
        color: var(--text-cream) !important;
        letter-spacing: -0.015em;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(239, 235, 223, 0.8);
        margin-top: 0.4rem;
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

    /* Stats Strip inside Hero */
    .hero-stats-grid {
        display: flex;
        gap: 1.8rem;
        margin-top: 1.2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(239, 235, 223, 0.12);
    }
    .hero-stat-item {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--text-cream);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .hero-stat-item span {
        color: var(--accent-mint);
        font-weight: 700;
        font-size: 13px;
    }

    /* Section Cards & Headers */
    .section-header {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text-dark);
        border-left: 4px solid var(--accent-primary);
        padding-left: 10px;
        margin-top: 0.4rem;
        margin-bottom: 1rem;
    }
    .quiz-box {
        background-color: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: var(--text-dark);
    }
    .quiz-box h4 {
        color: var(--accent-primary) !important;
        font-family: 'Playfair Display', Georgia, serif !important;
    }
    .quiz-box p {
        color: var(--text-dark) !important;
    }
    
    /* Rating helper labels */
    .rating-legend {
        font-size: 0.88rem;
        color: var(--text-muted);
        background-color: #F8F5EE;
        border: 1px solid var(--border-subtle);
        padding: 0.5rem 0.9rem;
        border-radius: 6px;
        margin-bottom: 1.2rem;
    }
    .rating-legend b {
        color: var(--text-dark);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 2. Session State Initialization
# -----------------------------------------------------------------------------
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "student_id" not in st.session_state:
    st.session_state.student_id = None
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "target_role" not in st.session_state:
    st.session_state.target_role = ""
if "skill_vector" not in st.session_state:
    st.session_state.skill_vector = {}
if "adjusted_skill_vector" not in st.session_state:
    st.session_state.adjusted_skill_vector = {}
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {}

# -----------------------------------------------------------------------------
# 3. Sidebar Information & Admin View
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/color/96/graduation-cap.png", width=70)
    st.title("Oppenheimer Skill Portal")
    st.caption("Academia-Industry Skill Assessment & Gap Engine")
    st.markdown("---")
    
    st.markdown("### 📋 Rating Scale Guide")
    st.markdown("""
    - **Level 1**: Basic awareness / Beginner
    - **Level 2**: Elementary understanding
    - **Level 3**: Intermediate / Practical experience
    - **Level 4**: Advanced / Project-ready
    - **Level 5**: Expert / Mastery
    """)
    
    st.markdown("---")
    st.info("💡 **SQLite Integration**: All assessments are persisted in `portal.db` upon submission.")

    with st.expander("🗄️ Database Quick-View (Admin)"):
        try:
            records = get_all_students()
            if records:
                st.markdown(f"**Total Registered Students:** `{len(records)}`")
                st.dataframe(records, use_container_width=True)
            else:
                st.caption("No student assessments saved yet.")
        except Exception as e:
            st.error(f"Error loading records: {e}")

# -----------------------------------------------------------------------------
# 4. Hero Header & Live Stats Strip
# -----------------------------------------------------------------------------
all_skills_count = len(get_all_skills())
available_roles = get_available_roles()
db_students = get_all_students()

st.markdown(
    f"""
    <div class="hero-container">
        <span class="badge-tag"><span class="live-dot" style="background-color:var(--accent-primary);"></span>Team Oppenheimer</span>
        <h1 class="hero-title">Student Skill <em class="italic-emphasis">Assessment</em> Questionnaire</h1>
        <p class="hero-subtitle">Evaluate your technical, domain, and soft skills with verification micro-quizzes and persistent database storage.</p>
        <div class="hero-stats-grid" style="border-top:1px solid var(--border-subtle);">
            <div class="hero-stat-item" style="color:var(--text-muted);">Skills Tracked: <span style="color:var(--accent-primary);">+{all_skills_count}</span></div>
            <div class="hero-stat-item" style="color:var(--text-muted);">Career Tracks: <span style="color:var(--accent-primary);">{len(available_roles)}</span></div>
            <div class="hero-stat-item" style="color:var(--text-muted);">Assessed Students: <span style="color:var(--accent-primary);">{len(db_students)}</span></div>
            <div class="hero-stat-item" style="color:var(--text-muted);">Vector Engine: <span style="color:var(--accent-primary);">Cosine Math</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------------------------------------------------
# 5. Assessment Form Setup
# -----------------------------------------------------------------------------
tech_skills = get_skills_by_category("technical")
domain_skills = get_skills_by_category("domain")
soft_skills = get_skills_by_category("soft")

# Render Form enclosed in Container
with st.form(key="assessment_form"):
    
    with st.container(border=True):
        st.markdown("<div class='section-header'>Step 1: Student Profile & Career Target</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            student_name_input = st.text_input(
                "Full Student Name *",
                value=st.session_state.student_name,
                placeholder="e.g. Aarav Sharma",
                help="Enter your full name for skill verification."
            )
        with col2:
            target_role_input = st.selectbox(
                "Target Career Role *",
                options=available_roles,
                index=0 if not st.session_state.target_role else available_roles.index(st.session_state.target_role),
                help="Select the career track you are targeting for gap analysis."
            )
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("<div class='section-header'>Step 2: Competency Assessment & Verification</div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="rating-legend">
                <b>Rating Scale:</b> 1 = Basic Awareness &nbsp;|&nbsp; 2 = Elementary &nbsp;|&nbsp; 3 = Intermediate &nbsp;|&nbsp; 4 = Advanced &nbsp;|&nbsp; 5 = Expert
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Organize assessment into Category Tabs
        tab_tech, tab_domain, tab_soft = st.tabs([
            f"Technical Competencies ({len(tech_skills)})",
            f"Domain & Applied Skills ({len(domain_skills)})",
            f"Professional Aptitude ({len(soft_skills)})"
        ])
        
        ratings_input: Dict[str, int] = {}
        
        # --- TAB 1: TECHNICAL SKILLS ---
        with tab_tech:
            st.markdown("#### Technical Skills Evaluation")
            st.caption("Rate your proficiency with core programming, tooling, and backend concepts.")
            
            for skill in tech_skills:
                ratings_input[skill["id"]] = st.slider(
                    label=f"**{skill['name']}**",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    help=skill["description"],
                    key=f"slider_{skill['id']}"
                )
                st.divider()
            
            # Technical Micro-Quiz Question (Dynamic Rotation from quiz_bank)
            tech_q_data = get_question_for_skill("py_prog")
            st.markdown(
                f"""
                <div class="quiz-box">
                    <h4 style="margin-top:0;">Technical Competency Verification</h4>
                    <p><b>Verification Question:</b> {tech_q_data['question']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            tech_quiz_ans = st.radio(
                "Select your answer:",
                options=tech_q_data["options"],
                key="quiz_tech"
            )

        # --- TAB 2: DOMAIN SKILLS ---
        with tab_domain:
            st.markdown("#### Domain & Track-Specific Skills")
            st.caption("Evaluate your expertise in domain methodologies and role-specific competencies.")
            
            for skill in domain_skills:
                ratings_input[skill["id"]] = st.slider(
                    label=f"**{skill['name']}**",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    help=skill["description"],
                    key=f"slider_{skill['id']}"
                )
                st.divider()

            # Domain Micro-Quiz Question (Dynamic Rotation from quiz_bank)
            domain_q_data = get_question_for_skill("machine_learning")
            st.markdown(
                f"""
                <div class="quiz-box">
                    <h4 style="margin-top:0;">Domain Competency Verification</h4>
                    <p><b>Verification Question:</b> {domain_q_data['question']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            domain_quiz_ans = st.radio(
                "Select your answer:",
                options=domain_q_data["options"],
                key="quiz_domain"
            )

        # --- TAB 3: SOFT SKILLS ---
        with tab_soft:
            st.markdown("#### Professional Aptitude & Collaboration")
            st.caption("Self-assess your interpersonal, collaborative, and problem-solving abilities.")
            
            for skill in soft_skills:
                ratings_input[skill["id"]] = st.slider(
                    label=f"**{skill['name']}**",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1,
                    help=skill["description"],
                    key=f"slider_{skill['id']}"
                )
                st.divider()

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(
        label="Submit Assessment & Generate Profile",
        type="primary",
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 6. Form Submission, Quiz Adjustment & SQLite Persistence
# -----------------------------------------------------------------------------
if submit_button:
    if not student_name_input.strip():
        st.error("Please enter your Full Student Name before submitting.")
    else:
        with st.spinner("Calibrating skill ratings with verification checks and recording profile..."):
            time.sleep(0.5)  # Subtle feedback delay
            
            # Check Quiz Correctness
            tech_quiz_correct = (tech_quiz_ans == tech_q_data["correct"])
            domain_quiz_correct = (domain_quiz_ans == domain_q_data["correct"])
            
            # Mark served questions as used on actual form submission
            mark_question_used(tech_q_data["skill_id"], tech_q_data["index"])
            mark_question_used(domain_q_data["skill_id"], domain_q_data["index"])

            # Copy raw self-ratings into adjusted ratings vector
            adjusted_ratings = dict(ratings_input)
            
            # Verification Adjustment Logic:
            if not tech_quiz_correct:
                for tech_skill_id in ["data_struct", "py_prog"]:
                    if adjusted_ratings.get(tech_skill_id, 0) > 3:
                        adjusted_ratings[tech_skill_id] = 3

            if not domain_quiz_correct:
                for dom_skill_id in ["machine_learning", "stat_analysis", "seo_opt"]:
                    if adjusted_ratings.get(dom_skill_id, 0) > 3:
                        adjusted_ratings[dom_skill_id] = 3

            # Persistent Database Storage Operations
            try:
                # 1. Save student record
                new_student_id = save_student(student_name_input, target_role_input)
                
                # 2. Save skill responses
                save_skill_responses(new_student_id, ratings_input, adjusted_ratings)
                
                # 3. Update session state
                st.session_state.submitted = True
                st.session_state.student_id = new_student_id
                st.session_state.student_name = student_name_input.strip()
                st.session_state.target_role = target_role_input
                st.session_state.skill_vector = ratings_input
                st.session_state.adjusted_skill_vector = adjusted_ratings
                st.session_state.quiz_scores = {
                    "Technical Quiz": "Verified" if tech_quiz_correct else "Calibrated (Benchmark Adjusted)",
                    "Domain Quiz": "Verified" if domain_quiz_correct else "Calibrated (Benchmark Adjusted)"
                }
                
                st.success(f"Assessment successfully recorded. Assigned Candidate ID: #{new_student_id}")

            except Exception as db_err:
                st.error(f"Database Operation Failed: {db_err}")

# -----------------------------------------------------------------------------
# 7. Display Results & Persistent Output
# -----------------------------------------------------------------------------
if st.session_state.submitted and st.session_state.student_id:
    st.markdown("---")
    st.markdown("<div class='section-header'>Assessment Summary & Analytics Navigation</div>", unsafe_allow_html=True)
    
    # Navigation links for results & portfolio
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.page_link("pages/3_Portfolio.py", label="View Verified Student Portfolio", icon="🎓", use_container_width=True)
    with nav_col2:
        st.page_link("pages/2_Results.py", label="View Skill Gap & Alignment Report", icon="📊", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a:
        st.metric("Student ID", f"#{st.session_state.student_id}")
    with col_b:
        st.metric("Student Name", st.session_state.student_name)
    with col_c:
        st.metric("Target Role Track", st.session_state.target_role)
    with col_d:
        st.metric("Total Skills Assessed", f"{len(st.session_state.skill_vector)} Skills")

    st.markdown("#### Competency Verification Summary")
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        tech_status = st.session_state.quiz_scores.get("Technical Quiz", "")
        if "Correct" in tech_status:
            st.success(f"**Technical Quiz:** {tech_status}")
        else:
            st.warning(f"**Technical Quiz:** {tech_status}")
    with q_col2:
        domain_status = st.session_state.quiz_scores.get("Domain Quiz", "")
        if "Correct" in domain_status:
            st.success(f"**Domain Quiz:** {domain_status}")
        else:
            st.warning(f"**Domain Quiz:** {domain_status}")

    with st.expander("🔍 View Skill Vector (Fetched from SQLite)", expanded=True):
        db_vector = get_student_skill_vector(st.session_state.student_id)
        st.markdown(f"**Retrieved Vector for Student #{st.session_state.student_id}:**")
        st.json(db_vector)

    role_reqs = get_role_requirements(st.session_state.target_role)
    with st.expander(f"📋 Target Role Requirements Baseline [{st.session_state.target_role}]"):
        st.dataframe(
            [
                {
                    "Skill ID": item["skill_id"],
                    "Skill Name": item["name"],
                    "Category": item["category"].upper(),
                    "Required Level (1-5)": item["required_level"],
                    "Stored Verified Level": st.session_state.adjusted_skill_vector.get(item["skill_id"], 0)
                }
                for item in role_reqs
            ],
            use_container_width=True
        )

    if st.button("🔄 Take Another Assessment"):
        st.session_state.submitted = False
        st.session_state.student_id = None
        st.rerun()
