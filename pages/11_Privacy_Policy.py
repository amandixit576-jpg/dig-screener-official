import streamlit as st

st.set_page_config(page_title="Privacy Policy | DIG", page_icon="⚜️", layout="wide")

# --- HIDE SIDEBAR MENU HACK ---
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Privacy Policy</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Your data security is our top priority.</p>", unsafe_allow_html=True)
st.write("---")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("### 1. Information We Collect")
    st.write("At Dixit Investment Group (DIG), we believe in minimal data tracking. We only collect essential information required to provide you with a seamless experience. This includes basic account details (if you sign up for Premium) and anonymous usage analytics.")
    
    st.markdown("### 2. How We Use Your Data")
    st.write("Your data is strictly used to improve our screener's performance and personalize your dashboard. **We do not sell, rent, or trade your personal information to any third parties.**")
    
    st.markdown("### 3. Financial Privacy")
    st.success("DIG Terminal **DOES NOT** ask for, collect, or store your Demat account passwords, broker login details, or bank account numbers. We are a screener, not a broker.")
    
    st.markdown("### 4. Third-Party APIs")
    st.write("We use Yahoo Finance and other institutional APIs to fetch stock data. Your search queries may be processed through these APIs to retrieve the requested financial numbers.")
    
    st.markdown("### 5. Updates to this Policy")
    st.write("We may update this policy periodically to comply with legal standards. Continued use of DIG Screener implies your acceptance of the revised terms.")
    
    st.write("---")
    st.caption("Last Updated: March 2026")
