"""Data loader component."""

import streamlit as st
import pandas as pd

@st.cache_data
def load_data(uploaded_file):
    """Load and preprocess data from uploaded file."""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Convert InvoiceDate to datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
        # Calculate TotalAmount
        df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
        
        return df
    return None

def display_data_preview(df: pd.DataFrame):
    """Display data preview section."""
    st.markdown("## 📊 Data Preview")
    
    with st.expander("ℹ️ Tentang Dataset"):
        st.markdown("""
        Dataset ini berisi transaksi penjualan dari sebuah e-commerce.
        
        Kolom-kolom penting:
        - 🔢 **InvoiceNo**: Nomor invoice untuk setiap transaksi
        - 📅 **InvoiceDate**: Tanggal dan waktu transaksi
        - 🏷️ **StockCode**: Kode produk
        - 📝 **Description**: Deskripsi produk
        - 📦 **Quantity**: Jumlah unit yang dibeli
        - 💰 **UnitPrice**: Harga per unit
        - 👤 **CustomerID**: ID unik pelanggan
        - 🌍 **Country**: Negara tempat pengiriman
        """)
    
    if df is not None:
        # Display basic information
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", f"{len(df):,}")
        with col2:
            st.metric("Time Period", f"{df['InvoiceDate'].min().strftime('%Y-%m-%d')} to {df['InvoiceDate'].max().strftime('%Y-%m-%d')}")
        with col3:
            st.metric("Total Customers", f"{df['CustomerID'].nunique():,}")
        
        # Show sample data
        st.markdown("### 📋 Sample Data")
        st.dataframe(df.head(), use_container_width=True)
        
        # Show summary statistics
        st.markdown("### 📈 Summary Statistics")
        st.dataframe(df.describe(), use_container_width=True)