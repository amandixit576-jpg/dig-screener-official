import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Intrinsic Value Calculator | DIG", page_icon="🧮", layout="wide")

st.write("<br>", unsafe_allow_html=True)
st.markdown("<h1 style='color: #1E88E5;'>🧮 DCF Intrinsic Value Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #888;'>Estimate the 'Fair Value' of a stock by projecting its future earnings and discounting them back to the present value.</p>", unsafe_allow_html=True)
st.write("---")

# --- INPUT SECTION ---
st.markdown("### 📊 Enter Financial Assumptions")
c1, c2, c3 = st.columns(3)

with c1:
    company = st.text_input("Company Name / Symbol", "ITC")
    eps = st.number_input("Current EPS (₹)", value=15.5, step=1.0)
    
with c2:
    growth_rate = st.number_input("Expected Growth Rate (%) [Years 1-5]", value=12.0, step=1.0)
    terminal_rate = st.number_input("Terminal Growth Rate (%) [After Year 5]", value=4.0, step=0.5)

with c3:
    discount_rate = st.number_input("Discount Rate / WACC (%)", value=12.0, step=1.0)
    margin_safety = st.number_input("Margin of Safety (%)", value=20.0, step=5.0)

st.write("<br>", unsafe_allow_html=True)

if st.button("Calculate True Value 🎯", type="primary", use_container_width=True):
    with st.spinner("Calculating Present Value of Future Cash Flows..."):
        
        # --- DCF CALCULATION ENGINE ---
        years = 5
        g = growth_rate / 100
        tg = terminal_rate / 100
        r = discount_rate / 100
        ms = margin_safety / 100
        
        # Calculate projected EPS and Present Value (PV)
        future_eps = []
        pv_eps = []
        current_eps = eps
        
        for year in range(1, years + 1):
            current_eps = current_eps * (1 + g)
            future_eps.append(current_eps)
            pv = current_eps / ((1 + r) ** year)
            pv_eps.append(pv)
            
        # Terminal Value calculation (Gordon Growth Model)
        terminal_value = (future_eps[-1] * (1 + tg)) / (r - tg)
        pv_terminal_value = terminal_value / ((1 + r) ** years)
        
        # Total Intrinsic Value
        intrinsic_value = sum(pv_eps) + pv_terminal_value
        buy_price = intrinsic_value * (1 - ms)
        
        # --- DISPLAY RESULTS ---
        st.success(f"Valuation Audit Complete for {company.upper()}")
        
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            st.markdown(f"""
            <div style='background-color: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid #1E88E5;'>
                <h4 style='color: #888; margin-bottom: 0px;'>Fair Intrinsic Value</h4>
                <h2 style='color: white; margin-top: 5px;'>₹{round(intrinsic_value, 2)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with rc2:
            st.markdown(f"""
            <div style='background-color: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid #10B981;'>
                <h4 style='color: #888; margin-bottom: 0px;'>Safe Buy Price (With Margin)</h4>
                <h2 style='color: #10B981; margin-top: 5px;'>₹{round(buy_price, 2)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
        with rc3:
             st.markdown(f"""
            <div style='background-color: #1F2937; padding: 20px; border-radius: 10px; border-left: 5px solid #F59E0B;'>
                <h4 style='color: #888; margin-bottom: 0px;'>Margin of Safety Applied</h4>
                <h2 style='color: #F59E0B; margin-top: 5px;'>{margin_safety}%</h2>
            </div>
            """, unsafe_allow_html=True)
             
        st.caption("Disclaimer: This DCF model is for educational purposes. True valuation requires deep fundamental audit.")
