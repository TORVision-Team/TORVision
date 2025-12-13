# forensic_pipeline.py
import pandas as pd
import os
from utils.config import DATA_PATH, TOR_NODES_FILE

def load_tor_nodes(csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(DATA_PATH, TOR_NODES_FILE)

    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"TOR nodes file missing at {csv_path}")

def run_forensics():
    tor_nodes = load_tor_nodes()
    print(f"Loaded {len(tor_nodes)} Tor nodes for analysis")

if __name__ == "__main__":
    run_forensics()
