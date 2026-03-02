import streamlit as st
import yfinance as yf

# Website ka mast sa UI setup
st.set_page_config(page_title="Smart Portfolio", layout="centered")
st.title("📊 Smart Portfolio Matchmaker")
st.write("Apni requirement batao, hum live market se best option nikalenge!")

# User Inputs (Sidebar me)
st.sidebar.header("User Profile")
risk = st.sidebar.selectbox("Risk Appetite", ["Low (Safe)", "Medium (Balanced)", "High (Aggressive)"])
horizon = st.sidebar.selectbox("Investment Horizon", ["< 1 Year", "1 - 5 Years", "5+ Years"])

st.write("---")
st.subheader("🤖 AI Recommendation")

# Tumhara CA-Level Logic
ticker = ""
if risk == "Low (Safe)":
    ticker = "LIQUIDBEES.NS"
    st.success("Goal: Capital Protection. Recommendation: Liquid ETFs.")
elif risk == "Medium (Balanced)":
    ticker = "NIFTYBEES.NS"
    st.info("Goal: Market Returns. Recommendation: Nifty 50 Index ETF.")
else:
    ticker = "RELIANCE.NS" # Yahan hum aage chalkar aur stocks daalenge
    st.warning("Goal: Wealth Creation. Recommendation: Bluechip/Growth Stocks.")

# Live Data dikhane ka button
if st.button(f"Fetch Live Data for {ticker}"):
    with st.spinner("Market se data fetch ho raha hai..."):
        # Pichle 1 mahine ka data
        stock_data = yf.Ticker(ticker)
        history = stock_data.history(period="1mo")
        
        current_price = history['Close'].iloc[-1]
        prev_price = history['Close'].iloc[-2]
        change = current_price - prev_price
        
        # Premium Metric Display
        st.metric(label=f"{ticker} (Current Price)", 
                  value=f"₹{current_price:.2f}", 
                  delta=f"₹{change:.2f}")
        
        # Interactive Chart
        st.write("**Past 1 Month Trend:**")
        st.line_chart(history['Close'])