"""Customer Lifetime Value Analysis component."""

import streamlit as st
import pandas as pd
import altair as alt
from ..metrics_card import metric_card

def calculate_clv(df: pd.DataFrame):
    """Calculate Customer Lifetime Value metrics."""
    # Calculate total amount for each transaction
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    
    # Calculate reference date
    reference_date = df['InvoiceDate'].max()
    
    # Calculate customer metrics
    customer_metrics = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - x.max()).days,  # Recency
        'InvoiceNo': 'count',  # Frequency
        'TotalAmount': 'sum'  # Monetary
    }).reset_index()
    
    customer_metrics.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    
    # Calculate CLV
    # Using a simple formula: Average Order Value * Purchase Frequency * (1 / Churn Probability)
    customer_metrics['Avg_Order_Value'] = customer_metrics['Monetary'] / customer_metrics['Frequency']
    customer_metrics['Churn_Probability'] = customer_metrics['Recency'].apply(lambda x: min(x + 1, 365)) / 365
    customer_metrics['CLV'] = customer_metrics['Avg_Order_Value'] * customer_metrics['Frequency'] * (1 / customer_metrics['Churn_Probability'])
    
    # Remove extreme outliers (clip at 95th percentile)
    customer_metrics['CLV'] = customer_metrics['CLV'].clip(0, customer_metrics['CLV'].quantile(0.95))
    
    return customer_metrics

def display_clv_analysis(df: pd.DataFrame):
    """Display Customer Lifetime Value analysis section."""
    st.markdown("## 💰 Customer Lifetime Value Analysis")
    
    with st.expander("ℹ️ Apa itu Customer Lifetime Value?"):
        st.markdown("""
        **Customer Lifetime Value (CLV)** adalah prediksi total nilai bisnis yang bisa diharapkan dari seluruh hubungan dengan seorang pelanggan.
        
        Komponen perhitungan:
        - 💵 **Average Order Value**: Rata-rata nilai pembelian per transaksi
        - 🔄 **Purchase Frequency**: Seberapa sering customer berbelanja
        - 📊 **Customer Lifespan**: Berapa lama customer akan tetap aktif
        
        Manfaat:
        - Identifikasi customer paling berharga
        - Optimasi budget marketing
        - Strategi retensi customer
        - Pengembangan produk
        """)
    
    # Calculate CLV metrics
    clv_data = calculate_clv(df)
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card(
            "Average CLV",
            f"${clv_data['CLV'].mean():.2f}",
            "Rata-rata nilai customer"
        )
    
    with col2:
        metric_card(
            "Total Revenue",
            f"${clv_data['Monetary'].sum():,.2f}",
            "Total pendapatan"
        )
    
    with col3:
        metric_card(
            "Avg Order Value",
            f"${clv_data['Avg_Order_Value'].mean():.2f}",
            "Rata-rata nilai per order"
        )
    
    # CLV Distribution
    st.markdown("### 📊 Distribusi Customer Lifetime Value")
    
    # Histogram CLV
    hist = alt.Chart(clv_data).mark_bar().encode(
        x=alt.X('CLV:Q', 
               bin=alt.Bin(maxbins=30),
               title='Customer Lifetime Value ($)'),
        y=alt.Y('count():Q', 
               title='Number of Customers'),
        color=alt.value('#1f77b4'),
        tooltip=[
            alt.Tooltip('count():Q', title='Count'),
            alt.Tooltip('CLV:Q', title='CLV', format='$.2f')
        ]
    ).properties(height=300)
    
    # Add mean line
    mean_line = alt.Chart(clv_data).mark_rule(color='red').encode(
        x='mean(CLV):Q',
        size=alt.value(2),
        tooltip=[alt.Tooltip('mean(CLV):Q', title='Mean CLV', format='$.2f')]
    )
    
    st.altair_chart(hist + mean_line, use_container_width=True)
    
    # Customer Segmentation
    st.markdown("### 👥 Customer Segmentation by CLV")
    
    # Define segments based on CLV percentiles
    clv_data['Segment'] = pd.qcut(clv_data['CLV'], 
                                q=3, 
                                labels=['Low Value', 'Medium Value', 'High Value'])
    
    segment_stats = clv_data.groupby('Segment').agg({
        'CustomerID': 'count',
        'CLV': 'mean',
        'Monetary': 'sum'
    }).reset_index()
    
    # Format the stats
    segment_stats.columns = ['Segment', 'Customer Count', 'Average CLV', 'Total Revenue']
    
    # Add color coding
    def color_segments(val):
        if val == 'Low Value':
            return 'background-color: #ff000020'
        elif val == 'Medium Value':
            return 'background-color: #ffff0020'
        else:
            return 'background-color: #00ff0020'
    
    # Display segment statistics
    st.dataframe(
        segment_stats.style
        .format({
            'Customer Count': '{:,.0f}',
            'Average CLV': '${:,.2f}',
            'Total Revenue': '${:,.2f}'
        })
        .apply(lambda x: [''] + [color_segments(x['Segment'])]*3, axis=1)
    )
    
    # Scatter plot of Frequency vs Monetary colored by CLV
    st.markdown("### 📈 Frequency vs Monetary Analysis")
    scatter = alt.Chart(clv_data).mark_circle(size=60).encode(
        x=alt.X('Frequency:Q', title='Purchase Frequency'),
        y=alt.Y('Monetary:Q', title='Total Spent ($)'),
        color=alt.Color('CLV:Q', 
                       scale=alt.Scale(scheme='viridis'),
                       title='Customer Lifetime Value'),
        tooltip=[
            alt.Tooltip('CustomerID:N', title='Customer ID'),
            alt.Tooltip('Frequency:Q', title='Purchase Frequency'),
            alt.Tooltip('Monetary:Q', title='Total Spent', format='$.2f'),
            alt.Tooltip('CLV:Q', title='CLV', format='$.2f'),
            alt.Tooltip('Segment:N', title='Segment')
        ]
    ).properties(height=400)
    
    st.altair_chart(scatter, use_container_width=True)
    
    return clv_data

