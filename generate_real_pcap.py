# generate_real_pcap.py
import pandas as pd
import json
from datetime import datetime, timedelta
import random
from utils.config import DATA_PATH, PCAP_FILE

# Load real TOR nodes
df = pd.read_csv(f"{DATA_PATH}/sample_tor_nodes.csv")

packets = []
for i in range(50):  # generate 50 sample packets
    node = df.sample(1).iloc[0]
    packets.append({
        "src_ip": node["ip"],
        "dst_ip": f"10.0.{random.randint(1,255)}.{random.randint(1,255)}",
        "protocol": random.choice(["TCP", "UDP"]),
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(0,60))).isoformat()
    })

# Save JSON to REAL_DATA_PATH
with open(f"{DATA_PATH}/{PCAP_FILE}", "w") as f:
    json.dump(packets, f, indent=4)

print(f"Real PCAP JSON saved to {DATA_PATH}/{PCAP_FILE}")