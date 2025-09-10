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

def optimize_basket_data(df_filtered, item_stats):
    """Optimize data for market basket analysis to reduce memory usage."""
    # Ambil hanya top 100 produk berdasarkan frekuensi transaksi
    top_products = item_stats.nlargest(100, 'Transaction_Count').index
    
    # Filter transaksi untuk hanya menggunakan top products
    df_filtered = df_filtered[df_filtered['Description'].isin(top_products)]
    
    # Ambil sample dari transaksi terbaru jika data terlalu besar
    if df_filtered['InvoiceNo'].nunique() > 5000:
        recent_transactions = df_filtered['InvoiceNo'].unique()[-5000:]  # Ambil 5000 transaksi terakhir
        df_filtered = df_filtered[df_filtered['InvoiceNo'].isin(recent_transactions)]
    
    return df_filtered

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
    st.warning("⚠️ Analisis dibatasi pada 100 produk teratas dan 5000 transaksi terakhir untuk efisiensi memori")
    
    # Optimize data untuk market basket analysis
    df_optimized = optimize_basket_data(df_filtered, item_stats)
    
    # Create basket matrix
    basket = pd.crosstab(index=df_optimized['InvoiceNo'], columns=df_optimized['Description'])
    basket_encoded = (basket > 0).astype(int)
    
    try:
        # Generate frequent itemsets dengan support yang lebih tinggi
        freq_items = apriori(basket_encoded, min_support=0.02, use_colnames=True)
        
        if not freq_items.empty:
            rules = association_rules(freq_items, metric="lift", min_threshold=1)
            rules = rules.sort_values("lift", ascending=False)
            
            # Format rules untuk tampilan yang lebih sederhana
            formatted_rules = []
            for _, row in rules.head(10).iterrows():
                formatted_rules.append({
                    'Products Bought': ', '.join(list(row['antecedents'])),
                    'Leads to Buying': ', '.join(list(row['consequents'])),
                    'Support': f"{row['support']*100:.1f}%",
                    'Confidence': f"{row['confidence']*100:.1f}%",
                    'Lift': f"{row['lift']:.2f}"
                })
            
            rules_formatted = pd.DataFrame(formatted_rules)
            
            # Tampilkan dataframe tanpa styling khusus
            st.dataframe(rules_formatted, use_container_width=True)
            
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
            
    except Exception as e:
        st.error(f"Error dalam analisis: {str(e)}")
        st.info("Coba kurangi jumlah data atau tingkatkan minimum support untuk mengurangi penggunaan memori.")