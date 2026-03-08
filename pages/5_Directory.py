import streamlit as st

# Setup Page
st.set_page_config(page_title="Stocks Directory | DIG", page_icon="🗂️", layout="wide")

# --- 🌟 HEADER SECTION ---
st.markdown("<h1 style='color:#1E88E5;'>🗂️ Stocks Directory</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#888;'>Explore the top curated list of NSE Listed Companies. Filter by sector and analyze instantly.</p>", unsafe_allow_html=True)
st.write("---")

# --- 📊 THE DATABASE (Curated Top Stocks) ---
# Humne yahan ek solid list banayi hai taaki page 1 second mein load ho jaye!
DIRECTORY_DATA = [
    {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "Energy"},
    {"symbol": "TCS", "name": "Tata Consultancy Svcs", "sector": "IT"},
    {"symbol": "HDFCBANK", "name": "HDFC Bank", "sector": "Banking"},
    {"symbol": "ITC", "name": "ITC Ltd.", "sector": "FMCG"},
    {"symbol": "INFY", "name": "Infosys", "sector": "IT"},
    {"symbol": "SBIN", "name": "State Bank of India", "sector": "Banking"},
    {"symbol": "BHARTIARTL", "name": "Bharti Airtel", "sector": "Telecom"},
    {"symbol": "HINDUNILVR", "name": "Hindustan Unilever", "sector": "FMCG"},
    {"symbol": "L&T", "name": "Larsen & Toubro", "sector": "Infrastructure"},
    {"symbol": "TATAMOTORS", "name": "Tata Motors", "sector": "Automobile"},
    {"symbol": "M&M", "name": "Mahindra & Mahindra", "sector": "Automobile"},
    {"symbol": "ASIANPAINT", "name": "Asian Paints", "sector": "Consumer Goods"},
    {"symbol": "ZOMATO", "name": "Zomato Ltd.", "sector": "Consumer Tech"},
    {"symbol": "TATAPOWER", "name": "Tata Power", "sector": "Energy"},
    {"symbol": "IRCTC", "name": "IRCTC", "sector": "Railways"}
]

# --- 🔍 SMART FILTERS ---
# Saare unique sectors nikalne ka logic
sectors = sorted(list(set([item["sector"] for item in DIRECTORY_DATA])))

f1, f2, f3 = st.columns([1, 1, 2])
with f1:
    selected_sector = st.selectbox("Select Sector", ["All Sectors"] + sectors)
with f2:
    search_text = st.text_input("Quick Filter (Name/Symbol)", placeholder="e.g. Tata...")

st.write("<br>", unsafe_allow_html=True)

# --- 🗂️ THE GRID SYSTEM (Finology Style) ---
# Filter logic apply karna
filtered_data = DIRECTORY_DATA
if selected_sector != "All Sectors":
    filtered_data = [d for d in filtered_data if d["sector"] == selected_sector]
if search_text:
    filtered_data = [d for d in filtered_data if search_text.lower() in d["name"].lower() or search_text.lower() in d["symbol"].lower()]

# Grid banana (3 columns per row)
if not filtered_data:
    st.warning("No stocks found matching your criteria.")
else:
    # 3 columns ka layout
    cols = st.columns(3)
    
    for index, stock in enumerate(filtered_data):
        # Decide karna ki kaunse column mein card jayega (0, 1, or 2)
        col = cols[index % 3]
        
        with col:
            # Card ka UI Design (Dark & Green Theme)
            st.markdown(f"""
            <div style='background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1F2937; margin-bottom: 10px; height: 160px;'>
                <h3 style='margin-top: 0px; margin-bottom: 5px; color: #E5E7EB; font-size: 1.3rem;'>{stock['name']}</h3>
                <p style='margin: 0px; font-size: 13px; color: #888;'>Sector: <span style='color: #00E570; font-weight: bold;'>{stock['sector']}</span></p>
                <div style='margin-top: 15px; margin-bottom: 15px;'>
                    <span style='background-color: #1F2937; padding: 4px 8px; border-radius: 4px; font-size: 12px; color: #fff;'>NSE: {stock['symbol']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Button (HTML ke theek neeche taaki wo functional rahe)
            # Hum isme wahi "Magic Trick" laga rahe hain jo Baskets page pe lagayi thi
            if st.button("Details", key=f"dir_btn_{stock['symbol']}", type="primary", use_container_width=True):
                # Isse App.py ka engine trigger hoga
                st.session_state.current_view = stock['symbol'] + ".NS"
                st.switch_page("app.py")
            
            st.write("<br>", unsafe_allow_html=True) # Cards ke beech mein thodi space
