import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import init_session
init_session()

from utils.session import init_session, get_data

# ---------------- INIT ----------------
init_session()

st.set_page_config(page_title="AI Dashboard", layout="wide")

st.title("📋 Executive AI Dashboard - Sales & Inventory Intelligence")

# ---------------- LOAD DATA ----------------
df = get_data()

if df is None:
    st.error("❌ No dataset found. Please upload data first.")
    st.stop()

df = df.copy()

# ---------------- AUTO COLUMN SAFETY ----------------
if "Sales" not in df.columns:
    df["Sales"] = 0

if "Revenue" not in df.columns:
    df["Revenue"] = df["Sales"] * 100

if "Product" not in df.columns:
    df["Product"] = "Unknown"

# ---------------- KPI SECTION ----------------
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", int(df["Sales"].sum()))
col2.metric("Total Revenue", f"₹{int(df['Revenue'].sum()):,}")
col3.metric("Products", df["Product"].nunique())
col4.metric("Avg Sales", round(df["Sales"].mean(), 2))

st.divider()

# ---------------- SALES TREND GRAPH ----------------
st.subheader("📈 Sales Trend Analysis")

df["Index"] = range(len(df))

fig1 = px.line(
    df,
    x="Index",
    y="Sales",
    title="Sales Trend Over Time",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# ---------------- TOP PRODUCTS ----------------
st.subheader("🏆 Top Performing Products")

top = df.groupby("Product")["Sales"].sum().reset_index()
top = top.sort_values("Sales", ascending=False).head(10)

fig2 = px.bar(
    top,
    x="Product",
    y="Sales",
    title="Top 10 Products"
)
st.plotly_chart(fig2, use_container_width=True)

# ---------------- REVENUE PIE CHART ----------------
st.subheader("💰 Revenue Distribution")

fig3 = px.pie(
    df,
    names="Product",
    values="Revenue",
    title="Revenue Share by Product"
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- INVENTORY ANALYSIS ----------------
st.subheader("📦 Inventory Intelligence")

avg_sales = df["Sales"].mean()

df["Stock_Status"] = df["Sales"].apply(
    lambda x: "Low Stock" if x < avg_sales * 0.5
    else ("Overstock" if x > avg_sales * 1.5 else "Healthy")
)

status = df["Stock_Status"].value_counts().reset_index()
status.columns = ["Status", "Count"]

fig4 = px.bar(
    status,
    x="Status",
    y="Count",
    title="Inventory Status Distribution"
)
st.plotly_chart(fig4, use_container_width=True)

# ---------------- INSIGHTS ----------------
st.subheader("💡 AI Insights")

st.success("📈 System is analyzing sales patterns")

if df["Sales"].mean() > df["Sales"].median():
    st.warning("⚠ Sales are skewed: few products dominate revenue")

if df["Sales"].max() > df["Sales"].mean() * 2:
    st.warning("⚠ Demand spikes detected in some products")

st.info("🤖 Ready for forecasting & optimization")

# ---------------- DOWNLOAD ----------------
st.subheader("⬇ Export Data")

csv = df.to_csv(index=False)

st.download_button(
    "Download Dashboard Data",
    csv,
    "final_dashboard.csv",
    "text/csv"
)