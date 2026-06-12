import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import init_session
init_session()

from utils.inventory import (
    calculate_safety_stock,
    calculate_reorder_point,
    calculate_eoq,
    inventory_status
)

st.set_page_config(page_title="Inventory Optimization", layout="wide")

st.title("📦 Smart Inventory Optimization Dashboard")

st.markdown("Optimize stock levels using AI-driven supply chain analytics")

st.divider()

# ---------------- INPUT SECTION ----------------
st.subheader("⚙ Inventory Input Parameters")

col1, col2, col3, col4 = st.columns(4)

current_stock = col1.number_input("Current Stock", min_value=0, value=30)
avg_sales = col2.number_input("Avg Daily Sales", min_value=1, value=5)
lead_time = col3.number_input("Lead Time (Days)", min_value=1, value=7)
safety_factor = col4.number_input("Safety Factor", min_value=1.0, value=2.0)

col5, col6 = st.columns(2)

annual_demand = col5.number_input("Annual Demand", value=5000)
ordering_cost = col6.number_input("Ordering Cost", value=100)

holding_cost = st.number_input("Holding Cost", value=20)

st.divider()

# ---------------- CALCULATIONS ----------------
if st.button("🚀 Optimize Inventory"):

    safety_stock = calculate_safety_stock(avg_sales, lead_time, safety_factor)
    reorder_point = calculate_reorder_point(avg_sales, lead_time, safety_stock)
    eoq = calculate_eoq(annual_demand, ordering_cost, holding_cost)

    recommended_stock = reorder_point + safety_stock

    status = inventory_status(current_stock, reorder_point, recommended_stock)

    # ---------------- KPI CARDS ----------------
    st.subheader("📊 Inventory KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Safety Stock", round(safety_stock, 2))
    c2.metric("Reorder Point", round(reorder_point, 2))
    c3.metric("EOQ", round(eoq, 2))
    c4.metric("Recommended Stock", round(recommended_stock, 2))

    st.divider()

    # ---------------- STATUS PANEL ----------------
    st.subheader("🚨 Inventory Status")

    if status == "Reorder Required":
        st.error("⚠ Reorder Required - Low Stock Risk Detected")
    elif status == "Overstock":
        st.warning("⚠ Overstock Detected - Reduce Procurement")
    else:
        st.success("✅ Stock Level Healthy")

    # ---------------- VISUALIZATION ----------------
    st.subheader("📈 Inventory Analysis Chart")

    chart_df = pd.DataFrame({
        "Category": ["Current Stock", "Recommended Stock", "Reorder Point"],
        "Value": [current_stock, recommended_stock, reorder_point]
    })

    fig = px.bar(
        chart_df,
        x="Category",
        y="Value",
        color="Category",
        title="Stock vs Recommendation"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- EOQ INSIGHT ----------------
    st.subheader("📦 EOQ Analysis")

    eoq_df = pd.DataFrame({
        "Type": ["Economic Order Quantity (EOQ)"],
        "Value": [eoq]
    })

    fig2 = px.pie(
        eoq_df,
        names="Type",
        values="Value",
        title="Optimal Order Quantity"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- ALERT SYSTEM ----------------
    st.subheader("⚠ Smart Alerts")

    alerts = []

    if current_stock < reorder_point:
        alerts.append("Low Stock Alert - Immediate Reorder Required")

    if current_stock > recommended_stock * 1.5:
        alerts.append("Overstock Warning - Excess Inventory Detected")

    if avg_sales > 10:
        alerts.append("High Demand Pattern Detected")

    if len(alerts) == 0:
        st.success("No Critical Alerts")

    for a in alerts:
        st.warning(a)

    # ---------------- DOWNLOAD ----------------
    st.subheader("⬇ Export Report")

    report = pd.DataFrame({
        "Metric": ["Safety Stock", "Reorder Point", "EOQ", "Recommended Stock", "Status"],
        "Value": [
            safety_stock,
            reorder_point,
            eoq,
            recommended_stock,
            status
        ]
    })

    csv = report.to_csv(index=False)

    st.download_button(
        "Download Inventory Report",
        csv,
        "inventory_report.csv",
        "text/csv"
    )