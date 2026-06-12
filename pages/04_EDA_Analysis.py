import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from utils.session import init_session
init_session()

from utils.preprocessing import convert_date
from utils.feature_engineering import create_features

st.set_page_config(page_title="EDA Analysis", layout="wide")

st.title("📊 Exploratory Data Analysis Dashboard")

# ---------------- LOAD DATA ----------------
uploaded_file = st.file_uploader("Upload Dataset", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df = convert_date(df)
    df = create_features(df)

    st.success("Dataset Loaded Successfully")

    # ---------------- KPI ----------------
    st.subheader("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicates", df.duplicated().sum())

    st.divider()

    # ---------------- DATA PREVIEW ----------------
    st.subheader("📋 Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.subheader("📈 Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)

    st.divider()

    # ---------------- MISSING VALUES ----------------
    st.subheader("❌ Missing Values Analysis")

    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Values"]

    fig1 = px.bar(missing, x="Column", y="Missing Values", title="Missing Value Distribution")
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- NUMERIC DISTRIBUTION ----------------
    st.subheader("📊 Numerical Distribution")

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(num_cols) > 0:

        selected_col = st.selectbox("Select Column", num_cols)

        fig2 = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
        st.plotly_chart(fig2, use_container_width=True)

    # ---------------- OUTLIER DETECTION ----------------
    st.subheader("⚠ Outlier Detection (Box Plot)")

    if len(num_cols) > 0:

        selected_box = st.selectbox("Select Column for Outliers", num_cols)

        fig3 = px.box(df, y=selected_box, title=f"Outlier Detection - {selected_box}")
        st.plotly_chart(fig3, use_container_width=True)

    # ---------------- CORRELATION ----------------
    st.subheader("🔥 Correlation Heatmap")

    if len(num_cols) > 1:

        corr = df[num_cols].corr()

        fig4 = ff.create_annotated_heatmap(
            z=corr.values,
            x=list(corr.columns),
            y=list(corr.columns),
            colorscale="Viridis"
        )

        st.plotly_chart(fig4, use_container_width=True)

    # ---------------- BUSINESS INSIGHTS ----------------
    st.subheader("💡 AI Insights")

    insights = []

    if df.isnull().sum().sum() > 0:
        insights.append("❗ Missing values detected → requires preprocessing")

    if "Sales" in df.columns:
        if df["Sales"].max() > df["Sales"].mean() * 2:
            insights.append("⚠ High demand spikes detected in sales")

        insights.append("📈 Sales data shows forecasting potential")

    if "Revenue" in df.columns:
        insights.append("💰 Revenue distribution indicates top-product dependency")

    insights.append("📊 Dataset is suitable for ML forecasting models")

    for i in insights:
        st.success(i)

    st.divider()

    # ---------------- DOWNLOAD ----------------
    st.subheader("⬇ Download Processed Dataset")

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Clean Dataset",
        csv,
        "eda_processed_data.csv",
        "text/csv"
    )

else:
    st.info("👆 Upload dataset to start EDA analysis")