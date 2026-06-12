import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import init_session
init_session()

from utils.reports import (
    generate_pdf_report,
    generate_excel_report,
    generate_csv_report
)

st.title("📑 Reports & Export Dashboard")

# -----------------------------------
# Sample Data (Replace with real data later)
# -----------------------------------

sample_df = pd.DataFrame({

    "Product": [
        "Laptop",
        "Mobile",
        "Monitor",
        "Keyboard",
        "Mouse"
    ],

    "Sales": [
        120,
        150,
        90,
        200,
        180
    ],

    "Revenue": [
        120000,
        90000,
        45000,
        80000,
        30000
    ]
})

# -----------------------------------
# Dataset Preview
# -----------------------------------

st.subheader("📋 Report Dataset Preview")

st.dataframe(sample_df)

# -----------------------------------
# KPI Cards
# -----------------------------------

st.subheader("📊 Report KPIs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales",
        int(sample_df["Sales"].sum())
    )

with col2:
    st.metric(
        "Total Revenue",
        f"₹{sample_df['Revenue'].sum()}"
    )

with col3:
    st.metric(
        "Products",
        sample_df.shape[0]
    )

# -----------------------------------
# Sales Chart
# -----------------------------------

st.subheader("📈 Sales Performance")

fig1 = px.bar(
    sample_df,
    x="Product",
    y="Sales",
    title="Product-wise Sales"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# -----------------------------------
# Revenue Chart
# -----------------------------------

st.subheader("💰 Revenue Contribution")

fig2 = px.pie(
    sample_df,
    names="Product",
    values="Revenue",
    title="Revenue Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# Report Summary
# -----------------------------------

st.subheader("📑 AI Generated Summary")

summary_text = f"""
Total Sales: {sample_df['Sales'].sum()} units  
Total Revenue: ₹{sample_df['Revenue'].sum()}  
Top Product: {sample_df.loc[sample_df['Sales'].idxmax(), 'Product']}  
Insight: Sales are concentrated among top performing products.
"""

st.info(summary_text)

# -----------------------------------
# Generate PDF Report
# -----------------------------------

if st.button("📄 Generate PDF Report"):

    pdf_file = generate_pdf_report(

        "reports/forecast_report.pdf",

        "Sales Forecast Report",

        summary_text
    )

    st.success(f"✅ PDF Generated: {pdf_file}")

# -----------------------------------
# Generate Excel Report
# -----------------------------------

if st.button("📊 Generate Excel Report"):

    excel_file = generate_excel_report(

        sample_df,

        "reports/inventory_report.xlsx"
    )

    st.success(f"✅ Excel Generated: {excel_file}")

# -----------------------------------
# Generate CSV Report
# -----------------------------------

if st.button("⬇ Generate CSV Report"):

    csv_file = generate_csv_report(

        sample_df,

        "reports/kpi_report.csv"
    )

    st.success(f"✅ CSV Generated: {csv_file}")

# -----------------------------------
# Download Buttons
# -----------------------------------

st.subheader("⬇ Direct Downloads")

csv = sample_df.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    "report.csv",
    "text/csv"
)

excel_file = "report.xlsx"
sample_df.to_excel(excel_file, index=False)

with open(excel_file, "rb") as f:
    st.download_button(
        "Download Excel",
        f,
        "report.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )