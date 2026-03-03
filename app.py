import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

# --- 1. PAGE SETUP & MEMORY ---
st.set_page_config(page_title="Dixit Investment Group | Pro Terminal", layout="wide", initial_sidebar_state="collapsed")

if 'current_view' not in st.session_state: st.session_state.current_view = "HOME"
if 'portfolio' not in st.session_state: st.session_state.portfolio = pd.DataFrame(columns=["Ticker", "Buy Price", "Quantity"])

# --- PROFESSIONAL CSS ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1300px; }
    .main-title { text-align: center; color: #1E88E5; font-size: 3.2rem; font-weight: 800; margin-bottom: 0px; }
    .sub-tagline { text-align: center; color: #555; font-size: 1.1rem; font-weight: 500; margin-top: 5px; margin-bottom: 30px; }
    div[data-testid="stButton"] button { white-space: nowrap !important; border-radius: 8px !important; }
    th { text-align: left !important; background-color: rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# --- FORMATTING HELPERS ---
def format_inr(number):
    if pd.isna(number) or number is None: return "N/A"
    try:
        s, *d = str(round(float(number), 2)).partition(".")
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d) if r else s
    except: return str(number)

def format_df_to_crores(df):
    if df is None or df.empty: return df
    formatted = df.copy()
    for col in formatted.columns:
        formatted[col] = pd.to_numeric(formatted[col], errors='coerce')
        formatted[col] = formatted[col].apply(lambda x: f"{format_inr(x / 10000000)}" if pd.notna(x) else "N/A")
    return formatted

# --- 2. LIVE INDEX BAR (Top Pulse) ---
@st.cache_data(ttl=300)
def get_index_data():
    indices = {"SENSEX": "^BSESN", "NIFTY 50": "^NSEI", "BANKNIFTY": "^NSEBANK"}
    res = {}
    for name, tick in indices.items():
        try:
            d = yf.Ticker(tick).history(period="2d")
            curr, prev = d['Close'].iloc[-1], d['Close'].iloc[-2]
            res[name] = {"price": curr, "chg": curr - prev, "pct": ((curr - prev)/prev)*100}
        except: pass
    return res

idx = get_index_data()
if idx:
    icols = st.columns(len(idx) + 2)
    for i, (name, val) in enumerate(idx.items()):
        color = "green" if val['chg'] >= 0 else "red"
        icols[i+1].markdown(f"**{name}**<br>₹{format_inr(val['price'])} <span style='color:{color};'>({val['pct']:.2f}%)</span>", unsafe_allow_html=True)
st.divider()

# --- 3. SIDEBAR & NAVIGATION ---
TOP_STOCKS = {"RELIANCE.NS": "Reliance", "TCS.NS": "TCS", "HDFCBANK.NS": "HDFC Bank", "INFY.NS": "Infosys", "ZOMATO.NS": "Zomato", "ITC.NS": "ITC"}

st.sidebar.markdown("<h3 style='color:#1E88E5;'>DIG Menu</h3>", unsafe_allow_html=True)
if st.sidebar.button("🏠 Home Dashboard", use_container_width=True): st.session_state.current_view = "HOME"; st.rerun()
if st.sidebar.button("⚖️ Peer Comparison", use_container_width=True): st.session_state.current_view = "COMPARE"; st.rerun()

# --- 4. HOME PAGE ---
if st.session_state.current_view == "HOME":
    st.markdown('<h1 class="main-title">Dixit Investment Group</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-tagline">(A Premium Wealth and Portfolio Management Company)</p>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        search = st.text_input("Search Company", placeholder="Type Symbol (e.g. TCS)...", label_visibility="collapsed")
        if st.button("Run Audit", type="primary", use_container_width=True) and search:
            st.session_state.current_view = search.upper() if search.upper().endswith(".NS") else f"{search.upper()}.NS"
            st.rerun()
        
        st.markdown("<p style='text-align:center;'><b>Trending:</b></p>", unsafe_allow_html=True)
        t_cols = st.columns(len(TOP_STOCKS))
        for i, (tick, name) in enumerate(TOP_STOCKS.items()):
            if t_cols[i].button(name): st.session_state.current_view = tick; st.rerun()

    st.divider()
    
    ht1, ht2 = st.tabs(["💰 SIP Wealth Calculator", "💼 My Virtual Portfolio"])
    with ht1:
        cc1, cc2 = st.columns([1, 2])
        sip = cc1.number_input("Monthly SIP (₹)", 500, 1000000, 5000, 500)
        yrs = cc1.slider("Years", 1, 30, 10)
        rate = cc1.slider("Exp. Returns (%)", 5, 25, 12)
        m_r = rate/12/100
        m_d = yrs*12
        fv = sip * (((1 + m_r)**m_d - 1) / m_r) * (1 + m_r)
        cc2.success(f"### Estimated Wealth: ₹{format_inr(round(fv, 0))}")
        cc2.metric("Total Invested", f"₹{format_inr(sip*m_d)}")
        cc2.metric("Wealth Gained", f"₹{format_inr(round(fv - (sip*m_d), 0))}")

    with ht2:
        st.markdown("### Portfolio Tracking")
        pc1, pc2, pc3, pc4 = st.columns(4)
        pt = pc1.selectbox("Asset", list(TOP_STOCKS.keys()))
        pq = pc2.number_input("Qty", 1, 10000, 10)
        pb = pc3.number_input("Buy Price", 1.0, 100000.0, 100.0)
        if pc4.button("➕ Add Trade", use_container_width=True):
            st.session_state.portfolio = pd.concat([st.session_state.portfolio, pd.DataFrame({"Ticker": [pt], "Buy Price": [pb], "Quantity": [pq]})], ignore_index=True)
            st.rerun()
        st.dataframe(st.session_state.portfolio, use_container_width=True)

# --- 5. STOCK ANALYSIS ENGINE ---
elif st.session_state.current_view == "COMPARE":
    st.header("⚖️ Peer Comparison Engine")
    if st.button("⬅️ Back"): st.session_state.current_view = "HOME"; st.rerun()
else:
    ticker = st.session_state.current_view
    if st.button("⬅️ Back to Search"): st.session_state.current_view = "HOME"; st.rerun()
    
    s_obj = yf.Ticker(ticker)
    info = s_obj.info
    hist = s_obj.history(period="1y")
    
    if not hist.empty:
        st.markdown(f"<h3 style='color:#1E88E5; margin-bottom:0px;'>Dixit Investment Group</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns([3, 1])
        c1.markdown(f"# {info.get('shortName', ticker)}")
        curr_p = hist['Close'].iloc[-1]
        c2.metric("Price", f"₹{format_inr(curr_p)}", f"{curr_p - hist['Close'].iloc[-2]:.2f}")

        # Super Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Technicals", "📋 Ratios", "📑 Financials (Cr)", "📰 News", "💎 AI Quant"])
        
        with tab1:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(template="plotly_white", xaxis_rangeslider_visible=False, height=500)
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            st.markdown("### Core Audit Ratios")
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("P/E Ratio", round(info.get('trailingPE', 0), 2))
            m2.metric("P/B Ratio", round(info.get('priceToBook', 0), 2))
            m3.metric("ROE (%)", f"{round(info.get('returnOnEquity', 0)*100, 2)}%")
            m4.metric("Debt/Equity", round(info.get('debtToEquity', 0), 2))
            st.metric("Market Cap (Cr)", f"₹{format_inr(round(info.get('marketCap', 0)/10000000, 2))} Cr")

        with tab3:
            st.markdown("### 📑 Annual P&L (In Crores)")
            st.dataframe(format_df_to_crores(s_obj.financials), use_container_width=True)
            st.markdown("### 📑 Balance Sheet (In Crores)")
            st.dataframe(format_df_to_crores(s_obj.balance_sheet), use_container_width=True)

        with tab4:
            st.markdown("### 📰 Live News Feed")
            for n in s_obj.news[:4]:
                st.markdown(f"🔹 **[{n['title']}]({n['link']})**")
                st.caption(f"Source: {n['publisher']}")

        with tab5:
            entered_code = st.text_input("🔑 Premium Access Code:", type="password")
            if entered_code == "AMANPRO":
                st.success("🔓 Algorithm Running...")
                pe = info.get('trailingPE', 0)
                if pe < 20: st.success("Verdict: STRONG BUY (Undervalued)")
                else: st.warning("Verdict: CAUTION (Overpriced)")
