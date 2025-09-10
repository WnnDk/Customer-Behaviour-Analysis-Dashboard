"""Theme and styling configurations for the dashboard."""

DARK_THEME = """
    <style>
    .metric-card {
        background-color: #2D2D2D;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #333;
        margin: 10px 0;
        color: #FFFFFF;
    }
    .big-number {
        color: #00ff00;
        font-size: 24px;
        font-weight: bold;
    }
    .metric-label {
        color: #888;
        font-size: 14px;
        font-weight: 500;
    }
    .help-text {
        font-size: 13px;
        color: #888;
        font-style: italic;
    }
    .stMarkdown {
        padding: 10px 0;
    }
    .data-info {
        padding: 10px;
        background-color: #2D2D2D;
        border-radius: 5px;
        margin: 10px 0;
        color: #FFFFFF;
    }
    .chart-container {
        background-color: #2D2D2D;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
    }
    div[data-testid="stDataFrame"] div[role="cell"] {
        color: #FFFFFF;
    }
    div[data-testid="stDataFrame"] th {
        color: #FFFFFF;
    }
    .stAlert {
        background-color: #2D2D2D;
        color: #FFFFFF;
    }
    </style>
"""

def apply_theme():
    """Apply the dashboard theme."""
    import streamlit as st
    st.markdown(DARK_THEME, unsafe_allow_html=True)
