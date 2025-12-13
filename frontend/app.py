app.py : import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from utils.config import DATA_PATH

# Make sure Python can find your project modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(_file_)))
sys.path.append(PROJECT_ROOT)

# If you need them later, you can import your modules like this:
# from preprocessor.feature_engineering import FeatureEngineer
# from preprocessor.similarity import SimilarityEngine
# from forensic_logs.pcap_parser import PcapParser
# from forensic_logs.log_matcher import LogMatcher

st.set_page_config(
    page_title="TORVision Dashboard",
    layout="wide"
)

st.title(" TORVision – ML-Driven TOR Analysis Dashboard")

# ---------- Helper functions to load ML outputs ----------
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

# ---------- Sidebar Navigation ----------
st.sidebar.title(" Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Overview",
        "Engineered Features",
        "Similarity Matrix",
        "Forensic Sample (PCAP JSON)"
    ]
)

# ================== PAGE: OVERVIEW ==================
if page == "Overview":
    st.header("System Overview")

    df = load_engineered()

    if df is None:
        st.warning("engineered_output.csv not found in data/samples. Run your ML pipeline first.")
    else:
        col1, col2, col3 = st.columns(3)

        total_nodes = len(df)
        exit_nodes = int(df["is_exit"].sum()) if "is_exit" in df.columns else 0
        middle_nodes = int(df["is_middle"].sum()) if "is_middle" in df.columns else 0

        with col1:
            st.metric("Total Nodes", total_nodes)
        with col2:
            st.metric("Exit Nodes", exit_nodes)
        with col3:
            st.metric("Middle Nodes", middle_nodes)

        st.subheader("Bandwidth (normalized) distribution")
        if "bandwidth_norm" in df.columns:
            st.line_chart(df["bandwidth_norm"])
        else:
            st.info("bandwidth_norm column not found in engineered_output.csv")

# ================== PAGE: ENGINEERED FEATURES ==================
elif page == "Engineered Features":
    st.header("Engineered Features (from ML pipeline)")

    df = load_engineered()
    if df is None:
        st.warning("engineered_output.csv not found in data/samples.")
    else:
        st.dataframe(df, use_container_width=True)

# ================== PAGE: SIMILARITY ==================
elif page == "Similarity Matrix":
    st.header("Node Similarity Matrix")

    sim_df = load_similarity()
    eng_df = load_engineered()

    if sim_df is None or eng_df is None:
        st.warning("similarity_matrix.csv and/or engineered_output.csv not found.")
    else:
        sim_values = sim_df.values.astype(float)
        np.fill_diagonal(sim_values, 0.0)  # Ignore self-similarity

        # Most similar node pair
        max_idx = np.unravel_index(sim_values.argmax(), sim_values.shape)
        score = sim_values[max_idx]

        node1_fp = eng_df.iloc[max_idx[0]]["fingerprint"] if "fingerprint" in eng_df.columns else f"Node {max_idx[0]}"
        node2_fp = eng_df.iloc[max_idx[1]]["fingerprint"] if "fingerprint" in eng_df.columns else f"Node {max_idx[1]}"

        st.subheader("Most similar node pair")
        st.success(f"{node1_fp}** ↔ *{node2_fp}*  (similarity score: {score:.3f})")

        # Summary stats
        st.subheader("Similarity Analysis Summary")
        st.metric("Total Nodes Analyzed", len(eng_df))
        st.metric("Similarity Matrix Size", f"{sim_df.shape[0]} × {sim_df.shape[1]}")
        st.info(
            "The full similarity matrix is intentionally not displayed due to size. "
            "High-risk correlations are extracted and analyzed instead."
        )

        # Optional: Top 5 most similar pairs
        flat = [(i, j, sim_values[i][j]) for i in range(len(sim_values)) for j in range(i+1, len(sim_values))]
        top_k = sorted(flat, key=lambda x: x[2], reverse=True)[:5]

        st.subheader("Top 5 Most Similar Node Pairs")
        for i, j, score in top_k:
            n1 = eng_df.iloc[i]["fingerprint"]
            n2 = eng_df.iloc[j]["fingerprint"]
            st.write(f" {n1} ↔ {n2} — similarity: *{score:.3f}*")

# ================== PAGE: FORENSIC SAMPLE ==================
elif page == "Forensic Sample (PCAP JSON)":
    st.header("Forensic – Parsed PCAP JSON")

    pcap_df = load_sample_pcap()
    if pcap_df is None:
        st.warning("sample_pcap.json not found in data/samples.")
    else:
        st.dataframe(pcap_df, use_container_width=True)
        #st.info("This is just a sample view. Your forensic module can integrate deeper matching later.")