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
    st.session_state.db_initialized = True


# Custom CSS for rich aesthetics, card styling, and clean UI
st.markdown(
    """
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }
    
    /* Hero Banner */
    .hero-container {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-glow);
        color: var(--text-primary);
        padding: 2rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4), inset 0 0 20px rgba(56, 189, 248, 0.08);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .hero-container:hover {
        border-color: var(--border-glow-hover);
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.2), inset 0 0 25px rgba(168, 85, 247, 0.12);
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
        color: var(--text-primary);
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-muted);
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
        line-height: 1.5;
    }
    .badge-tag {
        display: inline-block;
        background: linear-gradient(135deg, #0284c7 0%, #7e22ce 100%);
        color: #ffffff;
        padding: 0.28rem 0.8rem;
        border-radius: 20px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }

    /* Stats Strip inside Hero */
    .hero-stats-grid {
        display: flex;
        gap: 1.5rem;
        margin-top: 1.2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-stat-item {
        font-size: 0.88rem;
        color: var(--text-secondary);
        font-weight: 600;
    }
    .hero-stat-item span {
        color: var(--accent-cyan);
        font-weight: 800;
    }

    /* Section Cards & Headers */
    .section-header {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--accent-cyan);
        border-left: 4px solid var(--accent-cyan);
        padding-left: 10px;
        margin-top: 0.8rem;
        margin-bottom: 1.2rem;
    }
    .quiz-box {
        background-color: rgba(30, 41, 59, 0.7);
        border: 1px solid var(--border-glow);
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        color: var(--text-primary);
    }
    .quiz-box h4 {
        color: var(--accent-cyan) !important;
    }
    .quiz-box p {
        color: var(--text-primary) !important;
    }
    
    /* Rating helper labels */
    .rating-legend {
        font-size: 0.88rem;
        color: var(--text-secondary);
        background-color: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 0.5rem 0.9rem;
        border-radius: 8px;
        margin-bottom: 1.2rem;
    }
    .rating-legend b {
        color: var(--text-primary);
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
        except Exception as err:
            st.error(f"Failed to fetch DB records: {err}")

# -----------------------------------------------------------------------------
# 4. Hero Header & Live Stats Strip
# -----------------------------------------------------------------------------
all_skills_count = len(get_all_skills())
available_roles = get_available_roles()
db_students = get_all_students()

st.markdown(
    f"""
    <div class="hero-container">
        <span class="badge-tag">Team Oppenheimer</span>
        <h1 class="hero-title">Student Skill Assessment Questionnaire</h1>
        <p class="hero-subtitle">Evaluate your technical, domain, and soft skills with verification micro-quizzes and persistent database storage.</p>
        <div class="hero-stats-grid">
            <div class="hero-stat-item">🎯 Skills Tracked: <span>{all_skills_count}</span></div>
            <div class="hero-stat-item">🎯 Career Tracks: <span>{len(available_roles)}</span></div>
            <div class="hero-stat-item">👥 Assessed Students: <span>{len(db_students)}</span></div>
            <div class="hero-stat-item">⚡ Vector Engine: <span>Cosine Similarity</span></div>
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
        st.markdown("<div class='section-header'>👤 Step 1: Student Profile & Career Target</div>", unsafe_allow_html=True)
        
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
        st.markdown("<div class='section-header'>📊 Step 2: Skill Self-Assessment & Verification</div>", unsafe_allow_html=True)
        
        st.markdown(
            """
            <div class="rating-legend">
                <b>Rating Scale:</b> 1 = No Experience &nbsp;|&nbsp; 2 = Elementary &nbsp;|&nbsp; 3 = Intermediate &nbsp;|&nbsp; 4 = Advanced &nbsp;|&nbsp; 5 = Expert
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Organize assessment into Category Tabs
        tab_tech, tab_domain, tab_soft = st.tabs([
            f"💻 Technical Skills ({len(tech_skills)})",
            f"🎯 Domain Skills ({len(domain_skills)})",
            f"🤝 Soft Skills ({len(soft_skills)})"
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
                    <h4 style="margin-top:0;">🛡️ Technical Verification Micro-Quiz</h4>
                    <p><b>Question:</b> {tech_q_data['question']}</p>
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
                    <h4 style="margin-top:0;">🛡️ Domain Verification Micro-Quiz</h4>
                    <p><b>Question:</b> {domain_q_data['question']}</p>
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
            st.markdown("#### Soft Skills & Work Ethic")
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
        label="🚀 Submit & Save Assessment",
        type="primary",
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# 6. Form Submission, Quiz Adjustment & SQLite Persistence
# -----------------------------------------------------------------------------
if submit_button:
    if not student_name_input.strip():
        st.error("⚠️ Please enter your Full Student Name before submitting.")
    else:
        with st.spinner("🔒 Calibrating skill ratings with verification quizzes & saving to database..."):
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
                    "Technical Quiz": "Correct (+ Verified)" if tech_quiz_correct else "Incorrect (Ratings Adjusted)",
                    "Domain Quiz": "Correct (+ Verified)" if domain_quiz_correct else "Incorrect (Ratings Adjusted)"
                }
                
                st.success(f"✅ Assessment successfully saved to database! Assigned Student ID: #{new_student_id}")

            except Exception as db_err:
                st.error(f"❌ Database Error: Failed to record assessment. Detail: {db_err}")

# -----------------------------------------------------------------------------
# 7. Display Results & Persistent Output
# -----------------------------------------------------------------------------
if st.session_state.submitted and st.session_state.student_id:
    st.markdown("---")
    st.markdown("<div class='section-header'>🎉 Assessment Summary & Next Steps</div>", unsafe_allow_html=True)
    
    # Navigation links for results & portfolio
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.page_link("pages/3_Portfolio.py", label="🎓 View Official Digital Student Portfolio", icon="🎓", use_container_width=True)
    with nav_col2:
        st.page_link("pages/2_Results.py", label="📊 View Multi-Dimensional Skill Radar & Gap Analysis", icon="📊", use_container_width=True)

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

    st.markdown("#### 🛡️ Micro-Quiz Verification Results")
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
