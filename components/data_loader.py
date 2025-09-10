"""Data loader component."""

import streamlit as st
import pandas as pd
from datetime import datetime

def format_date_safely(date_value):
    """Format date safely, handling both datetime and string inputs."""
    try:
        if isinstance(date_value, str):
            date_value = pd.to_datetime(date_value)
        return date_value.strftime('%Y-%m-%d')
    except:
        return str(date_value)

@st.cache_data
def load_data(uploaded_file):
    """Load and preprocess data from uploaded file.
    
    Args:
        uploaded_file: File object from st.file_uploader
        
    Returns:
        pd.DataFrame or None: Processed DataFrame if successful, None if failed
    """
    if uploaded_file is not None:
        # Coba beberapa encoding yang umum digunakan
        encodings = ['latin1', 'iso-8859-1', 'cp1252', 'utf-8']
        
        for encoding in encodings:
            try:
                # Baca CSV dengan encoding tertentu
                df = pd.read_csv(
                    uploaded_file,
                    encoding=encoding,
                    on_bad_lines='skip',
                    low_memory=False,
                    dtype={
                        'InvoiceNo': str,
                        'StockCode': str,
                        'Description': str,
                        'Quantity': float,
                        'UnitPrice': float,
                        'CustomerID': str,
                        'Country': str
                    }
                )
                
                # Jika berhasil membaca file, lakukan preprocessing
                try:
                    # Bersihkan data
                    df = df.dropna(subset=['InvoiceNo', 'Description', 'Quantity', 'UnitPrice'])
                    
                    # Convert InvoiceDate to datetime
                    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
                    df = df.dropna(subset=['InvoiceDate'])  # Hapus baris dengan tanggal invalid
                    
                    # Calculate TotalAmount
                    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
                    
                    # Filter data yang valid
                    df = df[
                        (df['Quantity'] > 0) &  # Hanya quantity positif
                        (df['UnitPrice'] > 0)   # Hanya harga positif
                    ]
                    
                    # Jika preprocessing berhasil, return DataFrame
                    return df
                    
                except Exception as e:
                    st.error(f"Error preprocessing data: {str(e)}")
                    continue
                    
            except UnicodeDecodeError:
                # Jika encoding ini gagal, coba encoding berikutnya
                st.warning(f"Failed to read with {encoding} encoding, trying next...")
                continue
                
            except Exception as e:
                # Jika ada error lain, tampilkan error dan coba encoding berikutnya
                st.warning(f"Error with {encoding} encoding: {str(e)}")
                continue
        
        # Jika semua encoding gagal
        st.error("Failed to read the file with any supported encoding")
        return None
            
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
            min_date = format_date_safely(df['InvoiceDate'].min())
            max_date = format_date_safely(df['InvoiceDate'].max())
            st.metric("Time Period", f"{min_date} to {max_date}")
        with col3:
            st.metric("Total Customers", f"{df['CustomerID'].nunique():,}")
        
        # Show sample data
        st.markdown("### 📋 Sample Data")
        st.dataframe(df.head(), width='stretch')
        
        # Show summary statistics
        st.markdown("### 📈 Summary Statistics")
        st.dataframe(df.describe(), width='stretch')