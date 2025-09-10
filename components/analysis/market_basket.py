"""Market Basket Analysis component."""

import streamlit as st
import pandas as pd
import altair as alt
from mlxtend.frequent_patterns import apriori, association_rules
from ..metrics_card import metric_card

def prepare_basket_data(df: pd.DataFrame):
    """Prepare data for market basket analysis."""
    # Filter valid transactions
    df_filtered = df[
        (df['Quantity'] > 0) &  # Only positive quantities
        (~df['InvoiceNo'].astype(str).str.contains('C', na=False))  # Exclude cancelled orders
    ].copy()
    
    # Calculate item statistics
    item_stats = df_filtered.groupby('Description').agg({
        'Quantity': ['count', 'sum'],
        'InvoiceNo': 'nunique'
    }).sort_values(('InvoiceNo', 'nunique'), ascending=False)
    
    item_stats.columns = ['Total_Units', 'Total_Quantity', 'Transaction_Count']
    return df_filtered, item_stats

def display_market_basket_analysis(df: pd.DataFrame):
    """Display Market Basket Analysis section."""
    st.markdown("## 🛍️ Market Basket Analysis")
    
    with st.expander("ℹ️ Apa itu Market Basket Analysis?"):
        st.markdown("""
        **Market Basket Analysis** adalah teknik untuk menemukan kombinasi produk yang sering dibeli bersamaan.
        
        Metrics penting:
        - 📊 **Support**: Seberapa sering kombinasi produk muncul dalam transaksi
        - 🎯 **Confidence**: Probabilitas membeli produk B jika membeli produk A
        - 📈 **Lift**: Seberapa kuat hubungan antar produk (>1 berarti ada korelasi positif)
        
        Manfaat:
        - Pengaturan tata letak toko
        - Strategi bundling produk
        - Rekomendasi produk
        - Promosi yang lebih efektif
        """)
    
    # Prepare data
    df_filtered, item_stats = prepare_basket_data(df)
    
    # Display metrics
    total_transactions = df_filtered['InvoiceNo'].nunique()
    total_products = len(df_filtered['Description'].unique())
    avg_basket_size = df_filtered.groupby('InvoiceNo')['Description'].nunique().mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card(
            "Total Transactions",
            f"{total_transactions:,}",
            "Jumlah transaksi yang dianalisis"
        )
    
    with col2:
        metric_card(
            "Unique Products",
            f"{total_products:,}",
            "Jumlah produk unik"
        )
    
    with col3:
        metric_card(
            "Avg Basket Size",
            f"{avg_basket_size:.1f}",
            "Rata-rata jumlah item per transaksi"
        )
    
    # Top Products Analysis
    st.markdown("### 🔝 Top Products Analysis")
    top_10_products = item_stats.head(10).reset_index()
    top_10_products['Transaction_Percentage'] = (top_10_products['Transaction_Count'] / total_transactions * 100)
    
    chart = alt.Chart(top_10_products).mark_bar().encode(
        x=alt.X('Transaction_Percentage:Q', title='Percentage of Transactions (%)'),
        y=alt.Y('Description:N', sort='-x', title='Product'),
        color=alt.Color('Transaction_Percentage:Q', scale=alt.Scale(scheme='viridis')),
        tooltip=[
            alt.Tooltip('Description:N', title='Product'),
            alt.Tooltip('Transaction_Count:Q', title='Number of Transactions'),
            alt.Tooltip('Transaction_Percentage:Q', title='% of Transactions', format='.1f'),
            alt.Tooltip('Total_Quantity:Q', title='Total Units Sold')
        ]
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)
    
    # Market Basket Analysis
    st.markdown("### 🔍 Association Rules Analysis")
    st.warning("⚠️ Analisis dibatasi pada produk yang muncul di minimal 50 transaksi untuk efisiensi")
    
    # Filter frequent items and create basket
    frequent_items = item_stats[item_stats['Transaction_Count'] >= 50].index
    df_filtered = df_filtered[df_filtered['Description'].isin(frequent_items)]
    
    basket = pd.crosstab(index=df_filtered['InvoiceNo'], columns=df_filtered['Description'])
    basket_encoded = (basket > 0).astype(int)
    
    # Generate frequent itemsets and rules
    freq_items = apriori(basket_encoded, min_support=0.03, use_colnames=True)
    
    if not freq_items.empty:
        rules = association_rules(freq_items, metric="lift", min_threshold=1)
        rules = rules.sort_values("lift", ascending=False)
        
            # Format rules untuk tampilan
            formatted_rules = []
            for _, row in rules.head(10).iterrows():
                formatted_rules.append({
                    'Products Bought': ', '.join(list(row['antecedents'])),
                    'Leads to Buying': ', '.join(list(row['consequents'])),
                    'Support (%)': f"{row['support']*100:.1f}%",
                    'Confidence (%)': f"{row['confidence']*100:.1f}%",
                    'Lift Value': row['lift'],  # Simpan nilai numerik
                    'Lift': f"{row['lift']:.2f}"  # Format untuk display
                })
            
            rules_formatted = pd.DataFrame(formatted_rules)
            
            # Styling berdasarkan nilai Lift numerik
            def style_lift(val):
                try:
                    lift = float(val)
                    if lift > 2:
                        return 'color: #00ff00'
                    elif lift > 1:
                        return 'color: #ffff00'
                    return 'color: #ff4b4b'
                except:
                    return ''
            
            # Tampilkan dataframe dengan styling
            st.dataframe(
                rules_formatted.style.applymap(style_lift, subset=['Lift Value']).hide_columns(['Lift Value']),
                use_container_width=True
            )
        
        # Visualization
        scatter = alt.Chart(rules).mark_circle(size=60).encode(
            x=alt.X('confidence:Q', 
                   title='Confidence',
                   axis=alt.Axis(format='%')),
            y=alt.Y('lift:Q',
                   title='Lift'),
            color=alt.Color('support:Q',
                          title='Support',
                          scale=alt.Scale(scheme='viridis')),
            tooltip=[
                alt.Tooltip('antecedents:N', title='If Purchase'),
                alt.Tooltip('consequents:N', title='Then Likely to Purchase'),
                alt.Tooltip('support:Q', title='Support', format='.1%'),
                alt.Tooltip('confidence:Q', title='Confidence', format='.1%'),
                alt.Tooltip('lift:Q', title='Lift', format='.2f')
            ]
        ).properties(height=400)
        
        st.altair_chart(scatter, use_container_width=True)
        
        # Insights
        st.markdown("### 🎯 Key Insights")
        strong_associations = len(rules[rules['lift'] > 2])
        avg_lift = rules['lift'].mean()
        max_confidence = rules['confidence'].max() * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card(
                "Strong Associations",
                f"{strong_associations}",
                "Produk dengan Lift > 2"
            )
        
        with col2:
            metric_card(
                "Average Lift",
                f"{avg_lift:.2f}",
                "Rata-rata kekuatan asosiasi"
            )
        
        with col3:
            metric_card(
                "Max Confidence",
                f"{max_confidence:.1f}%",
                "Probabilitas tertinggi"
            )
    else:
        st.error("Tidak cukup data untuk menghasilkan association rules. Coba kurangi minimum support.")

