"""RFM Analysis component."""

import streamlit as st
import pandas as pd
import altair as alt
from ..metrics_card import metric_card

def calculate_rfm(df: pd.DataFrame):
    """Calculate RFM metrics."""
    # Calculate reference date
    reference_date = df['InvoiceDate'].max() + pd.DateOffset(days=1)
    
    # Calculate RFM metrics
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
        'InvoiceNo': 'count',  # Frequency
        'TotalAmount': 'sum'  # Monetary
    }).reset_index()
    
    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    
    # Calculate RFM scores
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1])
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4])
    rfm['RFM_Score'] = rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)
    
    return rfm

def display_rfm_analysis(df: pd.DataFrame):
    """Display RFM analysis section."""
    st.markdown("## 👥 RFM Analysis")
    
    with st.expander("ℹ️ Apa itu RFM Analysis?"):
        st.markdown("""
        **RFM Analysis** adalah metode segmentasi customer berdasarkan 3 metrik utama:
        
        1. 📅 **Recency**: Berapa lama sejak pembelian terakhir
            - Semakin kecil nilai Recency, semakin baik (customer masih aktif)
        
        2. 🔄 **Frequency**: Seberapa sering customer melakukan pembelian
            - Semakin tinggi nilai Frequency, semakin baik
        
        3. 💰 **Monetary**: Total nilai pembelian customer
            - Semakin tinggi nilai Monetary, semakin baik
        
        Setiap metrik diberi skor 1-4, kemudian dijumlahkan untuk mendapatkan RFM Score.
        """)
    
    # Calculate RFM
    rfm = calculate_rfm(df)
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card(
            "Average Recency",
            f"{rfm['Recency'].mean():.1f} days",
            "Rata-rata waktu sejak pembelian terakhir"
        )
    
    with col2:
        metric_card(
            "Average Frequency",
            f"{rfm['Frequency'].mean():.1f}",
            "Rata-rata jumlah transaksi per customer"
        )
    
    with col3:
        metric_card(
            "Average Monetary",
            f"${rfm['Monetary'].mean():.2f}",
            "Rata-rata nilai pembelian per customer"
        )
    
    # RFM Score Table
    st.markdown("### 📊 Tabel RFM Score")
    
    def style_rfm_scores(val):
        if isinstance(val, (int, float)):
            if val >= 10:
                return 'background-color: #00ff0020'
            elif val >= 7:
                return 'background-color: #ffff0020'
            else:
                return 'background-color: #ff000020'
        return ''
    
    st.dataframe(
        rfm.style
        .format({
            'Recency': '{:.0f}',
            'Frequency': '{:.0f}',
            'Monetary': '${:,.2f}',
            'RFM_Score': '{:.0f}'
        })
        .applymap(style_rfm_scores, subset=['RFM_Score'])
    )
    
    # Visualisasi
    st.markdown("### 📈 Distribusi RFM Score")
    
    chart_data = pd.DataFrame({
        'RFM Score': rfm['RFM_Score'].values,
        'Count': 1
    }).groupby('RFM Score').count().reset_index()
    
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('RFM Score:Q', bin=False, title='RFM Score'),
        y=alt.Y('Count:Q', title='Number of Customers'),
        color=alt.Color('RFM Score:Q', scale=alt.Scale(scheme='viridis'))
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)
    
    # Insights
    st.markdown("### 🎯 Key Insights")
    total_customers = len(rfm)
    loyal_customers = len(rfm[rfm['RFM_Score'] >= 9])
    loyal_percentage = (loyal_customers / total_customers) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        metric_card(
            "Total Customers",
            f"{total_customers:,}",
            None
        )
    
    with col2:
        metric_card(
            "Loyal Customers (RFM Score ≥ 9)",
            f"{loyal_customers:,} ({loyal_percentage:.1f}%)",
            None
        )
    
    return rfm

