import os
import pandas as pd
import streamlit as st


def load_dataset():

    st.sidebar.header("📂 Dataset")

    uploaded = st.sidebar.file_uploader(
        "Upload Accident Dataset (CSV)",
        type=["csv"]
    )

    if uploaded is not None:
        return pd.read_csv(uploaded)

    default_path = os.path.join("data", "sample_accidents.csv")

    if os.path.exists(default_path):
        return pd.read_csv(default_path)

    st.error("Default dataset not found!")
    st.stop()