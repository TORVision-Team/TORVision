import os
import sys

# ---------------- FIX PYTHON PATH (VERY IMPORTANT) ----------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
# -----------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
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
        "Forensic Sample (PCAP JSON)"
    ]
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
        rows, cols = sim_values.shape

        # Remove self-similarity safely
        for i in range(min(rows, cols)):
            sim_values[i, i] = 0

        # ---- SAFE max similarity extraction ----
        max_idx = np.unravel_index(np.argmax(sim_values), sim_values.shape)
        score = sim_values[max_idx]

        r, c = max_idx

        # Guard against mismatch with engineered dataframe
        if r < len(eng_df) and c < len(eng_df):
            n1 = eng_df.iloc[r]["fingerprint"]
            n2 = eng_df.iloc[c]["fingerprint"]
        else:
            n1 = f"Index {r}"
            n2 = f"Index {c}"

        # ---- UI OUTPUT ----
        st.subheader("Most Similar Node Pair")
        st.success(f"{n1} ↔ {n2}")
        st.metric("Similarity Score", f"{score:.3f}")

        st.subheader("Similarity Analysis Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Nodes Analyzed", len(eng_df))
        with col2:
            st.metric("Similarity Matrix Size", f"{rows} × {cols}")

        st.info(
            f"Similarity computed on a subset of {min(rows, cols)} nodes for scalability."
        )

        # -------- Top 5 Most Similar Node Pairs (SAFE) --------
        flat = []
        for i in range(rows):
            for j in range(cols):
                if i != j:  # ignore self-similarity
                    flat.append((i, j, sim_values[i][j]))

        top_k = sorted(flat, key=lambda x: x[2], reverse=True)[:5]

        st.subheader("Top 5 Most Similar Node Pairs")
        for i, j, score in top_k:
            n1 = eng_df.iloc[i]["fingerprint"] if i < len(eng_df) else f"Index {i}"
            n2 = eng_df.iloc[j]["fingerprint"] if j < len(eng_df) else f"Index {j}"
            st.write(f"**{n1}** ↔ **{n2}** — similarity: *{score:.3f}*")

# ================== FORENSIC ==================
elif page == "Forensic Sample (PCAP JSON)":
    st.header("Forensic – Parsed PCAP Data")

    pcap_df = load_sample_pcap()
    if pcap_df is None:
        st.warning("PCAP data not found.")
    else:
        st.dataframe(pcap_df, use_container_width=True)
