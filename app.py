import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Pro Terminal | Stock Screener", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM BRANDING & HEADER ---
st.markdown("""
    <div style='text-align: center; padding: 10px;'>
        <h1 style='color: #1E88E5; font-family: "Arial Black", sans-serif;'>🏢 Dixit Capital & Wealth Management</h1>
        <p style='font-style: italic; color: #888888; font-size: 18px;'>Advanced Quantitative Analysis & Portfolio Tracking</p>
    </div>
    <hr>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTROLS ---
st.sidebar.header("⚙️ Terminal Settings")

risk_profile = st.sidebar.selectbox(
    "Client Risk Appetite:", 
    ["Conservative (Low Risk)", "Moderate (Balanced)", "Aggressive (High Risk)"]
)

benchmark_ticker = "RELIANCE.NS"
if risk_profile == "Conservative (Low Risk)":
    benchmark_ticker = "LIQUIDBEES.NS"
elif risk_profile == "Moderate (Balanced)":
    benchmark_ticker = "NIFTYBEES.NS"

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Equity Search")
# Ab user bina .NS lagaye bhi search kar sakta hai
raw_ticker = st.sidebar.text_input("Enter Company Name/Symbol:", "RELIANCE").upper()
user_ticker = raw_ticker if raw_ticker.endswith(".NS") else f"{raw_ticker}.NS"

st.sidebar.caption("Example: HDFCBANK, TCS, ZOMATO")

# --- DATA FETCHING ENGINE ---
@st.cache_data(ttl=300)
def fetch_market_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        return stock.history(period="1y")
    except:
        return None

# Naya Fundamental Engine (Din mein ek hi baar change hota hai, isliye cache zyada der tak)
@st.cache_data(ttl=3600)
def fetch_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol)
        return stock.info
    except:
        return {}

data = fetch_market_data(user_ticker)
info = fetch_fundamentals(user_ticker)

# --- MAIN DASHBOARD ---
if data is not None and not data.empty:
    
    # Calculate Key Metrics
    curr_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    price_change = curr_price - prev_price
    pct_change = (price_change / prev_price) * 100
    
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    
    # Top Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=f"{raw_ticker} - Last Traded Price", 
                  value=f"₹{curr_price:.2f}", 
                  delta=f"{price_change:.2f} ({pct_change:.2f}%)")
    with col2:
        st.metric(label="50-Day SMA", value=f"₹{data['SMA_50'].iloc[-1]:.2f}" if not data['SMA_50'].isna().iloc[-1] else "N/A")
    with col3:
        st.metric(label="200-Day SMA", value=f"₹{data['SMA_200'].iloc[-1]:.2f}" if not data['SMA_200'].isna().iloc[-1] else "N/A")
        
    # --- TICKERTAPE STYLE TABS ---
    tab1, tab2 = st.tabs(["📈 Technical Analysis", "📋 Fundamental Audit"])
    
    with tab1:
        st.markdown("### Interactive Technical Chart")
        fig = go.Figure()
        
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
            name='Market Price',
            increasing_line_color='#26A69A', decreasing_line_color='#EF5350'
        ))
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['SMA_50'],
            line=dict(color='orange', width=1.5),
            name='50-Day SMA'
        ))
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['SMA_200'],
            line=dict(color='blue', width=1.5),
            name='200-Day SMA'
        ))
        
        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=10, r=10, t=30, b=10),
            height=550,
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### Core Fundamentals & Valuation")
        if info:
            # Formatting Market Cap into Crores
            mcap = info.get('marketCap', 0)
            mcap_str = f"₹{mcap / 10000000:.2f} Cr" if mcap > 10000000 else "N/A"

            f_col1, f_col2, f_col3, f_col4 = st.columns(4)
            
            with f_col1:
                st.metric("Market Cap", mcap_str)
                st.metric("P/E Ratio", round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else "N/A")
            with f_col2:
                st.metric("ROE", f"{round(info.get('returnOnEquity', 0)*100, 2)}%" if info.get('returnOnEquity') else "N/A")
                st.metric("EPS (TTM)", f"₹{round(info.get('trailingEps', 0), 2)}" if info.get('trailingEps') else "N/A")
            with f_col3:
                st.metric("Book Value", f"₹{round(info.get('bookValue', 0), 2)}" if info.get('bookValue') else "N/A")
                st.metric("Price to Book (P/B)", round(info.get('priceToBook', 0), 2) if info.get('priceToBook') else "N/A")
            with f_col4:
                st.metric("Dividend Yield", f"{round(info.get('dividendYield', 0)*100, 2)}%" if info.get('dividendYield') else "N/A")
                st.metric("Debt to Equity", round(info.get('debtToEquity', 0), 2) if info.get('debtToEquity') else "N/A")
                
            st.write("---")
            st.markdown(f"**Business Summary:** *{info.get('longBusinessSummary', 'No description available.')[:400]}...*")
        else:
            st.warning("⚠️ Fundamental data is currently unavailable for this stock.")

    st.info(f"**System Note:** Based on the selected **{risk_profile}** profile, the recommended benchmark asset is **{benchmark_ticker}**.")

else:
    st.error("⚠️ Invalid Ticker Symbol. Please ensure you enter a valid NSE symbol (e.g., ZOMATO).")
