import os
import sys

# ---------------- FIX PROJECT ROOT PATH (CRITICAL) ----------------
# app.py is inside: TORVision/frontend/app.py
# Project root is:   TORVision/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# -----------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np

# ✅ Safe import after path fix
from utils.config import DATA_PATH

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(
    page_title="TORVision Dashboard",
    layout="wide"
)

st.title("TORVision : ML-Driven TOR Analysis Dashboard")

# ---------------- Helper functions ----------------
DATA_DIR = DATA_PATH


def load_engineered():
    path = os.path.join(DATA_DIR, "engineered_output.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def load_similarity():
    path = os.path.join(DATA_DIR, "similarity_matrix.csv")
    if os.path.exists(path):
        return pd.read_csv(path, header=None)
    return None


def load_sample_pcap():
    path = os.path.join(DATA_DIR, "sample_pcap.json")
    if os.path.exists(path):
        import json
        with open(path, "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    return None


# ---------------- Sidebar ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Engineered Features",
        "Similarity Matrix",
        "Forensic Sample (PCAP JSON)",
        "TOR Weather Forecast",
    ],
)

# ================== OVERVIEW ==================
if page == "Overview":
    st.header("System Overview")

    df = load_engineered()
    if df is None:
        st.warning("engineered_output.csv not found. Run ML pipeline first.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Nodes", len(df))
        with col2:
            st.metric("Exit Nodes", int(df["is_exit"].sum()) if "is_exit" in df else 0)
        with col3:
            st.metric("Middle Nodes", int(df["is_middle"].sum()) if "is_middle" in df else 0)

        if "bandwidth_norm" in df.columns:
            st.subheader("Bandwidth Distribution")
            st.line_chart(df["bandwidth_norm"])


# ================== ENGINEERED FEATURES ==================
elif page == "Engineered Features":
    st.header("Engineered Features")

    df = load_engineered()
    if df is None:
        st.warning("No engineered features found.")
    else:
        st.dataframe(df, use_container_width=True)


# ================== SIMILARITY MATRIX ==================
elif page == "Similarity Matrix":
    st.header("Node Similarity Analysis")

    sim_df = load_similarity()
    eng_df = load_engineered()

    if sim_df is None or eng_df is None:
        st.warning("Similarity data not found.")
    else:
        sim_values = sim_df.values.astype(float)

        # Remove self similarity
        for i in range(min(sim_values.shape)):
            sim_values[i, i] = 0

        r, c = np.unravel_index(np.argmax(sim_values), sim_values.shape)
        score = sim_values[r, c]

        n1 = eng_df.iloc[r]["fingerprint"] if r < len(eng_df) else f"Index {r}"
        n2 = eng_df.iloc[c]["fingerprint"] if c < len(eng_df) else f"Index {c}"

        st.subheader("Most Similar Node Pair")
        st.success(f"{n1} ↔ {n2}")
        st.metric("Similarity Score", f"{score:.3f}")


# ================== FORENSIC ==================
elif page == "Forensic Sample (PCAP JSON)":
    st.header("Forensic – Parsed PCAP Data")

    pcap_df = load_sample_pcap()
    if pcap_df is None:
        st.warning("PCAP data not found.")
    else:
        st.dataframe(pcap_df, use_container_width=True)


# ================== TOR WEATHER FORECAST ==================
elif page == "TOR Weather Forecast":
    st.header("TOR Weather Forecast")

    try:
        from tor_weather_forecast.dashboard_section import tor_weather_section
        tor_weather_section()
    except Exception as e:
        st.error("TOR Weather module failed to load.")
        st.code(str(e))
