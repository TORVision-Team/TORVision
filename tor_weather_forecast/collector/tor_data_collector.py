import pandas as pd
import random
from datetime import datetime
import os

COUNTRIES = ["DE", "NL", "FR", "US", "SE", "FI", "IN"]
FLAGS = ["Exit", "Guard", "Stable"]

CSV_PATH = "data/tor_metrics_log.csv"

def generate_fake_tor_data(n=50):
    rows = []
    for _ in range(n):
        rows.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fingerprint": f"node-{random.randint(1000,9999)}",
            "country": random.choice(COUNTRIES),
            "bandwidth": random.randint(50, 1000),
            "flags": ",".join(random.sample(FLAGS, random.randint(1, 3)))
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    df = generate_fake_tor_data()

    # Append if file exists, else create with headers
    if os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, mode="a", index=False, header=False)
    else:
        df.to_csv(CSV_PATH, index=False)

    print("✔ TOR sample data collected (syntax fixed)")
