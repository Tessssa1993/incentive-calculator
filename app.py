import streamlit as st
import pandas as pd

# Basic Page Setup
st.set_page_config(page_title="Incentive Calc", page_icon="💰")

# --- DATA CONNECTION ---
# 1. Open your Google Sheet
# 2. File > Share > Publish to Web
# 3. Select 'Link', choose your sheet name, and 'Commas-separated values (.csv)'
# 4. Paste that link below:
SHEET_URL = "https://docs.google.com/spreadsheets/d/1y1SZUF9y7PYihbV8z4wa-bhYje_Q6tapJKqHuCSQlNw/pub?output=csv"

@st.cache_data(ttl=300) # Refresh data every 5 mins
def get_data():
    return pd.read_csv(SHEET_URL)

try:
    df = get_data()
    # Clean column names just in case
    df.columns = [c.strip() for c in df.columns]

    st.title("Business Incentive Calculator")

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Select Details")
    
    month = st.sidebar.selectbox("Month", df['Month'].unique())
    
    # Filter by Month
    df_m = df[df['Month'] == month]
    
    squad = st.sidebar.selectbox("Squad", df_m['Squad'].unique())
    
    # Filter by Squad
    df_s = df_m[df_m['Squad'] == squad]
    
    product = st.sidebar.selectbox("Product", df_s['Product'].unique())
    
    # Filter by Product
    df_p = df_s[df_s['Product'] == product]
    
    contract_type = st.sidebar.selectbox("Type", df_p['Type'].unique())
    
    # Manual Input
    actual_sales = st.sidebar.number_input("Actual Sales", min_value=0, value=0)

    # --- CALCULATION ---
    row = df_p[df_p['Type'] == contract_type]
    
    if not row.empty:
        mrr = row['MRR'].values[0]
        rate = row['Rate'].values[0]
        result = actual_sales * mrr * rate
        
        # Display Results
        st.balloons() if result > 0 else None
        st.metric("Estimated Incentive", f"${result:,.2f}")
        
        with st.expander("View Calculation Details"):
            st.write(f"**Formula:** {actual_sales} (Sales) × ${mrr} (MRR) × {rate*100}% (Rate)")
            st.write(f"**Data Source:** {month} Rate Card for {squad}")
    else:
        st.error("Matching data not found.")

except Exception as e:
    st.warning("Awaiting valid Google Sheet Connection...")
    st.info("Ensure your Google Sheet is 'Published to Web' as a CSV.")
