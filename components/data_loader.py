"""Data loading and preprocessing utilities."""

import streamlit as st
import pandas as pd
import time

@st.cache_data
def load_data(uploaded_file):
    """Load and preprocess data from uploaded file."""
    if uploaded_file is not None:
        try:
            # Check file size
            if uploaded_file.size > 200 * 1024 * 1024:  # 200MB limit
                st.error("File terlalu besar. Maksimum ukuran file adalah 200MB.")
                return None

            # Show loading state
            with st.spinner('Loading data...'):
                # Load data
                df = pd.read_csv(uploaded_file, encoding="latin1")
                
                # Validate required columns
                required_columns = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 
                                 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    st.error(f"Kolom yang diperlukan tidak ditemukan: {', '.join(missing_columns)}")
                    return None

                # Basic preprocessing
                df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
                if df['InvoiceDate'].isna().any():
                    st.warning("Beberapa tanggal tidak valid dan akan dilewati")
                
                # Remove rows with missing essential data
                df = df.dropna(subset=['CustomerID', 'InvoiceNo'])
                
                # Success notification
                st.success("Data berhasil dimuat! ✅")
                
                return df
        except Exception as e:
            st.error(f"Error saat memuat data: {str(e)}")
            return None
    
    return None

def display_data_preview(df: pd.DataFrame):
    """Display data preview and basic information."""
    st.markdown("### 📋 Data Preview")
    df.index = df.index + 1
    st.dataframe(df.head(100))
    
    st.markdown("""
    <div class="data-info">
        <div class="metric-label">📅 Periode Data</div>
        <div class="big-number" style="font-size: 18px;">
    """, unsafe_allow_html=True)
    st.write(f"{df['InvoiceDate'].min().date()} sampai {df['InvoiceDate'].max().date()}")
    st.markdown('</div></div>', unsafe_allow_html=True)

