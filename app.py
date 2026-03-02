import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Pro Terminal | Dixit Capital", layout="wide")

# --- 2. POPUP FORM (PREMIUM SIGNUP) ---
@st.dialog("👑 Unlock Premium Features")
def premium_signup():
    st.markdown("Join **Dixit Capital Premium** for advanced CA-level audits, real-time alerts, and personalized portfolio management.")
    with st.form("premium_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone / WhatsApp Number")
        submitted = st.form_submit_button("Request Premium Access")
        if submitted:
            if name and phone:
                st.success(f"Thank you {name}! Our wealth management team will contact you shortly.")
            else:
                st.error("Please enter your name and phone number.")

# --- 3. HEADER & BRANDING ---
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>🏢 Dixit Capital & Wealth Management</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Advanced Stock Screener & Portfolio Tracker</p><hr>", unsafe_allow_html=True)

# --- 4. TOP STOCKS DICTIONARY ---
# Is list mein aap baad mein kitne bhi stocks add kar sakte hain
TOP_STOCKS = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "INFY.NS": "Infosys",
    "ZOMATO.NS": "Zomato",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel",
    "ITC.NS": "ITC Limited",
    "LT.NS": "Larsen & Toubro",
    "BAJFINANCE.NS": "Bajaj Finance",
    "TATAMOTORS.NS": "Tata Motors",
    "NTPC.NS": "NTPC Limited",
    "MARUTI.NS": "Maruti Suzuki",
    "SUNPHARMA.NS": "Sun Pharma",
    "LIQUIDBEES.NS": "Nippon India Liquid Bees",
    "NIFTYBEES.NS": "Nippon India Nifty Bees"
}

# --- 5. SIDEBAR SETTINGS ---
st.sidebar.header("⚙️ Settings")

# Premium Upgrade Button (Triggers Popup)
if st.sidebar.button("👑 Upgrade to Premium", use_container_width=True):
    premium_signup()

st.sidebar.markdown("---")
risk = st.sidebar.selectbox("Risk Profile:", ["Conservative", "Balanced", "Aggressive"])

st.sidebar.subheader("🔍 Smart Equity Search")
# SMART DROPDOWN: User type bhi kar sakta hai aur scroll bhi
selected_ticker = st.sidebar.selectbox(
    "Select or Type Company Name:",
    options=list(TOP_STOCKS.keys()),
    format_func=lambda x: f"{TOP_STOCKS[x]} ({x.replace('.NS', '')})"
)

# Agar user ko list ke bahar ka stock chahiye
manual_ticker = st.sidebar.text_input("Not in list? Type NSE symbol here:", "")
raw_ticker = manual_ticker.upper() if manual_ticker else selected_ticker
user_ticker = raw_ticker if raw_ticker.endswith(".NS") else f"{raw_ticker}.NS"


# --- 6. DATA ENGINE ---
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

# --- 7. MAIN DASHBOARD ---
if data is not None and not data.empty:
    
    curr_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    change = curr_price - prev_price
    pct = (change / prev_price) * 100

    data['SMA50'] = data['Close'].rolling(50).mean()
    data['SMA200'] = data['Close'].rolling(200).mean()
    sma50_val = data['SMA50'].iloc[-1]
    sma200_val = data['SMA200'].iloc[-1]

    # Metrics Row
    display_name = TOP_STOCKS.get(user_ticker, raw_ticker)
    c1, c2, c3 = st.columns(3)
    c1.metric(f"{display_name} Price", f"₹{curr_price:.2f}", f"{change:.2f} ({pct:.2f}%)")
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
