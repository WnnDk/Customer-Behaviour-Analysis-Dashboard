"""Metrics card component."""

import streamlit as st

def metric_card(title: str, value: str, description: str = ""):
    """Display a metric card with custom styling."""
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
    """, unsafe_allow_html=True)