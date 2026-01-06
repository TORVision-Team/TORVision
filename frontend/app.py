import os
import sys
import json
import streamlit as st
import pandas as pd
import numpy as np

# ---------------- FIX PROJECT ROOT PATH ----------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.config import DATA_PATH

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="TORVision Dashboard", layout="wide")

st.title("TORVision — ML-Driven TOR Analysis Dashboard")
st.caption("Forensic correlation & visualization of TOR infrastructure")

DATA_DIR = DATA_PATH

# ---------------- HELPER FUNCTIONS ----------------
def load_engineered():
    path = os.path.join(DATA_DIR, "engineered_output.csv")
    return pd.read_csv(path) if os.path.exists(path) else None

def load_similarity():
    path = os.path.join(DATA_DIR, "similarity_matrix.csv")
    return pd.read_csv(path, header=None) if os.path.exists(path) else None

def load_sample_pcap():
    path = os.path.join(DATA_DIR, "sample_pcap.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return pd.DataFrame(json.load(f))
    return None

def load_tor_nodes():
    path = os.path.join(DATA_DIR, "sample_tor_nodes.csv")
    return pd.read_csv(path) if os.path.exists(path) else None

def add_country_coordinates(df):
    country_coords = {
        "us": (37.0902, -95.7129),
        "in": (20.5937, 78.9629),
        "de": (51.1657, 10.4515),
        "fr": (46.2276, 2.2137),
        "gb": (55.3781, -3.4360),
        "nl": (52.1326, 5.2913),
        "ru": (61.5240, 105.3188),
        "cn": (35.8617, 104.1954),
    }

    df["country"] = df["country"].str.lower()
    df["lat"] = df["country"].map(lambda c: country_coords.get(c, (np.nan, np.nan))[0])
    df["lon"] = df["country"].map(lambda c: country_coords.get(c, (np.nan, np.nan))[1])
    return df

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Engineered Features",
        "Similarity Analysis",
        "Forensic PCAP Sample",
        "TOR Weather Forecast",
    ],
)

# ================== OVERVIEW ==================
if page == "Overview":
    st.header("System Overview")

    df = load_engineered()
    if df is not None:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total TOR Nodes", len(df))
        c2.metric("Exit Nodes", int(df.get("is_exit", 0).sum()))
        c3.metric("Middle Nodes", int(df.get("is_middle", 0).sum()))

        if "bandwidth_norm" in df.columns:
            st.subheader("Bandwidth Distribution")
            st.line_chart(df["bandwidth_norm"])
    else:
        st.warning("Engineered data not found.")


# ================== ENGINEERED FEATURES ==================
elif page == "Engineered Features":
    st.header("Engineered TOR Node Features")
    df = load_engineered()
    st.dataframe(df, use_container_width=True) if df is not None else st.warning("No data found.")

# ================== SIMILARITY ==================
elif page == "Similarity Analysis":
    st.header("Node Similarity Analysis")

    sim_df = load_similarity()
    eng_df = load_engineered()

    if sim_df is None or eng_df is None:
        st.warning("Similarity data not found.")
    else:
        sim = sim_df.values.astype(float)
        np.fill_diagonal(sim, 0)
        r, c = np.unravel_index(np.argmax(sim), sim.shape)

        st.success("Most Correlated TOR Nodes")
        st.write("Node A:", eng_df.iloc[r]["fingerprint"])
        st.write("Node B:", eng_df.iloc[c]["fingerprint"])
        st.metric("Similarity Score", f"{sim[r, c]:.3f}")

# ================== PCAP ==================
elif page == "Forensic PCAP Sample":
    st.header("Forensic PCAP Data")
    pcap_df = load_sample_pcap()
    st.dataframe(pcap_df, use_container_width=True) if pcap_df is not None else st.warning("PCAP not found.")

# ================== TOR WEATHER ==================
elif page == "TOR Weather Forecast":
    st.header("TOR Weather Forecast")
    try:
        from tor_weather_forecast.dashboard_section import tor_weather_section
        tor_weather_section()
    except Exception as e:
        st.error("TOR Weather module failed")
        st.code(str(e))
