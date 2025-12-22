import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "tor_metrics_log.csv")

EXPECTED_COLS = ["timestamp", "node_id", "country", "bandwidth", "flags"]


def forecast_busiest_countries():
    if not os.path.exists(DATA_PATH):
        return "Forecast: TOR metrics unavailable."

    try:
        df = pd.read_csv(DATA_PATH)

        if len(df.columns) == 5 and all(col not in EXPECTED_COLS for col in df.columns):
            df = pd.read_csv(DATA_PATH, header=None)
            df.columns = EXPECTED_COLS

        df.columns = [c.strip().lower() for c in df.columns]

        if "country" not in df.columns:
            return f"Forecast: Invalid TOR metrics format. Columns found: {list(df.columns)}"

        top = df["country"].value_counts().head(3).index.tolist()

        return (
            "Forecast: "
            + ", ".join(top)
            + " will be the busiest TOR exit hubs in the next few hours."
        )

    except Exception as e:
        return f"Forecast error: {str(e)}"
