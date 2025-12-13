# fetch_nodes.py
import requests
import pandas as pd
import os
from utils.config import (
    ONIONOO_BASE_URL,
    DATA_PATH,
    TOR_NODES_FILE,
    ENABLE_FALLBACK,
    SYNTHETIC_DATA_PATH
)

def fetch_live_tor_nodes():
    print("Fetching live Tor nodes from Onionoo...")
    url = f"{ONIONOO_BASE_URL}?type=relay&running=true"
    response = requests.get(url, timeout=15)
    response.raise_for_status()

    data = response.json()
    relays = data.get("relays", [])

    records = []
    for r in relays:
        records.append({
            "fingerprint": r.get("fingerprint"),
            "nickname": r.get("nickname"),
            "ip": r.get("or_addresses", [""])[0].split(":")[0],
            "or_port": r.get("or_port"),
            "dir_port": r.get("dir_port"),
            "country": r.get("country"),
            "flags": ",".join(r.get("flags", [])),
            "bandwidth": r.get("observed_bandwidth", 0),
            "last_seen": r.get("last_seen")
        })

    return pd.DataFrame(records)

def fallback_synthetic():
    print("[!] Falling back to synthetic dataset")
    fallback_file = os.path.join(SYNTHETIC_DATA_PATH, TOR_NODES_FILE)
    if not os.path.exists(fallback_file):
        raise FileNotFoundError("Synthetic fallback dataset not found")
    return pd.read_csv(fallback_file)

def main():
    try:
        df = fetch_live_tor_nodes()
    except Exception as e:
        print(f"Live fetch failed: {e}")
        if ENABLE_FALLBACK:
            df = fallback_synthetic()
        else:
            raise

    output_path = os.path.join(DATA_PATH, TOR_NODES_FILE)
    df.to_csv(output_path, index=False)
    print(f"Tor nodes saved to {output_path}")

if __name__ == "__main__":
    main()
