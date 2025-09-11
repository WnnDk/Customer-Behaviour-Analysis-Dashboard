"""E-commerce Customer Behavior Analysis Dashboard."""

import streamlit as st
from components.styles.theme import apply_theme
from components.data_loader import load_data, display_data_preview
from components.download_section import display_download_section
from components.analysis import (
    display_rfm_analysis,
    display_market_basket_analysis,
    display_churn_analysis,
    display_clv_analysis
)

# Page config
st.set_page_config(
    page_title="Customer Behavior Analysis Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply theme
apply_theme()

# Header
st.markdown("<h1 style='text-align: center;'>🛒 Customer Behavior Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em;'>Analisis perilaku pelanggan menggunakan RFM Analysis</p>", unsafe_allow_html=True)

# File upload section
col1, col2 = st.columns([3, 1])

with col1:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # For alignment
    st.download_button(
        label="📥 Download Sample Data",
        data=open("OnlineRetail.csv", "rb"),
        file_name="OnlineRetail.csv",
        mime="text/csv"
    )

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "👥 RFM Analysis",
    "📉 Churn Analysis",
    "🛍️ Market Basket",
    "💰 Customer Lifetime Value"
])

# Load data
df = load_data(uploaded_file)

if df is not None:
    # Overview Tab
    with tab1:
        st.markdown("## 📊 Overview")
        display_data_preview(df)
    
    # RFM Analysis Tab
    with tab2:
        display_rfm_analysis(df)
    
    # Churn Analysis Tab
    with tab3:
        display_churn_analysis(df)
    
    # Market Basket Analysis Tab
    with tab4:
        display_market_basket_analysis(df)
    
    # Customer Lifetime Value Tab
    with tab5:
        display_clv_analysis(df)
else:
    # Show upload prompt in each tab
    for tab in [tab1, tab2, tab3, tab4, tab5]:
        with tab:
            st.info("📤 Upload dataset untuk memulai analisis!")
