import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Pro Terminal", layout="wide")

# --- 2. HEADER & BRANDING ---
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏢 Dixit Capital & Wealth Management</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Advanced Stock Screener & Portfolio Tracker</p><hr>", unsafe_allow_html=True)

# --- 3. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Settings")
risk = st.sidebar.selectbox("Risk Profile:", ["Conservative", "Balanced", "Aggressive"])
raw_ticker = st.sidebar.text_input("Enter NSE Stock (e.g., ZOMATO):", "RELIANCE").upper()
user_ticker = raw_ticker if raw_ticker.endswith(".NS") else f"{raw_ticker}.NS"

# --- 4. DATA ENGINE (Super Safe Mode) ---
@st.cache_data(ttl=300)
def get_data(symbol):
    try:
        return yf.Ticker(symbol).history(period="1y")
    except:
        return None

@st.cache_data(ttl=3600)
def get_info(symbol):
    try:
        return yf.Ticker(symbol).info
    except:
        return {}

@st.cache_data(ttl=1800)
def get_news(symbol):
    try:
        return yf.Ticker(symbol).news
    except:
        return []

data = get_data(user_ticker)
info = get_info(user_ticker)
news = get_news(user_ticker)

# --- 5. MAIN DASHBOARD ---
if data is not None and not data.empty:
    
    # Calculate Prices safely
    curr_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    change = curr_price - prev_price
    pct = (change / prev_price) * 100

    data['SMA50'] = data['Close'].rolling(50).mean()
    data['SMA200'] = data['Close'].rolling(200).mean()
    sma50_val = data['SMA50'].iloc[-1]
    sma200_val = data['SMA200'].iloc[-1]

    # Metrics Row
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{raw_ticker} Price", f"₹{curr_price:.2f}", f"{change:.2f} ({pct:.2f}%)")
    c2.metric("50-Day SMA", f"₹{sma50_val:.2f}" if str(sma50_val) != 'nan' else "N/A")
    c3.metric("200-Day SMA", f"₹{sma200_val:.2f}" if str(sma200_val) != 'nan' else "N/A")

    # Tabs Creation
    t1, t2, t3 = st.tabs(["📈 Technical Chart", "📋 Fundamentals", "📰 Latest News"])

    # TAB 1: Chart
    with t1:
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], line=dict(color='orange'), name='50 SMA'))
        fig.add_trace(go.Scatter(x=data.index, y=data['SMA200'], line=dict(color='blue'), name='200 SMA'))
        fig.update_layout(template="plotly_dark", margin=dict(t=20, b=20, l=10, r=10), height=550, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # TAB 2: Fundamentals
    with t2:
        if info:
            mc = info.get('marketCap', 0)
            st.write(f"**Market Cap:** ₹{mc / 10000000:.2f} Cr" if mc else "**Market Cap:** N/A")
            
            f1, f2, f3, f4 = st.columns(4)
            f1.metric("P/E Ratio", round(info.get('trailingPE', 0), 2) if info.get('trailingPE') else "N/A")
            f2.metric("ROE", f"{round(info.get('returnOnEquity', 0)*100, 2)}%" if info.get('returnOnEquity') else "N/A")
            f3.metric("Book Value", f"₹{round(info.get('bookValue', 0), 2)}" if info.get('bookValue') else "N/A")
            f4.metric("Debt/Equity", round(info.get('debtToEquity', 0), 2) if info.get('debtToEquity') else "N/A")
            
            st.write("---")
            st.write(f"**About Company:** {info.get('longBusinessSummary', 'No description.')[:500]}...")
        else:
            st.warning("⚠️ Fundamental data not available.")

    # TAB 3: News
    with t3:
        if news:
            for n in news[:5]:
                st.write(f"🔹 **[{n.get('title', 'Read News')}]({n.get('link', '#')})** - *(Source: {n.get('publisher', 'Web')})*")
                st.write("---")
        else:
            st.info("No recent news found.")

else:
    st.error("⚠️ Invalid Stock Symbol. Please check the name and try again.")
