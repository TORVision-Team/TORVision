import pandas as pd
from forensic_logs.pcap_parser import PCAPParser
from forensic_logs.log_matcher import LogMatcher

# Load engineered TOR features
df = pd.read_csv("data/samples/engineered_output.csv")

# Parse packets
parser = PCAPParser()
packets = parser.parse()

# Match logs
matcher = LogMatcher(df)
results = matcher.match(packets)

print("\n=== Log Matching Results ===")
for r in results:
    print(r)

print("\nLog matching complete!")
