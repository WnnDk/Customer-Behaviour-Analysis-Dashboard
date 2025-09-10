"""Theme configuration for the dashboard."""

import streamlit as st

def apply_theme():
    """Apply custom theme to the dashboard."""
    st.markdown("""
        <style>
        .stMetric .metric-container {
            background-color: rgba(28, 131, 225, 0.1);
            border: 1px solid rgba(28, 131, 225, 0.1);
            border-radius: 10px;
            padding: 20px;
        }
        
        .metric-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #1c83e1;
        }
        
        .metric-value {
            font-size: 2em;
            font-weight: 700;
            color: #0c3c7c;
        }
        
        .metric-description {
            font-size: 0.9em;
            color: #666;
        }
        
        .stMarkdown {
            font-size: 1.1em;
        }
        </style>
    """, unsafe_allow_html=True)