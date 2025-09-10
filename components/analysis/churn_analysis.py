"""Churn Analysis component."""

import streamlit as st
import pandas as pd
import altair as alt
from ..metrics_card import metric_card

def calculate_churn(df: pd.DataFrame, churn_days: int = 90):
    """Calculate churn metrics."""
    # Calculate last purchase date
    last_purchase = df.groupby('CustomerID')['InvoiceDate'].max().reset_index()
    last_purchase.columns = ['CustomerID', 'LastPurchaseDate']
    
    # Reference date = last transaction date in dataset
    reference_date = df['InvoiceDate'].max()
    
    # Calculate days since last purchase
    last_purchase['DaysSinceLastPurchase'] = (reference_date - last_purchase['LastPurchaseDate']).dt.days
    
    # Flag churn: Not purchased in last 90 days
    last_purchase['Churned'] = last_purchase['DaysSinceLastPurchase'].apply(lambda x: 1 if x > churn_days else 0)
    
    return last_purchase

def display_churn_analysis(df: pd.DataFrame):
    """Display Churn Analysis section."""
    st.markdown("## 📉 Churn Analysis")
    
    with st.expander("ℹ️ Apa itu Churn Analysis?"):
        st.markdown("""
        **Churn Analysis** adalah analisis untuk mengidentifikasi customer yang tidak aktif (churned).
        
        Dalam analisis ini:
        - 🔴 **Churned**: Customer yang tidak berbelanja dalam 90 hari terakhir
        - 🟢 **Active**: Customer yang masih aktif berbelanja
        
        Metrics penting:
        - **Churn Rate**: Persentase customer yang churned
        - **Days Since Last Purchase**: Berapa hari sejak pembelian terakhir
        - **Customer Status**: Active atau Churned
        """)
    
    # Calculate churn metrics
    last_purchase = calculate_churn(df)
    churn_rate = last_purchase['Churned'].mean() * 100
    active_rate = 100 - churn_rate
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        metric_card(
            "Churn Rate",
            f"{churn_rate:.1f}%",
            "Persentase customer yang tidak aktif"
        )
    
    with col2:
        metric_card(
            "Retention Rate",
            f"{active_rate:.1f}%",
            "Persentase customer yang masih aktif"
        )
    
    # Customer Status Distribution
    st.markdown("### 📊 Customer Status Distribution")
    churn_counts = last_purchase['Churned'].value_counts().reset_index()
    churn_counts.columns = ['Churned', 'Count']
    churn_counts['Churned'] = churn_counts['Churned'].map({0: 'Active', 1: 'Churned'})
    churn_counts['Percent'] = (churn_counts['Count'] / churn_counts['Count'].sum()) * 100
    
    pie = alt.Chart(churn_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta('Count:Q', stack=True),
        color=alt.Color('Churned:N', 
                      scale=alt.Scale(domain=['Active', 'Churned'],
                                    range=['#00ff00', '#ff4b4b']),
                      legend=alt.Legend(title="Customer Status")),
        tooltip=[
            alt.Tooltip('Churned:N', title='Status'),
            alt.Tooltip('Count:Q', title='Count'),
            alt.Tooltip('Percent:Q', title='Percentage', format='.1f')
        ]
    ).properties(height=300)
    
    st.altair_chart(pie, use_container_width=True)
    
    # Days Since Last Purchase Distribution
    st.markdown("### 📈 Days Since Last Purchase Distribution")
    hist = alt.Chart(last_purchase).mark_bar().encode(
        x=alt.X('DaysSinceLastPurchase:Q', 
               bin=alt.Bin(maxbins=30),
               title='Days Since Last Purchase'),
        y=alt.Y('count():Q', 
               title='Number of Customers'),
        color=alt.value('#1f77b4'),
        tooltip=[
            alt.Tooltip('count():Q', title='Count'),
            alt.Tooltip('DaysSinceLastPurchase:Q', title='Days', bin=alt.Bin(maxbins=30))
        ]
    ).properties(height=300)
    
    # Add mean line
    mean_line = alt.Chart(last_purchase).mark_rule(color='red').encode(
        x='mean(DaysSinceLastPurchase):Q',
        size=alt.value(2),
        tooltip=[alt.Tooltip('mean(DaysSinceLastPurchase):Q', title='Mean Days', format='.1f')]
    )
    
    st.altair_chart(hist + mean_line, use_container_width=True)
    
    # Customer Details
    st.markdown("### 📋 Customer Details")
    last_purchase['Status'] = last_purchase['Churned'].map({0: 'Active', 1: 'Churned'})
    
    def style_status(val):
        if val == 'Active':
            return 'color: #00ff00'
        return 'color: #ff4b4b'
    
    st.dataframe(
        last_purchase.style
        .format({
            'DaysSinceLastPurchase': '{:.0f}',
            'LastPurchaseDate': lambda x: x.strftime('%Y-%m-%d')
        })
        .applymap(style_status, subset=['Status'])
    )
    
    return last_purchase

