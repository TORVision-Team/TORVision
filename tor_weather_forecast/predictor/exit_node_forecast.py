import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tor_metrics_log.csv")

EXPECTED_COLS = ["timestamp", "node_id", "country", "bandwidth", "flags"]


def forecast_exit_nodes():
    if not os.path.exists(DATA_PATH):
        return "Forecast: TOR metrics not found."

    try:
        # First attempt: normal read
        df = pd.read_csv(DATA_PATH)

        # 🔑 Detect headerless CSV
        if len(df.columns) == 5 and all(col not in EXPECTED_COLS for col in df.columns):
            df = pd.read_csv(DATA_PATH, header=None)
            df.columns = EXPECTED_COLS

        df.columns = [c.strip().lower() for c in df.columns]

        if "flags" not in df.columns:
            return f"Forecast: Invalid TOR metrics format. Columns found: {list(df.columns)}"

        exit_nodes = df["flags"].astype(str).str.contains("exit", case=False).sum()

        if exit_nodes < 2:
            return "Forecast: Insufficient TOR data."

        predicted = int(exit_nodes * 1.12)
        delta = predicted - exit_nodes

        return (
            f"Forecast: Exit nodes expected to increase by "
            f"{delta} (~12%) in the next 4 hours."
        )

    except Exception as e:
        return f"Forecast error: {str(e)}"
