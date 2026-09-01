"""
Oppenheimer Skill Portal (Team Oppenheimer)
Editorial Data Analytics Design System
---------------------------------------
Light, airy warm cream canvas (#EAE6DA / #F3F0E6) with deep teal accents (#14493D).
Near-black textured data panels (#14120F) reserved strictly as intentional focal points
for key metrics, radar charts, and institution summary cards.
"""

import streamlit as st


def apply_theme() -> None:
    """
    Injects global editorial theme CSS into the active Streamlit page.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg-cream: #EAE6DA;
            --bg-card: #F4F0E6;
            --bg-card-light: #F3F0E6;
            --bg-dark-panel: #14120F;
            --accent-primary: #14493D;
            --accent-primary-hover: #0E362D;
            --accent-mint: #8FE0B0;
            --accent-gold: #C9A227;
            --text-dark: #1C1A16;
            --text-muted: #6E695C;
            --text-cream: #EFEBDF;
            --border-subtle: #D6D0C2;
            --border-dark-panel: #28241F;
        }

        /* Warm Cream Background with Tactile SVG Noise Texture Overlay */
        .stApp {
            background-color: var(--bg-cream) !important;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E") !important;
            background-attachment: fixed !important;
            color: var(--text-dark) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Top Header Area Background */
        header[data-testid="stHeader"] {
            background-color: rgba(234, 230, 218, 0.9) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border-bottom: 1px solid var(--border-subtle) !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #E2DDD0 !important;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E") !important;
            border-right: 1px solid var(--border-subtle) !important;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem !important;
        }

        /* Sidebar Navigation Item Styling */
        div[data-testid="stSidebarNav"] ul li a {
            border-radius: 6px !important;
            transition: all 0.2s ease-in-out !important;
            color: var(--text-dark) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 500 !important;
        }
        div[data-testid="stSidebarNav"] ul li a:hover {
            background-color: rgba(20, 73, 61, 0.08) !important;
            color: var(--accent-primary) !important;
        }
        div[data-testid="stSidebarNav"] ul li a[aria-current="page"] {
            background-color: var(--accent-primary) !important;
            color: var(--text-cream) !important;
            font-weight: 600 !important;
        }
        div[data-testid="stSidebarNav"] ul li a[aria-current="page"] span {
            color: var(--text-cream) !important;
        }

        /* Main Container Spacing */
        .main .block-container {
            padding-top: 1.8rem;
            padding-bottom: 3.5rem;
            max-width: 1150px;
        }

        /* Editorial Serif Display Typography for Headings */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-dark) !important;
            font-family: 'Playfair Display', Georgia, serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em;
        }

        /* Italic Emphasis Styling for Key Headline Words */
        .italic-emphasis, em, i {
            font-family: 'Playfair Display', Georgia, serif !important;
            font-style: italic !important;
            color: var(--accent-primary) !important;
            font-weight: inherit !important;
        }

        p, span, label, div, li {
            color: var(--text-dark);
            font-family: 'Inter', sans-serif;
        }

        /* Monospace Data Labels & Badges */
        .mono-label, .badge-mono {
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            font-size: 11px !important;
            font-weight: 600 !important;
        }

        /* Light Airy Hero Banner Container */
        .hero-container {
            background-color: var(--bg-card-light) !important;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E") !important;
            border: 1px solid var(--border-subtle) !important;
            border-left: 5px solid var(--accent-primary) !important;
            color: var(--text-dark) !important;
            padding: 1.8rem 2rem !important;
            border-radius: 10px !important;
            margin-bottom: 1.8rem !important;
            box-shadow: 0 2px 10px rgba(28, 26, 22, 0.04) !important;
        }
        .hero-title {
            font-family: 'Playfair Display', Georgia, serif !important;
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: var(--text-dark) !important;
            margin: 0 !important;
        }
        .hero-subtitle {
            font-size: 1.05rem !important;
            color: var(--text-muted) !important;
            margin-top: 0.3rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* Light Badge Tag for Hero Headers */
        .badge-tag {
            display: inline-block !important;
            background-color: rgba(20, 73, 61, 0.08) !important;
            border: 1px solid var(--accent-primary) !important;
            color: var(--accent-primary) !important;
            padding: 0.25rem 0.75rem !important;
            border-radius: 4px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
        }

        /* Global Safety Net for Containers on Cream Canvas */
        div[data-testid="stForm"], 
        div[data-testid="stExpander"],
        .element-container,
        .role-card, .problem-box, .stat-box,
        .metric-card-box, .portfolio-section-card, .acad-card,
        .tech-card, .meta-box {
            color: var(--text-dark);
        }

        /* Lighter Cream Card Containers & Expanders */
        div[data-testid="stForm"], div[data-testid="stExpander"],
        .metric-card-box, .portfolio-section-card, .acad-card, .tech-card {
            background-color: var(--bg-card-light) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(28, 26, 22, 0.04) !important;
            transition: all 0.2s ease !important;
        }
        div[data-testid="stForm"]:hover, div[data-testid="stExpander"]:hover {
            border-color: #C4BEB0 !important;
            box-shadow: 0 4px 14px rgba(28, 26, 22, 0.08) !important;
        }

        /* Input Controls (Text Inputs, Text Areas) */
        .stTextInput input, .stTextArea textarea {
            background-color: #F8F5EE !important;
            color: var(--text-dark) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 6px !important;
            transition: all 0.2s ease-in-out !important;
            font-family: 'Inter', sans-serif !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: var(--accent-primary) !important;
            box-shadow: 0 0 0 2px rgba(20, 73, 61, 0.15) !important;
        }

        /* Selectbox / Dropdown Styling & Dark Popover List */
        div[data-baseweb="select"] > div {
            background-color: #F8F5EE !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 6px !important;
        }
        div[data-baseweb="select"] * {
            color: var(--text-dark) !important;
        }
        ul[role="listbox"], div[data-baseweb="popover"], div[data-baseweb="menu"] {
            background-color: var(--bg-dark-panel) !important;
            border: 1px solid var(--border-dark-panel) !important;
            border-radius: 8px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4) !important;
        }
        li[role="option"] {
            background-color: var(--bg-dark-panel) !important;
            color: var(--text-cream) !important;
            font-family: 'Inter', sans-serif !important;
            transition: background 0.2s ease !important;
        }
        li[role="option"]:hover, li[role="option"][aria-selected="true"] {
            background-color: rgba(143, 224, 176, 0.15) !important;
            color: var(--accent-mint) !important;
        }

        /* Sliders Styling */
        div[data-baseweb="slider"] {
            padding-top: 0.5rem;
        }
        div[data-baseweb="slider"] * {
            color: var(--text-dark) !important;
        }

        /* Pill-Shaped Buttons */
        .stButton > button {
            background-color: var(--accent-primary) !important;
            color: var(--text-cream) !important;
            border: none !important;
            border-radius: 999px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            font-size: 0.82rem !important;
            padding: 0.5rem 1.4rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 2px 8px rgba(20, 73, 61, 0.2) !important;
        }
        .stButton > button:hover {
            background-color: var(--accent-primary-hover) !important;
            color: var(--text-cream) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(20, 73, 61, 0.3) !important;
        }

        /* Secondary Pill Buttons (Transparent + Thin Teal Border) */
        .stDownloadButton > button, button[data-testid="stSecondaryButton"] {
            background-color: transparent !important;
            color: var(--accent-primary) !important;
            border: 1px solid var(--accent-primary) !important;
            border-radius: 999px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            font-size: 0.82rem !important;
            padding: 0.45rem 1.3rem !important;
            transition: all 0.2s ease !important;
        }
        .stDownloadButton > button:hover, button[data-testid="stSecondaryButton"]:hover {
            background-color: rgba(20, 73, 61, 0.08) !important;
            color: var(--accent-primary) !important;
            transform: translateY(-1px) !important;
        }

        /* Tabs Styling */
        button[data-baseweb="tab"] {
            color: var(--text-muted) !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            border-radius: 4px !important;
        }
        button[data-baseweb="tab"]:hover {
            color: var(--accent-primary) !important;
            background: rgba(20, 73, 61, 0.06) !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--accent-primary) !important;
            border-bottom: 2px solid var(--accent-primary) !important;
        }

        /* Metrics Styling (Cream Page Context) */
        div[data-testid="stMetricValue"] {
            color: var(--accent-primary) !important;
            font-family: 'Playfair Display', Georgia, serif !important;
            font-weight: 700 !important;
            font-size: 2.2rem !important;
        }
        div[data-testid="stMetricLabel"] {
            color: var(--text-muted) !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            font-size: 11px !important;
            font-weight: 600 !important;
        }

        /* Captions Override */
        .stCaption, div[data-testid="stCaptionContainer"], span[data-testid="stCaptionContainer"] {
            color: var(--text-muted) !important;
            font-size: 0.88rem !important;
            line-height: 1.45 !important;
        }

        /* Dataframe & Table Styling */
        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            background-color: var(--bg-card-light) !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-subtle) !important;
            color: var(--text-dark) !important;
        }
        div[data-testid="stDataFrame"] * {
            color: var(--text-dark) !important;
        }

        /* Alert Box Styling */
        div[data-testid="stAlert"] {
            background-color: var(--bg-card-light) !important;
            border-radius: 8px !important;
            border: 1px solid var(--border-subtle) !important;
            border-left: 4px solid var(--accent-primary) !important;
            box-shadow: 0 2px 8px rgba(28, 26, 22, 0.04) !important;
        }
        div[data-testid="stAlert"] * {
            color: var(--text-dark) !important;
        }

        /* Divider */
        hr {
            border: none !important;
            height: 1px !important;
            background-color: var(--border-subtle) !important;
            margin: 1.8rem 0 !important;
        }

        /* Reserved Near-Black Dark Panels (Data, Match Score, Radar Chart, Institution Mini Stats) */
        .dark-panel, .metric-card-dark, .score-card-dark, .radar-panel {
            background-color: var(--bg-dark-panel) !important;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E") !important;
            border: 1px solid var(--border-dark-panel) !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            color: var(--text-cream) !important;
            position: relative !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
        }

        .dark-panel h1, .dark-panel h2, .dark-panel h3, .dark-panel h4,
        .metric-card-dark h1, .metric-card-dark h2, .metric-card-dark h3,
        .score-card-dark h1, .score-card-dark h2, .score-card-dark h3 {
            color: var(--text-cream) !important;
        }

        .dark-panel p, .dark-panel span, .dark-panel label,
        .metric-card-dark p, .score-card-dark p {
            color: rgba(239, 235, 223, 0.8) !important;
        }

        .dark-panel-number, .stat-number-mint {
            font-family: 'JetBrains Mono', monospace !important;
            color: var(--accent-mint) !important;
            font-weight: 700 !important;
            font-size: 2.5rem !important;
            line-height: 1 !important;
        }

        .dark-panel-label {
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            font-size: 11px !important;
            color: var(--text-cream) !important;
            font-weight: 600 !important;
        }

        /* Pulsing "Live" Indicator Dot */
        .live-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--accent-mint);
            box-shadow: 0 0 0 0 rgba(143, 224, 176, 0.7);
            animation: livePulse 2s infinite;
            margin-right: 6px;
            vertical-align: middle;
        }

        @keyframes livePulse {
            0% { box-shadow: 0 0 0 0 rgba(143, 224, 176, 0.7); }
            70% { box-shadow: 0 0 0 6px rgba(143, 224, 176, 0); }
            100% { box-shadow: 0 0 0 0 rgba(143, 224, 176, 0); }
        }

        /* Skill Gap Demand Badges (Gold reserved ONLY for high demand) */
        .demand-badge-gold {
            display: inline-block;
            background-color: rgba(201, 162, 39, 0.12) !important;
            border: 1px solid var(--accent-gold) !important;
            color: var(--accent-gold) !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            padding: 3px 10px !important;
            border-radius: 4px !important;
            font-weight: 700 !important;
        }

        .demand-badge-neutral {
            display: inline-block;
            background-color: rgba(110, 105, 92, 0.12) !important;
            border: 1px solid var(--text-muted) !important;
            color: var(--text-muted) !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 11px !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            padding: 3px 10px !important;
            border-radius: 4px !important;
            font-weight: 600 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
