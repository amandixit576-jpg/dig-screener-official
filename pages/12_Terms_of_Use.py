import streamlit as st

st.set_page_config(page_title="Terms of Use | DIG", page_icon="⚜️", layout="wide")

# --- HIDE SIDEBAR MENU HACK ---
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Terms of Use</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Please read these terms carefully before using DIG Terminal.</p>", unsafe_allow_html=True)
st.write("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 1. Acceptance of Terms")
    st.write("By accessing and using digscreener.in, you accept and agree to be bound by the terms and provisions of this agreement.")
    
    st.markdown("### 2. SEBI Disclaimer (CRITICAL) 🚨")
    st.error(
        "**Dixit Investment Group (DIG) is NOT a SEBI Registered Investment Advisor.** \n\n"
        "All data, financial metrics, and quantitative ratings provided on this platform are for **Educational and Informational Purposes ONLY**. "
        "We do not provide 'Buy/Sell/Hold' recommendations. Stock market investments are subject to market risks. Please consult a qualified financial advisor or conduct your own thorough audit before investing."
    )
    
    st.markdown("### 3. Accuracy of Information")
    st.write("While we strive to provide 100% accurate institutional data via our APIs, DIG makes no warranties regarding the absolute accuracy, completeness, or reliability of the data. Delays, omissions, or inaccuracies may occur.")
    
    st.markdown("### 4. Limitation of Liability")
    st.write("Under no circumstances shall Aman Dixit, Dixit Investment Group, or its affiliates be liable for any direct, indirect, incidental, or consequential damages (including trading losses) resulting from the use or inability to use the information provided on this platform.")
    
    st.markdown("### 5. Intellectual Property")
    st.write("All custom quantitative models, UI designs, and codebase associated with the DIG Screener are the intellectual property of Dixit Investment Group.")

    st.write("---")
    st.caption("By continuing to use this website, you acknowledge that you have read and understood these terms.")
