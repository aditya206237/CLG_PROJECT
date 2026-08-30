"""
Academia-Industry Collaboration Portal (Ministry of Ayush / AIIA)
Student Skill Assessment & Verification Questionnaire App with SQLite Storage
"""

import streamlit as st
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

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AIIA Skill Assessment Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database tables at application startup
init_db()

# Custom CSS for rich aesthetics and clean UI
st.markdown(
    """
    <style>
    /* Main container styling */
    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }
    
    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #0d3b66 0%, #001e3d 100%);
        color: #ffffff;
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
    }
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #d0e1f9;
        margin-top: 0.4rem;
        margin-bottom: 0.6rem;
    }
    .badge-tag {
        display: inline-block;
        background-color: #2a9d8f;
        color: #ffffff;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Section Cards & Headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0d3b66;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.4rem;
        margin-top: 1rem;
        margin-bottom: 1.2rem;
    }
    .quiz-box {
        background-color: #eef4fb;
        border: 1px solid #b8d4f4;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    /* Rating helper labels */
    .rating-legend {
        font-size: 0.85rem;
        color: #555;
        background-color: #e9ecef;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        margin-bottom: 1rem;
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
    st.title("Ayush / AIIA Portal")
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
# 4. Hero Header Section
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <span class="badge-tag">SIH 2026 Project</span>
        <h1 class="hero-title">Student Skill Assessment Questionnaire</h1>
        <p class="hero-subtitle">Evaluate your technical, domain, and soft skills with verification quizzes and persistent database storage.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------------------------------------------
# 5. Assessment Form Setup
# -----------------------------------------------------------------------------
available_roles = get_available_roles()
tech_skills = get_skills_by_category("technical")
domain_skills = get_skills_by_category("domain")
soft_skills = get_skills_by_category("soft")

# Render Form
with st.form(key="assessment_form"):
    st.markdown("<div class='section-header'>👤 Step 1: Student Information</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        student_name_input = st.text_input(
            "Full Student Name *",
            value=st.session_state.student_name,
            placeholder="e.g. Aarav Sharma",
            help="Enter your name as registered in the AIIA portal."
        )
    with col2:
        target_role_input = st.selectbox(
            "Target Career Role *",
            options=available_roles,
            index=0 if not st.session_state.target_role else available_roles.index(st.session_state.target_role),
            help="Select the career track you are targeting for gap analysis."
        )
    
    st.markdown("<div class='section-header'>📊 Step 2: Skill Self-Assessment & Verification</div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="rating-legend">
            <b>Rating Scale:</b> 1 = No Experience | 2 = Elementary | 3 = Intermediate | 4 = Advanced | 5 = Expert
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
        
        # Technical Micro-Quiz Question
        st.markdown(
            """
            <div class="quiz-box">
                <h4>🛡️ Technical Verification Micro-Quiz</h4>
                <p><b>Question:</b> Which data structure operates on a <b>First In, First Out (FIFO)</b> principle?</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        tech_quiz_ans = st.radio(
            "Select your answer:",
            options=[
                "Stack (LIFO)",
                "Queue (FIFO)",
                "Binary Search Tree",
                "Hash Table"
            ],
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

        # Domain Micro-Quiz Question
        st.markdown(
            """
            <div class="quiz-box">
                <h4>🛡️ Domain Verification Micro-Quiz</h4>
                <p><b>Question:</b> What does <b>overfitting</b> mean in Machine Learning / Data Analysis?</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        domain_quiz_ans = st.radio(
            "Select your answer:",
            options=[
                "The model performs well on training data but poorly on unseen test data.",
                "The model is too simple to capture underlying patterns.",
                "The dataset contains duplicate records across features.",
                "The training process takes too long to converge."
            ],
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

    st.markdown("---")
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
        # Check Quiz Correctness
        tech_quiz_correct = (tech_quiz_ans == "Queue (FIFO)")
        domain_quiz_correct = (domain_quiz_ans == "The model performs well on training data but poorly on unseen test data.")
        
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
        st.page_link("pages/3_Portfolio.py", label="🎓 View Official Digital Student Portfolio", icon="🎓")
    with nav_col2:
        st.page_link("pages/2_Results.py", label="📊 View Multi-Dimensional Skill Radar & Gap Analysis", icon="📊")

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
        # Verify database retrieval function get_student_skill_vector()
        db_vector = get_student_skill_vector(st.session_state.student_id)
        st.markdown(f"**Retrieved Vector for Student #{st.session_state.student_id}:**")
        st.json(db_vector)

    # Required target role vector comparison preview
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
