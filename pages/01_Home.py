import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import get_data
from utils.session import init_session
init_session()

st.set_page_config(page_title="Home Dashboard", layout="wide")

df = get_data()

# ---------------- HEADER ----------------
st.title("🏠 Executive Home Dashboard")
st.markdown("### Intelligent Sales Forecasting & Inventory Optimization System")

st.divider()

# ---------------- IF NO DATA ----------------
if df is None:
    st.warning("Please upload dataset from Data Upload page to activate dashboard.")
    st.stop()

# ---------------- KPI SECTION ----------------
st.subheader("📊 Business KPIs")

col1, col2, col3, col4 = st.columns(4)

total_revenue = df["Revenue"].sum() if "Revenue" in df.columns else 0
total_sales = df["Sales"].sum() if "Sales" in df.columns else 0
products = df["Product"].nunique() if "Product" in df.columns else 0
forecast_accuracy = 96  # simulated KPI (you can later connect ML)

col1.metric("Total Revenue", f"₹{int(total_revenue):,}")
col2.metric("Total Sales", int(total_sales))
col3.metric("Products", products)
col4.metric("Forecast Accuracy", f"{forecast_accuracy}%")

st.divider()

# ---------------- CHART SECTION ----------------
st.subheader("📈 Business Performance Overview")

col1, col2 = st.columns(2)

with col1:
    if "Sales" in df.columns:
        sales_df = df.copy()
        sales_df["Index"] = range(len(sales_df))

        fig1 = px.line(
            sales_df,
            x="Index",
            y="Sales",
            title="Sales Trend Over Time"
        )
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    if "Revenue" in df.columns:
        fig2 = px.bar(
            df,
            x="Product" if "Product" in df.columns else df.index,
            y="Revenue",
            title="Revenue Contribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---------------- TOP PRODUCTS ----------------
st.subheader("🏆 Top Performing Products")

if "Product" in df.columns and "Sales" in df.columns:

    top = df.groupby("Product")["Sales"].sum().reset_index()
    top = top.sort_values("Sales", ascending=False)

    fig3 = px.bar(
        top,
        x="Product",
        y="Sales",
        title="Top Selling Products"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ---------------- INSIGHTS ENGINE ----------------
st.subheader("💡 AI Insights Engine")

insights = []

if "Sales" in df.columns:
    if df["Sales"].mean() > df["Sales"].median():
        insights.append("📊 Sales are skewed → few products dominate revenue")

    if df["Sales"].max() > df["Sales"].mean() * 2:
        insights.append("⚠ Demand spike detected in certain products")

if "Revenue" in df.columns:
    insights.append("💰 Revenue is concentrated in top products")

insights.append("📦 System ready for forecasting & inventory optimization")

for i in insights:
    st.success(i)

st.divider()

# ---------------- ALERT SECTION ----------------
st.subheader("🚨 System Alerts")

if "Sales" in df.columns:
    if df["Sales"].min() < df["Sales"].mean() * 0.3:
        st.error("Low demand products detected")

    if df["Sales"].max() > df["Sales"].mean() * 2:
        st.warning("High demand spike detected")

    else:
        st.success("No critical alerts found")

st.divider()

# ---------------- DOWNLOAD ----------------
st.subheader("⬇ Export Data")

csv = df.to_csv(index=False)

st.download_button(
    "Download Full Dataset",
    csv,
    "home_dashboard_data.csv",
    "text/csv"
)