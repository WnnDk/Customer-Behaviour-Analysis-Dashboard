"""Component for displaying metrics in a card format."""

import streamlit as st

def metric_card(label: str, value: str, help_text: str = None):
    """Display a metric in a styled card.
    
    Args:
        label: The metric label
        value: The metric value
        help_text: Optional help text to display
    """
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="big-number">{value}</div>
            {f'<div class="help-text">{help_text}</div>' if help_text else ''}
        </div>
    """, unsafe_allow_html=True)

