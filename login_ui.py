"""
Oppenheimer Skill Portal (Team Oppenheimer)
Editorial Data Analytics Login & Registration UI Component
"""

import streamlit as st
from auth import verify_user, register_user


def apply_login_styles():
    """Injects editorial theme and background CSS for authentication."""
    st.markdown(
        """
        <style>
        /* Hide sidebar and navigation menu when not logged in */
        [data-testid="stSidebar"], section[data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] {
            display: none !important;
        }

        /* Hide standard header decoration for full-screen view */
        header[data-testid="stHeader"] {
            background: transparent !important;
            border-bottom: none !important;
        }

        /* Flat Cream Card Container */
        .glass-hero {
            background-color: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            padding: 2.2rem 2.4rem;
            box-shadow: 0 4px 20px rgba(28, 26, 22, 0.06);
            margin: 1.5rem auto 2rem auto;
            max-width: 540px;
            transition: all 0.2s ease;
        }
        .glass-hero:hover {
            border-color: #C4BEB0;
            box-shadow: 0 6px 24px rgba(28, 26, 22, 0.1);
        }

        .auth-badge {
            display: inline-block;
            background-color: rgba(20, 73, 61, 0.1);
            border: 1px solid var(--accent-primary);
            color: var(--accent-primary);
            padding: 0.25rem 0.8rem;
            border-radius: 999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .auth-title {
            font-family: 'Playfair Display', Georgia, serif;
            font-size: 2.3rem;
            font-weight: 700;
            color: var(--text-dark);
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
            letter-spacing: -0.02em;
        }

        .auth-subtitle {
            font-size: 0.95rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            line-height: 1.45;
            font-family: 'Inter', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_login_page() -> None:
    """
    Renders the full-screen editorial login and signup view.
    Stops execution until authentication succeeds.
    """
    apply_login_styles()

    col_space1, col_main, col_space2 = st.columns([1, 2.8, 1])

    with col_main:
        st.markdown(
            """
            <div class="glass-hero" style="text-align: center;">
                <span class="auth-badge">Team Oppenheimer</span>
                <h1 class="auth-title">Oppenheimer <em class="italic-emphasis">Skill Portal</em></h1>
                <p class="auth-subtitle">Academia-Industry Collaboration & Competency Matching Infrastructure</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.container(border=True):
            tab_login, tab_signup = st.tabs(["🔑 Log In", "✨ Create Account"])

            # --- TAB 1: LOG IN ---
            with tab_login:
                st.markdown("<h4 style='color:var(--text-dark); margin-top:0.4rem;'>Welcome <em class='italic-emphasis'>Back</em></h4>", unsafe_allow_html=True)
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
                        label="Log In to Portal",
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
                st.markdown("<h4 style='color:var(--text-dark); margin-top:0.4rem;'>Account <em class='italic-emphasis'>Registration</em></h4>", unsafe_allow_html=True)
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
                        label="Create Account & Register",
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
                <div style="background-color:var(--bg-card-light); border:1px solid var(--border-subtle); border-radius:8px; padding:0.9rem 1.1rem !important; margin-bottom:0.8rem;">
                    <div style="font-size:10px; color:var(--accent-primary); font-family:'JetBrains Mono', monospace; text-transform:uppercase; letter-spacing:0.08em; font-weight:700;">
                        <span class="live-dot" style="background-color:var(--accent-primary);"></span>Active Session
                    </div>
                    <div style="font-size:1.05rem; font-weight:700; color:var(--text-dark); font-family:'Playfair Display', serif; margin-top:3px;">
                        {full_name}
                    </div>
                    <div style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono', monospace; margin-top:2px;">
                        {role} Track (@{username})
                    </div>
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
