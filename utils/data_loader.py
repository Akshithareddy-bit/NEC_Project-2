import pandas as pd
import streamlit as st


def load_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df

    except Exception as e:
        st.error(f"CSV Loading Error: {e}")
        return None


def load_excel(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        return df

    except Exception as e:
        st.error(f"Excel Loading Error: {e}")
        return None