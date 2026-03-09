import streamlit as st

st.set_page_config(page_title="Regulatory Disclaimer | DIG", page_icon="⚖️", layout="wide")

st.write("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #DC2626; font-size: 3.5rem;'>⚖️ Regulatory Disclaimer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.2rem;'>Please read this important legal information carefully before using the DIG Terminal.</p>", unsafe_allow_html=True)
st.write("<hr>", unsafe_allow_html=True)

st.markdown("""
### 1. No Investment Advice
The information, data, and charts provided on the Dixit Investment Group (DIG) Terminal are strictly for **educational, analytical, and informational purposes only**. We do not provide personalized financial, investment, or tax advice. The screening results, technical indicators, and institutional data should not be construed as a recommendation or solicitation to buy or sell any securities.

### 2. Risk of Loss
Investing in equity markets involves significant risk, including the potential loss of your entire principal. Past performance of any stock, sector, or investment strategy is not a reliable indicator of future results. Users must conduct their own independent due diligence or consult a certified financial advisor before making any financial decisions.

### 3. Data Accuracy & Third-Party Feeds
While we engineer DIG to provide institutional-grade accuracy, our platform relies on third-party APIs (such as Yahoo Finance) for live market feeds. 
* Market prices may be delayed by 15 minutes or more.
* We do not warrant or guarantee the completeness, timeliness, or absolute accuracy of the financial ratios, balance sheets, or historical data presented.

### 4. SEBI Registration Status
**DIG is currently an advanced educational and portfolio management project.** Any SEBI Registration Number (e.g., `INA000000000`) displayed on the platform is a placeholder (dummy text) used solely for UI/UX demonstration purposes. We are not a SEBI-registered Investment Advisor (RIA) or Research Analyst (RA).

### 5. Tax & Audit Estimations
The Tax Audit & SIP Goal Planner tools use generalized standard tax brackets (e.g., 20% STCG, 12.5% LTCG). These are approximate estimations and do not substitute for professional accounting, auditing, or official tax filing services.
""")

st.write("<br><br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("⬅️ I Understand - Back to Main Terminal", use_container_width=True, type="primary"):
        st.switch_page("app.py")
