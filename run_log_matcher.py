import pandas as pd
from forensic_logs.pcap_parser import PCAPParser
from forensic_logs.log_matcher import LogMatcher
from utils.config import DATA_PATH

# Load engineered TOR features
df = pd.read_csv(f"{DATA_PATH}/engineered_output.csv")

# Parse packets
parser = PCAPParser()
packets = parser.load_packets()

# Match logs
matcher = LogMatcher(df)
results = matcher.match(packets)

print("\n=== Log Matching Results ===")
for r in results:
    print(r)

print("\nLog matching complete!")
