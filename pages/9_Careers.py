import streamlit as st

st.set_page_config(page_title="Careers | DIG", page_icon="⚜️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E88E5;'>Careers at DIG</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.2rem;'>Build the future of quantitative finance with us.</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Why Join Dixit Investment Group?")
    st.write(
        "We are always on the lookout for bright minds who are passionate about the stock market, data automation, "
        "and financial engineering. At DIG, we don't just write code; we build automated financial engines that scale."
    )
    
    st.markdown("### 📌 Open Positions")
    st.error("Currently, we do not have any active openings. However, we are constantly growing!")
    
    st.write(
        "If you are an expert in **Python, Financial Auditing, or Quantitative Research**, drop your resume to our talent pool. "
        "We will reach out when the right opportunity arises."
    )
    
with col2:
    st.markdown("### 📩 Drop Your Resume")
    with st.form("resume_form"):
        st.text_input("Full Name")
        st.text_input("Email Address")
        st.text_input("LinkedIn Profile URL")
        st.text_area("Why do you want to join DIG?")
        submit = st.form_submit_button("Submit Profile", type="primary", use_container_width=True)
        if submit:
            st.success("Thanks! Your profile has been added to our talent pool.")
