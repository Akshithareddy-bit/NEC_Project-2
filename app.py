import streamlit as st

st.set_page_config(
    page_title="Intelligent Sales Forecasting System",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
.hero {
    background: linear-gradient(90deg,#0ea5e9,#2563eb);
    padding:30px;
    border-radius:15px;
    color:white;
}
.card {
    background:#f8fafc;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:0px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>📈 Intelligent Sales Forecasting System</h1>
<p>AI-powered sales analytics, forecasting, and inventory optimization</p>
</div>
""", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns([2,1])

with col1:
    st.subheader("Welcome")

    st.write("""
    This platform helps you analyze sales data,
    train ML forecasting models, predict future revenue,
    optimize inventory, and generate business reports —
    all from a single interactive dashboard.
    """)

with col2:
    st.subheader("Quick Start")

    st.markdown("""
    1. 📂 Upload Dataset  
    2. 🧹 Preprocess Data  
    3. 📊 Run EDA Analysis  
    4. 🤖 Train Model  
    5. 📈 Forecast Sales  
    6. 📦 Optimize Inventory  
    7. 📑 Generate Reports  
    8. 📋 View Dashboard  
    """)

st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="card">
    <h3>📊 Analytics</h3>
    <p>Interactive charts and business insights</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <h3>📈 Forecasting</h3>
    <p>Train ML models and predict future sales</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="card">
    <h3>📦 Inventory</h3>
    <p>Safety stock, EOQ and reorder point analysis</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

st.subheader("🚀 Project Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("📂 Data Upload")
    st.success("🧹 Data Preprocessing")
    st.success("📊 EDA Analysis")

with col2:
    st.info("🤖 Model Training")
    st.info("📈 Sales Forecasting")
    st.info("📦 Inventory Optimization")

with col3:
    st.warning("📑 Reports & Export")
    st.warning("📋 Executive Dashboard")