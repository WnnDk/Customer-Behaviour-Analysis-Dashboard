"""Download section component for the dashboard."""
import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import numpy as np

def generate_sample_data(num_records=1000):
    """Generate sample e-commerce transaction data."""
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate dates
    end_date = datetime(2023, 12, 31)
    start_date = end_date - timedelta(days=365)
    dates = [start_date + timedelta(
        days=np.random.randint(0, 365),
        hours=np.random.randint(0, 24),
        minutes=np.random.randint(0, 60)
    ) for _ in range(num_records)]
    
    # Sample products
    products = [
        ("PRD001", "Coffee Mug", 15.99),
        ("PRD002", "Laptop Sleeve", 25.99),
        ("PRD003", "Water Bottle", 12.99),
        ("PRD004", "Notebook Set", 9.99),
        ("PRD005", "Phone Charger", 19.99),
        ("PRD006", "Desk Lamp", 29.99),
        ("PRD007", "Mouse Pad", 7.99),
        ("PRD008", "Backpack", 45.99),
        ("PRD009", "Wireless Mouse", 34.99),
        ("PRD010", "Keyboard", 59.99)
    ]
    
    # Generate customer IDs
    customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, 201)]
    
    # Generate countries
    countries = ["USA", "UK", "Canada", "Australia", "Germany", "France", "Spain", "Italy"]
    
    # Create the data
    data = []
    for _ in range(num_records):
        product = products[np.random.randint(0, len(products))]
        quantity = np.random.randint(1, 6)
        
        data.append({
            'InvoiceNo': f"INV{str(np.random.randint(10000, 99999))}",
            'StockCode': product[0],
            'Description': product[1],
            'Quantity': quantity,
            'InvoiceDate': dates[_],
            'UnitPrice': product[2],
            'CustomerID': np.random.choice(customer_ids),
            'Country': np.random.choice(countries)
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    return df

def display_download_section():
    """Display the download section with sample data option."""
    st.markdown("### 📥 Download Sample Data")
    
    with st.expander("ℹ️ About Sample Data"):
        st.markdown("""
        If you don't have your own dataset, you can download our sample e-commerce transaction data.
        
        The sample data includes:
        - 1,000 transaction records
        - 10 different products
        - 200 unique customers
        - 8 countries
        - 1 year of transaction history
        
        The data format matches what's required for the analysis:
        - InvoiceNo: Unique transaction ID
        - StockCode: Product code
        - Description: Product name
        - Quantity: Number of units purchased
        - InvoiceDate: Date and time of purchase
        - UnitPrice: Price per unit
        - CustomerID: Unique customer identifier
        - Country: Country where the purchase was made
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div style='background-color: #2D2D2D; padding: 15px; border-radius: 10px; margin: 10px 0;'>
            <h4 style='color: #00ff00; margin: 0;'>🎯 Perfect for Testing</h4>
            <p style='color: #FFFFFF; margin: 10px 0 0 0;'>
                This sample dataset is designed to demonstrate all features of the dashboard:
                - RFM Analysis
                - Churn Analysis
                - Market Basket Analysis
                - Customer Lifetime Value
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Generate & Download Sample", type="primary"):
            # Generate sample data
            df = generate_sample_data()
            
            # Convert to CSV
            csv = df.to_csv(index=False)
            
            # Create download button
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"ecommerce_sample_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Show preview
            st.markdown("#### 👀 Preview of Sample Data")
            st.dataframe(df.head(), use_container_width=True)
