import streamlit as st
import pandas as pd

BASE_URL = (
    "https://huggingface.co/datasets/"
    "Maiyarasu/football_analytics/resolve/main/parquet"
)

@st.cache_data(ttl=3600)
def load_parquet(path: str):
    return pd.read_parquet(f"{BASE_URL}/{path}")