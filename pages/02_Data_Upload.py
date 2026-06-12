import streamlit as st
import pandas as pd
import plotly.express as px

from utils.session import init_session, set_data

# ---------------- INIT ----------------
init_session()

st.title("📂 Data Upload Dashboard")

uploaded_file = st.file_uploader(
    "Upload CSV / Excel File",
    type=["csv", "xlsx"]
)

df = None

# ---------------- LOAD DATA ----------------
if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    set_data(df)

    st.success("Dataset Loaded Successfully ✅")

    # ---------------- KPI METRICS ----------------
    st.subheader("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    st.divider()

    # ---------------- DATA PREVIEW ----------------
    st.subheader("📋 Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    # ---------------- STATISTICS ----------------
    st.subheader("📈 Statistical Summary")
    try:
        st.dataframe(df.describe(include="all"), use_container_width=True)
    except:
        st.info("No numeric columns for statistical summary")

    st.divider()

    # ---------------- NUMERIC GRAPH ----------------
    st.subheader("📊 Numeric Trend Analysis")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:

        selected_col = st.selectbox("Select Numeric Column", numeric_cols)

        fig1 = px.line(
            df,
            y=selected_col,
            title=f"{selected_col} Trend Analysis"
        )

        st.plotly_chart(fig1, use_container_width=True)

    else:
        st.info("No numeric columns found")

    # ---------------- CATEGORY GRAPH (FIXED) ----------------
    st.subheader("📊 Category Distribution")

    cat_cols = df.select_dtypes(include=["object"]).columns

    if len(cat_cols) > 0:

        cat_col = st.selectbox("Select Category Column", cat_cols)

        value_counts = df[cat_col].value_counts().reset_index()
        value_counts.columns = [cat_col, "Count"]

        fig2 = px.bar(
            value_counts,
            x=cat_col,
            y="Count",
            title=f"{cat_col} Distribution"
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("No categorical columns found")

    # ---------------- CORRELATION HEATMAP ----------------
    st.subheader("🔥 Correlation Heatmap")

    if len(numeric_cols) > 1:

        fig3 = px.imshow(
            df[numeric_cols].corr(),
            text_auto=True,
            title="Feature Correlation Heatmap"
        )

        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("Not enough numeric columns for correlation")

    # ---------------- DOWNLOAD ----------------
    st.subheader("⬇ Download Dataset")

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "dataset.csv",
        "text/csv"
    )

else:
    st.info("👆 Upload a dataset to see analytics dashboard")