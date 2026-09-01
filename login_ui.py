"""
Oppenheimer Skill Portal (Team Oppenheimer)
Futuristic Glassmorphism Login & Registration UI Component
"""

import streamlit as st
from auth import verify_user, register_user


def apply_login_styles():
    """Injects futuristic glassmorphism and animated background CSS."""
    st.markdown(
        """
        <style>
        /* Hide sidebar and navigation menu when not logged in */
        [data-testid="stSidebar"], section[data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Hide standard header decoration for full-screen immersive view */
        header[data-testid="stHeader"] {
            background: transparent !important;
            border-bottom: none !important;
        }

        /* Glassmorphism Card Container */
        .glass-hero {
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-glow);
            border-radius: 20px;
            padding: 2.2rem 2.4rem;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.55), inset 0 0 20px rgba(56, 189, 248, 0.1);
            margin: 1.5rem auto 2rem auto;
            max-width: 540px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-hero:hover {
            border-color: var(--border-glow-hover);
            box-shadow: 0 15px 45px rgba(56, 189, 248, 0.2), inset 0 0 25px rgba(168, 85, 247, 0.15);
        }

        .auth-badge {
            display: inline-block;
            background: linear-gradient(135deg, #0284c7 0%, #7e22ce 100%);
            color: #ffffff;
            padding: 0.25rem 0.8rem;
            border-radius: 20px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.4);
        }

        .auth-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.2rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--accent-cyan) 0%, #c084fc 50%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
            letter-spacing: -0.5px;
        }

        .auth-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            line-height: 1.4;
        }

        /* Form Inputs Neon Glow */
        .stTextInput input, .stSelectbox select {
            background-color: rgba(30, 41, 59, 0.85) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(148, 163, 184, 0.3) !important;
            border-radius: 10px !important;
            transition: all 0.3s ease-in-out !important;
        }
        .stTextInput input:focus, .stSelectbox select:focus {
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.45) !important;
        }

        /* Glowing Submit Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #0284c7 0%, #7e22ce 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            padding: 0.6rem 1.2rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(126, 34, 206, 0.35) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 22px rgba(56, 189, 248, 0.55) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_login_page() -> None:
    """
    Renders the full-screen glassmorphism login and signup view.
    Stops execution until authentication succeeds.
    """
    apply_login_styles()

    col_space1, col_main, col_space2 = st.columns([1, 2.8, 1])

    with col_main:
        st.markdown(
            """
            <div class="glass-hero" style="text-align: center;">
                <span class="auth-badge">Team Oppenheimer</span>
                <h1 class="auth-title">Oppenheimer Skill Portal</h1>
                <p class="auth-subtitle">Secure Access Portal for Students, Educators & Industry Partners</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):
            tab_login, tab_signup = st.tabs(["🔑 Log In", "✨ Create Account"])

            # --- TAB 1: LOG IN ---
            with tab_login:
                st.markdown("<h4 style='color:var(--accent-cyan); margin-top:0.4rem;'>Welcome Back</h4>", unsafe_allow_html=True)
                st.caption("Enter your credentials to access your verified assessment dashboard.")

                with st.form(key="login_form"):
                    login_username = st.text_input(
                        "Username *",
                        placeholder="e.g. aarav_sharma",
                        key="login_username_val"
                    )
                    login_password = st.text_input(
                        "Password *",
                        type="password",
                        placeholder="••••••••",
                        key="login_password_val"
                    )
                    
                    login_submitted = st.form_submit_button(
                        label="🚀 Log In to Portal",
                        type="primary",
                        use_container_width=True
                    )

                    if login_submitted:
                        if not login_username.strip() or not login_password:
                            st.error("⚠️ Please fill in both Username and Password.")
                        else:
                            user_data = verify_user(login_username, login_password)
                            if user_data:
                                st.session_state.logged_in = True
                                st.session_state.user = user_data
                                st.session_state.student_name = user_data["full_name"]
                                st.success(f"✅ Welcome back, {user_data['full_name']}!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid username or password. Please try again.")

            # --- TAB 2: CREATE ACCOUNT ---
            with tab_signup:
                st.markdown("<h4 style='color:var(--accent-purple); margin-top:0.4rem;'>New Account Registration</h4>", unsafe_allow_html=True)
                st.caption("Create a new persistent profile in the Oppenheimer Skill Portal database.")

                with st.form(key="signup_form"):
                    signup_fullname = st.text_input(
                        "Full Name *",
                        placeholder="e.g. Aarav Sharma",
                        key="signup_fullname_val"
                    )
                    signup_username = st.text_input(
                        "Desired Username *",
                        placeholder="e.g. aarav_sharma",
                        key="signup_username_val"
                    )
                    signup_role = st.selectbox(
                        "Stakeholder Role Track *",
                        options=["Student", "Academician", "Industry", "Institution"],
                        index=0,
                        key="signup_role_val"
                    )
                    signup_password = st.text_input(
                        "Password * (Min 6 characters)",
                        type="password",
                        placeholder="••••••••",
                        key="signup_password_val"
                    )
                    signup_confirm = st.text_input(
                        "Confirm Password *",
                        type="password",
                        placeholder="••••••••",
                        key="signup_confirm_val"
                    )

                    signup_submitted = st.form_submit_button(
                        label="✨ Create Account & Register",
                        type="primary",
                        use_container_width=True
                    )

                    if signup_submitted:
                        if signup_password != signup_confirm:
                            st.error("⚠️ Passwords do not match. Please re-enter passwords.")
                        else:
                            success, msg = register_user(
                                username=signup_username,
                                password=signup_password,
                                full_name=signup_fullname,
                                role=signup_role
                            )
                            if success:
                                st.success(f"✅ {msg}")
                                st.info("👉 You can now switch to the **Log In** tab above to access your account.")
                            else:
                                st.error(f"❌ {msg}")


def render_logout_button() -> None:
    """
    Renders user profile badge and Log Out button in sidebar.
    """
    if "logged_in" in st.session_state and st.session_state.logged_in:
        user = st.session_state.get("user", {})
        full_name = user.get("full_name", "Assessed User")
        username = user.get("username", "user")
        role = user.get("role", "Student")

        with st.sidebar:
            st.markdown("---")
            st.markdown(
                f"""
                <div style="background:rgba(15, 23, 42, 0.85); border:1px solid var(--border-glow); border-radius:12px; padding:0.85rem; margin-bottom:0.8rem; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                    <div style="font-size:0.75rem; color:var(--text-muted); font-weight:bold; text-transform:uppercase; letter-spacing:0.5px;">Active Account</div>
                    <div style="font-size:1.05rem; font-weight:bold; color:var(--text-primary); margin-top:2px;">👤 {full_name}</div>
                    <div style="font-size:0.82rem; color:var(--accent-cyan); font-weight:600; margin-top:2px;">🏷️ {role} Track (@{username})</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🔒 Log Out", key="sidebar_logout_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.session_state.submitted = False
                st.session_state.student_id = None
                st.rerun()

