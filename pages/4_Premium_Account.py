import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from streamlit_supabase_auth import login_form
from services.stock_data import fetch_stock_history
from utils.formatters import format_inr

# Setup
st.set_page_config(page_title="Premium Portal | DIG", page_icon="🔒", layout="wide")

# Initialize memory (Taaki agar koi seedha is page pe aaye toh error na ho)
if 'portfolio' not in st.session_state: 
    st.session_state.portfolio = pd.DataFrame(columns=["Ticker", "Buy Price", "Quantity", "Hold Type"])
if 'watchlist' not in st.session_state: 
    st.session_state.watchlist = ["RELIANCE.NS", "TCS.NS"]

st.markdown("<h2 style='color:#00E570;'>🔒 Client Portal</h2>", unsafe_allow_html=True)
st.write("---")

# Supabase Authentication
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

session = login_form(url=SUPABASE_URL, apiKey=SUPABASE_KEY, providers=["google"])

if not session:
    st.warning("👈 Please sign in with Google to access your premium dashboard and saved portfolios.")
    st.stop() # Ye function code ko yahin rok deta hai agar user logged in nahi hai

st.success(f"Welcome back to the Premium Terminal, {session['user']['email']}!")
st.write("---")

# 🔥 THE TRIPLE PREMIUM TABS 🔥
ptab1, ptab2, ptab3 = st.tabs(["⭐ Live Watchlist", "📊 Asset Allocation Radar", "🧠 Tax-Loss Harvesting Engine"])

# --- 1. PREMIUM WATCHLIST ---
with ptab1:
    st.markdown("### ⭐ Real-Time Watchlist")
    w_col1, w_col2 = st.columns([3, 1])
    with w_col1: 
        new_w = st.text_input("Add Asset to Watchlist", placeholder="e.g. ITC.NS", label_visibility="collapsed")
    with w_col2:
        if st.button("➕ Add Asset", use_container_width=True) and new_w:
            if new_w.upper() not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_w.upper())
                st.success(f"{new_w.upper()} Added!")
                st.rerun()
                
    if st.session_state.watchlist:
        w_data = []
        with st.spinner("Fetching Live Prices..."):
            for t in st.session_state.watchlist:
                hist = fetch_stock_history(t, "2d")
                if not hist.empty and len(hist) >= 2:
                    cp, pp = hist['Close'].iloc[-1], hist['Close'].iloc[-2]
                    chg, pct = cp - pp, ((cp - pp)/pp)*100
                    trend = "🟢" if chg >= 0 else "🔴"
                    w_data.append({"Asset": t.replace('.NS',''), "Live Price (₹)": round(cp, 2), "Day Change": f"{trend} {round(chg,2)} ({round(pct,2)}%)"})
        
        if w_data:
            st.dataframe(pd.DataFrame(w_data), use_container_width=True, hide_index=True)
            if st.button("🗑️ Clear Watchlist"): 
                st.session_state.watchlist = []
                st.rerun()

# --- 2. ASSET ALLOCATION RADAR ---
with ptab2:
    st.markdown("### 📊 Portfolio Diversification Radar")
    if not st.session_state.portfolio.empty:
        df_port = st.session_state.portfolio.copy()
        df_port["Live Price"] = [fetch_stock_history(t, "1d")['Close'].iloc[-1] if not fetch_stock_history(t, "1d").empty else 0 for t in df_port["Ticker"]]
        df_port["Current Value"] = df_port["Live Price"] * df_port["Quantity"]
        
        alloc = df_port.groupby("Ticker")["Current Value"].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(labels=alloc['Ticker'].str.replace('.NS',''), values=alloc['Current Value'], hole=.5, 
                                     marker=dict(colors=['#00E570', '#1F2937', '#9CA3AF', '#374151']))])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=10, r=10), showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Visual representation of your capital exposure across different assets.")
    else:
        st.info("Your virtual portfolio is empty. Add trades from the 'My Virtual Portfolio' tab on the Home page.")

# --- 3. TAX-LOSS HARVESTING ENGINE ---
with ptab3:
    st.markdown("### 🧠 AI Tax-Loss Harvesting Engine")
    st.caption("Identify underperforming assets to offset your Short-Term Capital Gains (STCG) tax liability legally.")
    if not st.session_state.portfolio.empty:
        df_port = st.session_state.portfolio.copy()
        df_port["Live Price"] = [fetch_stock_history(t, "1d")['Close'].iloc[-1] if not fetch_stock_history(t, "1d").empty else 0 for t in df_port["Ticker"]]
        df_port["Gross P&L"] = (df_port["Live Price"] - df_port["Buy Price"]) * df_port["Quantity"]
        
        harvest_df = df_port[(df_port["Gross P&L"] < 0) & (df_port["Hold Type"] == "Short-Term (< 1 Yr)")].copy()
        
        if not harvest_df.empty:
            st.error(f"🚨 Found {len(harvest_df)} harvestable short-term loss opportunities!")
            total_loss = abs(harvest_df["Gross P&L"].sum())
            tax_saved = total_loss * 0.20 
            
            hc1, hc2 = st.columns(2)
            hc1.metric("Total Unrealized ST Loss", f"₹{format_inr(round(total_loss, 2))}")
            hc2.metric("✨ Est. STCG Tax Savings", f"₹{format_inr(round(tax_saved, 2))}", "Actionable")
            
            show_df = harvest_df[["Ticker", "Buy Price", "Live Price", "Gross P&L"]].copy()
            show_df["Gross P&L"] = show_df["Gross P&L"].apply(lambda x: f"₹{round(x, 2)}")
            st.table(show_df)
            
            st.write("**Pro Strategy:** By booking these short-term losses before March 31st, you can legally offset them against your short-term profits, effectively saving a flat 20% tax on that capital. You can reinvest the capital into similar fundamental assets to maintain market exposure.")
        else:
            st.success("✅ No short-term losses found! Your portfolio is either purely in profit, or you only hold long-term positions.")
    else:
        st.info("Add trades to your Virtual Portfolio to analyze tax harvesting opportunities.")
