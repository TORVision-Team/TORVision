import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tor_metrics_log.csv")

EXPECTED_COLS = ["timestamp", "node_id", "country", "bandwidth", "flags"]


def predict_offline_nodes():
    if not os.path.exists(DATA_PATH):
        return []

    try:
        df = pd.read_csv(DATA_PATH)

        if len(df.columns) == 5 and all(col not in EXPECTED_COLS for col in df.columns):
            df = pd.read_csv(DATA_PATH, header=None)
            df.columns = EXPECTED_COLS

        df.columns = [c.strip().lower() for c in df.columns]

        threshold = df["bandwidth"].quantile(0.1)
        risky = df[df["bandwidth"] <= threshold]

        return [
            f"Node {row['node_id']} likely to go offline soon"
            for _, row in risky.iterrows()
        ][:5]

    except Exception:
        return []
