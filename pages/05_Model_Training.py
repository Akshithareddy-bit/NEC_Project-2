import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from utils.session import init_session, get_data

# ---------------- INIT ----------------
init_session()

st.title("🤖 Model Training Dashboard")

# ---------------- LOAD DATA ----------------
df = get_data()

if df is None:
    st.error("❌ No dataset found. Please upload data first.")
    st.stop()

st.success("Dataset Loaded ✅")
st.dataframe(df.head())

df = df.copy()

# ---------------- SAFE CLEANING ----------------
# Convert only object columns safely
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------- DROP EMPTY ROWS ----------------
df = df.dropna()

if df.shape[0] < 5:
    st.error("❌ Not enough usable data after cleaning.")
    st.stop()

# ---------------- NUMERIC ONLY ----------------
numeric_df = df.select_dtypes(include=["int64", "float64"])

if numeric_df.shape[1] < 2:
    st.error("❌ Need at least 2 numeric columns for training.")
    st.stop()

# ---------------- TARGET ----------------
target_col = st.selectbox(
    "🎯 Select Target Column",
    numeric_df.columns
)

# ---------------- FEATURES ----------------
feature_cols = st.multiselect(
    "📌 Select Feature Columns",
    [c for c in numeric_df.columns if c != target_col],
    default=[c for c in numeric_df.columns if c != target_col][:3]
)

if len(feature_cols) == 0:
    st.warning("Please select features")
    st.stop()

X = numeric_df[feature_cols]
y = numeric_df[target_col]

# ---------------- SPLIT SAFELY ----------------
test_size = 0.2 if len(df) > 10 else 0.3

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=test_size,
    random_state=42
)

# ---------------- MODEL ----------------
model = RandomForestRegressor()

if st.button("🚀 Train Model"):

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    score = model.score(X_test, y_test)

    st.success("Model Trained Successfully ✅")

    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", round(score, 3))
    col2.metric("Train Rows", len(X_train))
    col3.metric("Test Rows", len(X_test))

    # ---------------- ACTUAL VS PREDICTED ----------------
    result_df = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": preds
    })

    st.subheader("📈 Actual vs Predicted")
    st.plotly_chart(px.line(result_df), use_container_width=True)

    st.subheader("📊 Scatter Plot")
    st.plotly_chart(
        px.scatter(result_df, x="Actual", y="Predicted", trendline="ols"),
        use_container_width=True
    )

    # ---------------- ERROR ----------------
    result_df["Error"] = result_df["Actual"] - result_df["Predicted"]

    st.subheader("📉 Error Distribution")
    st.plotly_chart(
        px.histogram(result_df, x="Error"),
        use_container_width=True
    )

    # ---------------- FEATURE IMPORTANCE ----------------
    importance_df = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=True)

    st.subheader("🔥 Feature Importance")

    st.plotly_chart(
        px.bar(
            importance_df,
            x="Importance",
            y="Feature",
            orientation="h"
        ),
        use_container_width=True
    )