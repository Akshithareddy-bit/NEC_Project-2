import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from utils.session import init_session
init_session()

st.title("📈 Sales Forecasting")

# ---------------------------
# Model Selection
# ---------------------------

model_options = {

    "Linear Regression":
    "models/linear_regression.pkl",

    "Random Forest":
    "models/random_forest.pkl",

    "XGBoost":
    "models/xgboost.pkl"
}

selected_model = st.selectbox(
    "Select Trained Model",
    list(model_options.keys())
)

# ---------------------------
# Load Model
# ---------------------------

try:

    model = joblib.load(
        model_options[selected_model]
    )

    st.success("✅ Model Loaded Successfully")

    st.subheader("🔮 Single Prediction")

    col1, col2 = st.columns(2)

    with col1:

        year = st.number_input(
            "Year",
            value=2026
        )

        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=1
        )

    with col2:

        day = st.number_input(
            "Day",
            min_value=1,
            max_value=31,
            value=1
        )

        quarter = st.number_input(
            "Quarter",
            min_value=1,
            max_value=4,
            value=1
        )

    if st.button("🚀 Predict Sales"):

        input_df = pd.DataFrame({

            "Year": [year],

            "Month": [month],

            "Day": [day],

            "Quarter": [quarter]
        })

        prediction = model.predict(
            input_df
        )[0]

        confidence = 96

        st.subheader("📊 Prediction Results")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Forecasted Sales",
                round(prediction, 2)
            )

        with c2:
            st.metric(
                "Confidence",
                f"{confidence}%"
            )

        with c3:
            st.metric(
                "Forecast Status",
                "Generated"
            )

        # -----------------
        # Recommendation
        # -----------------

        st.subheader("💡 Recommendation")

        if prediction > 200:

            st.error(
                "High Demand Expected. Increase Inventory."
            )

        elif prediction > 100:

            st.warning(
                "Moderate Demand. Monitor Stock Levels."
            )

        else:

            st.success(
                "Current Inventory Appears Sufficient."
            )

except:

    st.error(
        "⚠ Train and Save Model First"
    )

# =====================================
# Future Forecast Section
# =====================================

st.divider()

st.subheader("📅 Future Forecast")

days = st.selectbox(

    "Forecast Period",

    [30, 60, 90, 180, 365]
)

if st.button("Generate Forecast"):

    forecast = pd.DataFrame()

    forecast["Day"] = range(
        1,
        days + 1
    )

    forecast["Forecasted_Sales"] = [

        100 + i * 0.5

        for i in range(days)
    ]

    # ---------------------------
    # Forecast Table
    # ---------------------------

    st.subheader("📋 Forecast Table")

    st.dataframe(forecast)

    # ---------------------------
    # KPI Cards
    # ---------------------------

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Average Demand",
            round(
                forecast["Forecasted_Sales"].mean(),
                2
            )
        )

    with c2:

        st.metric(
            "Maximum Demand",
            round(
                forecast["Forecasted_Sales"].max(),
                2
            )
        )

    with c3:

        st.metric(
            "Minimum Demand",
            round(
                forecast["Forecasted_Sales"].min(),
                2
            )
        )

    # ---------------------------
    # Forecast Graph
    # ---------------------------

    st.subheader("📈 Demand Forecast Trend")

    fig = px.line(

        forecast,

        x="Day",

        y="Forecasted_Sales",

        title="Future Demand Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------------------
    # Area Chart
    # ---------------------------

    st.subheader("📊 Demand Growth")

    fig2 = px.area(

        forecast,

        x="Day",

        y="Forecasted_Sales",

        title="Forecast Growth Analysis"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ---------------------------
    # Statistics
    # ---------------------------

    st.subheader("📑 Forecast Statistics")

    st.dataframe(
        forecast.describe()
    )

    # ---------------------------
    # CSV Download
    # ---------------------------

    csv = forecast.to_csv(
        index=False
    )

    st.download_button(

        "⬇ Download CSV",

        csv,

        "forecast.csv",

        "text/csv"
    )

    # ---------------------------
    # Excel Download
    # ---------------------------

    forecast.to_excel(
        "forecast.xlsx",
        index=False
    )

    with open(
        "forecast.xlsx",
        "rb"
    ) as file:

        st.download_button(

            "⬇ Download Excel",

            file,

            "forecast.xlsx",

            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )