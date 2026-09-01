"""
Oppenheimer Skill Portal (Team Oppenheimer)
Shared Futuristic Dark Theme Component
---------------------------------------
Injects unified dark glassmorphism styles, glowing neon accents, and matching control aesthetics
across all pages in the application.
"""

import streamlit as st


def apply_theme() -> None:
    """
    Injects global dark futuristic theme CSS into the active Streamlit page.
    Ensures cohesive visual language (background, typography, buttons, cards, sidebar, dataframes)
    matching the glassmorphism login interface.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            --bg-primary: #070a13;
            --bg-card: rgba(15, 23, 42, 0.75);
            --bg-card-solid: #0f172a;
            --bg-card-hover: rgba(30, 41, 59, 0.85);
            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --accent-cyan: #38bdf8;
            --accent-purple: #a855f7;
            --accent-gradient: linear-gradient(135deg, #38bdf8 0%, #a855f7 100%);
            --success: #34d399;
            --warning: #fbbf24;
            --error: #f87171;
            --border-glow: rgba(56, 189, 248, 0.25);
            --border-glow-hover: rgba(56, 189, 248, 0.55);
        }

        /* Animated Grid Background & Floating Glow Orbs */
        @keyframes driftGrid {
            0% { background-position: 0px 0px, 0% 50%; }
            50% { background-position: 40px 40px, 100% 50%; }
            100% { background-position: 0px 0px, 0% 50%; }
        }

        .stApp {
            background-color: var(--bg-primary) !important;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(168, 85, 247, 0.08) 0%, transparent 40%),
                linear-gradient(rgba(15, 23, 42, 0.85), rgba(7, 10, 19, 0.95)),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
            background-size: 100% 100%, 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
            background-attachment: fixed !important;
            animation: driftGrid 30s ease infinite !important;
            color: var(--text-primary) !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Futuristic Top Accent Bar */
        .stApp::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple), var(--accent-cyan));
            background-size: 200% 100%;
            animation: moveGradient 4s linear infinite;
            z-index: 999999;
        }

        @keyframes moveGradient {
            0% { background-position: 0% 0%; }
            100% { background-position: 200% 0%; }
        }

        /* Top Header Area Background */
        header[data-testid="stHeader"] {
            background: rgba(15, 23, 42, 0.75) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid var(--border-glow) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #090d16 !important;
            border-right: 1px solid var(--border-glow) !important;
            box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3) !important;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem !important;
        }

        /* Sidebar Navigation Item Styling */
        div[data-testid="stSidebarNav"] ul li a {
            border-radius: 8px !important;
            transition: all 0.25s ease-in-out !important;
            color: var(--text-secondary) !important;
        }
        div[data-testid="stSidebarNav"] ul li a:hover {
            background-color: rgba(56, 189, 248, 0.15) !important;
            color: var(--accent-cyan) !important;
        }
        div[data-testid="stSidebarNav"] ul li a[aria-current="page"] {
            background: linear-gradient(90deg, rgba(2, 132, 199, 0.3) 0%, rgba(126, 34, 206, 0.3) 100%) !important;
            border-left: 3px solid var(--accent-cyan) !important;
            font-weight: 700 !important;
            color: var(--text-primary) !important;
        }
        div[data-testid="stSidebarNav"] ul li a span {
            color: var(--text-primary) !important;
        }

        /* Main Container Spacing */
        .main .block-container {
            padding-top: 1.8rem;
            padding-bottom: 3.5rem;
            max-width: 1150px;
        }

        /* Base Typography System */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        p, span, label, div, li {
            color: var(--text-secondary);
            font-family: 'Inter', sans-serif;
        }

        /* Global Safety Net: Force direct text in cards & containers to be readable */
        div[data-testid="stForm"], 
        div[data-testid="stExpander"],
        div[data-testid="stMetric"],
        .element-container,
        .hero-container, .role-card, .problem-box, .stat-box,
        .score-card-green, .score-card-amber, .score-card-red,
        .metric-card-box, .portfolio-section-card, .acad-card,
        .tech-card, .meta-box, .glass-hero {
            color: var(--text-primary);
        }

        /* Glassmorphism Card Containers & Expander Styling */
        div[data-testid="stForm"], div[data-testid="stExpander"] {
            background: var(--bg-card) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid var(--border-glow) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(56, 189, 248, 0.05) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        div[data-testid="stForm"]:hover, div[data-testid="stExpander"]:hover {
            border-color: var(--border-glow-hover) !important;
            box-shadow: 0 8px 30px rgba(56, 189, 248, 0.2), inset 0 0 20px rgba(168, 85, 247, 0.08) !important;
        }

        /* Input Controls (Text Inputs, Text Areas) */
        .stTextInput input, .stTextArea textarea {
            background-color: rgba(30, 41, 59, 0.85) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(148, 163, 184, 0.3) !important;
            border-radius: 8px !important;
            transition: all 0.25s ease-in-out !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.45) !important;
        }

        /* Selectbox / Dropdown Styling & High-Contrast Options List */
        div[data-baseweb="select"] > div {
            background-color: rgba(30, 41, 59, 0.85) !important;
            color: var(--text-primary) !important;
            border: 1px solid rgba(148, 163, 184, 0.3) !important;
            border-radius: 8px !important;
            transition: all 0.25s ease-in-out !important;
        }
        div[data-baseweb="select"] * {
            color: var(--text-primary) !important;
        }
        ul[role="listbox"], div[data-baseweb="popover"], div[data-baseweb="menu"] {
            background-color: #0f172a !important;
            border: 1px solid var(--accent-cyan) !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
        }
        li[role="option"] {
            background-color: #0f172a !important;
            color: var(--text-primary) !important;
            transition: background 0.2s ease !important;
        }
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: rgba(56, 189, 248, 0.2) !important;
            color: var(--accent-cyan) !important;
        }

        /* Sliders Styling */
        div[data-baseweb="slider"] {
            padding-top: 0.5rem;
            transition: all 0.25s ease-in-out !important;
        }
        div[data-baseweb="slider"] * {
            color: var(--text-primary) !important;
        }

        /* Buttons Neon Glow Style & Micro-transitions */
        .stButton > button {
            background: linear-gradient(135deg, #0284c7 0%, #7e22ce 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 14px rgba(126, 34, 206, 0.35) !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 22px rgba(56, 189, 248, 0.55) !important;
            color: #ffffff !important;
        }

        /* Tabs Styling & Smooth Transitions */
        button[data-baseweb="tab"] {
            color: var(--text-muted) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important;
            transition: all 0.25s ease-in-out !important;
            border-radius: 6px !important;
        }
        button[data-baseweb="tab"]:hover {
            color: var(--accent-cyan) !important;
            background: rgba(56, 189, 248, 0.1) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--text-primary) !important;
            border-bottom: 2px solid var(--accent-cyan) !important;
        }

        /* Metrics Styling with Gradient-Text Effect */
        div[data-testid="stMetricValue"] {
            background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-purple) 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 800 !important;
            font-size: 2rem !important;
        }
        div[data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Captions Override for WCAG Readability */
        .stCaption, div[data-testid="stCaptionContainer"], span[data-testid="stCaptionContainer"] {
            color: var(--text-muted) !important;
            font-size: 0.88rem !important;
            line-height: 1.4 !important;
        }

        /* Dataframe & Table Dark Theme */
        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            background: rgba(15, 23, 42, 0.8) !important;
            border-radius: 10px !important;
            border: 1px solid var(--border-glow) !important;
            color: var(--text-primary) !important;
        }
        div[data-testid="stDataFrame"] * {
            color: var(--text-primary) !important;
        }

        /* Alert Box Styling (Info, Success, Warning, Error) */
        div[data-testid="stAlert"] {
            background-color: rgba(15, 23, 42, 0.9) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
            border-left-width: 4px !important;
        }
        div[data-testid="stAlert"] * {
            color: var(--text-primary) !important;
        }

        /* Glowing Divider */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--border-glow), transparent) !important;
            margin: 1.8rem 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

