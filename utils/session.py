import streamlit as st

def init_session():
    if "data" not in st.session_state:
        st.session_state["data"] = None

def set_data(df):
    st.session_state["data"] = df

def get_data():
    return st.session_state.get("data", None)