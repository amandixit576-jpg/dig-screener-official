import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Peer Comparison | DIG", page_icon="⚖️", layout="wide")

st.write("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='color: #1E88E5;'>⚖️ Smart Peer Comparison Engine</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888;'>Compare fundamentally strong companies side-by-side to find the true sector leader.</p>", unsafe_allow_html=True)
st.write("---")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    stock1 = st.text_input("Enter First Company (e.g., TCS)", "TCS").upper().strip()
with col2:
    stock2 = st.text_input("Enter Second Company (e.g., INFY)", "INFY").upper().strip()

st.write("<br>", unsafe_allow_html=True)

if st.button("📊 Run Comparison Analysis", type="primary", use_container_width=True):
    with st.spinner("Crunching financial data from Yahoo Finance..."):
        
        # NS add karne ka smart function
        def get_safe_ticker(ticker):
            if not (ticker.endswith('.NS') or ticker.endswith('.BO')):
                return ticker + '.NS'
            return ticker

        s1, s2 = get_safe_ticker(stock1), get_safe_ticker(stock2)
        
        try:
            # Data Fetching
            info1 = yf.Ticker(s1).info
            info2 = yf.Ticker(s2).info
            
            # --- THE BALANCE SHEET (Data Organization) ---
            metrics = {
                "Metric": [
                    "Sector", 
                    "Market Cap (₹ Cr)", 
                    "P/E Ratio", 
                    "ROE (%)", 
                    "Debt to Equity", 
                    "Dividend Yield (%)",
                    "52-Week High"
                ],
                info1.get('shortName', s1): [
                    info1.get('sector', 'N/A'),
                    round(info1.get('marketCap', 0) / 10000000, 2) if info1.get('marketCap') else 'N/A',
                    round(info1.get('trailingPE', 0), 2) if info1.get('trailingPE') else 'N/A',
                    round(info1.get('returnOnEquity', 0) * 100, 2) if info1.get('returnOnEquity') else 'N/A',
                    round(info1.get('debtToEquity', 0), 2) if info1.get('debtToEquity') else 'N/A',
                    round(info1.get('dividendYield', 0) * 100, 2) if info1.get('dividendYield') else 'N/A',
                    info1.get('fiftyTwoWeekHigh', 'N/A')
                ],
                info2.get('shortName', s2): [
                    info2.get('sector', 'N/A'),
                    round(info2.get('marketCap', 0) / 10000000, 2) if info2.get('marketCap') else 'N/A',
                    round(info2.get('trailingPE', 0), 2) if info2.get('trailingPE') else 'N/A',
                    round(info2.get('returnOnEquity', 0) * 100, 2) if info2.get('returnOnEquity') else 'N/A',
                    round(info2.get('debtToEquity', 0), 2) if info2.get('debtToEquity') else 'N/A',
                    round(info2.get('dividendYield', 0) * 100, 2) if info2.get('dividendYield') else 'N/A',
                    info2.get('fiftyTwoWeekHigh', 'N/A')
                ]
            }
            
            df = pd.DataFrame(metrics).set_index("Metric")
            
            # --- DISPLAY THE AUDIT ---
            st.success("Comparison completed successfully!")
            st.markdown("### 📈 Fundamental Head-to-Head")
            
            # Streamlit ki mast dataframe formatting
            st.dataframe(df, use_container_width=True, height=280)
            
            st.caption("ℹ️ *Note: N/A indicates data is temporarily unavailable from the institutional feed.*")
            
        except Exception as e:
            st.error("Error fetching data. Please check the NSE symbols and try again.")
