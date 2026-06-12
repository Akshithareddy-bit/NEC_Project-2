import streamlit as st
import pandas as pd
import plotly.express as px
from utils.session import init_session
init_session()

from utils.preprocessing import (
    handle_missing_values,
    remove_duplicates,
    convert_date
)

from utils.feature_engineering import (
    create_features
)

st.title("🧹 Data Preprocessing")

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv"]
)

if uploaded_file:

    # --------------------
    # Load Dataset
    # --------------------
    df_original = pd.read_csv(uploaded_file)

    st.subheader("📋 Original Dataset")

    st.dataframe(df_original)

    # --------------------
    # Before Stats
    # --------------------
    missing_before = df_original.isnull().sum().sum()
    duplicate_before = df_original.duplicated().sum()

    # --------------------
    # Preprocessing
    # --------------------
    df = df_original.copy()

    df = handle_missing_values(df)

    df, duplicates_removed = remove_duplicates(df)

    df = convert_date(df)

    df = create_features(df)

    missing_after = df.isnull().sum().sum()

    # --------------------
    # Processed Dataset
    # --------------------
    st.subheader("✅ Processed Dataset")

    st.dataframe(df)

    # --------------------
    # KPI Cards
    # --------------------
    st.subheader("📊 Preprocessing Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Missing Values Removed",
            int(missing_before - missing_after)
        )

    with col2:
        st.metric(
            "Duplicates Removed",
            int(duplicates_removed)
        )

    with col3:
        st.metric(
            "Features Generated",
            len(df.columns) - len(df_original.columns)
        )

    # --------------------
    # Missing Values Table
    # --------------------
    st.subheader("⚠ Missing Values Summary")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(missing_df)

    # --------------------
    # Missing Values Graph
    # --------------------
    st.subheader("📈 Missing Values Before vs After")

    compare_df = pd.DataFrame({

        "Stage": [
            "Before",
            "After"
        ],

        "Missing Values": [
            missing_before,
            missing_after
        ]
    })

    fig = px.bar(
        compare_df,
        x="Stage",
        y="Missing Values",
        title="Missing Values Comparison"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------
    # Dataset Shape
    # --------------------
    st.subheader("📏 Dataset Shape")

    shape_df = pd.DataFrame({

        "Metric": [
            "Rows",
            "Columns"
        ],

        "Value": [
            df.shape[0],
            df.shape[1]
        ]
    })

    st.dataframe(shape_df)

    # --------------------
    # Feature Summary
    # --------------------
    st.subheader("🛠 Generated Features")

    generated_features = list(
        set(df.columns) -
        set(df_original.columns)
    )

    if generated_features:

        feature_df = pd.DataFrame({
            "Generated Features":
            generated_features
        })

        st.dataframe(feature_df)

    # --------------------
    # Save Dataset
    # --------------------
    df.to_csv(
        "processed/processed_dataset.csv",
        index=False
    )

    st.success(
        "✅ Processed Dataset Saved Successfully"
    )

    # --------------------
    # Download CSV
    # --------------------
    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Processed CSV",
        data=csv,
        file_name="processed_dataset.csv",
        mime="text/csv"
    )

    # --------------------
    # Download Excel
    # --------------------
    excel_file = "processed_dataset.xlsx"

    df.to_excel(
        excel_file,
        index=False
    )

    with open(excel_file, "rb") as f:

        st.download_button(
            label="⬇ Download Excel",
            data=f,
            file_name="processed_dataset.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    st.success(
        "🎉 Preprocessing Completed Successfully"
    )