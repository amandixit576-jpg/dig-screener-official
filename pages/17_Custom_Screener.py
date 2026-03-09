import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Custom Screener | DIG", page_icon="🎛️", layout="wide")

st.write("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='color: #1E88E5;'>🎛️ Institutional Stock Screener</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888;'>Filter fundamentally strong companies based on your own custom valuation and growth metrics.</p>", unsafe_allow_html=True)
st.write("---")

# --- FAST DATA CACHING (Taki website crash na ho) ---
@st.cache_data(ttl=3600)
def load_screener_data():
    # NIFTY Top 20 stocks for lightning-fast screening (Aap isme aur add kar sakte ho baad mein)
    tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", 
               "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "BAJFINANCE.NS", "L&T.NS",
               "HINDUNILVR.NS", "AXISBANK.NS", "KOTAKBANK.NS", "LT.NS", "ASIANPAINT.NS",
               "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "TATASTEEL.NS", "ZOMATO.NS"]
    
    data = []
    for t in tickers:
        try:
            info = yf.Ticker(t).info
            if 'shortName' in info:
                data.append({
                    "Company": info.get('shortName', t),
                    "Symbol": t.replace('.NS', ''),
                    "Sector": info.get('sector', 'N/A'),
                    "Current Price (₹)": round(info.get('currentPrice', 0), 2),
                    "Market Cap (₹ Cr)": round(info.get('marketCap', 0) / 10000000, 2),
                    "P/E Ratio": round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else 0,
                    "ROE (%)": round(info.get('returnOnEquity', 0) * 100, 2) if info.get('returnOnEquity') else 0,
                    "Debt to Equity": round(info.get('debtToEquity', 0), 2) if info.get('debtToEquity') else 0,
                    "Div Yield (%)": round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0
                })
        except:
            continue
    return pd.DataFrame(data)

# --- SCREENER UI & FILTERS ---
df = load_screener_data()

st.sidebar.markdown("### ⚙️ Adjust Screener Parameters")

# Sliders for filtering
min_mcap = st.sidebar.number_input("Min Market Cap (₹ Cr)", value=10000, step=5000)
max_pe = st.sidebar.slider("Maximum P/E Ratio", min_value=0, max_value=150, value=50, step=1)
min_roe = st.sidebar.slider("Minimum ROE (%)", min_value=-20, max_value=50, value=12, step=1)
max_debt = st.sidebar.slider("Max Debt to Equity", min_value=0.0, max_value=5.0, value=1.5, step=0.1)

st.sidebar.write("---")
if st.sidebar.button("🔄 Reset Filters", type="primary"):
    st.rerun()

# --- FILTERING LOGIC ---
if not df.empty:
    filtered_df = df[
        (df['Market Cap (₹ Cr)'] >= min_mcap) &
        (df['P/E Ratio'] <= max_pe) &
        (df['P/E Ratio'] > 0) & # Ignore negative P/E
        (df['ROE (%)'] >= min_roe) &
        (df['Debt to Equity'] <= max_debt)
    ]
    
    # --- DISPLAY RESULTS ---
    st.markdown(f"### 🎯 Found **{len(filtered_df)}** stocks matching your criteria")
    
    if len(filtered_df) > 0:
        st.dataframe(filtered_df.set_index("Company"), use_container_width=True, height=400)
        st.success("Tip: You can click on the column headers to sort the data (e.g., Highest ROE to lowest).")
    else:
        st.warning("No stocks found matching these strict criteria. Try relaxing your filters in the sidebar.")
else:
    st.error("Engine loading failed. Please refresh.")
