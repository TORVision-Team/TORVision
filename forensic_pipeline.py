"""
Forensic Pipeline
=================

This module connects all forensic components:
- Loads TOR node metadata
- Parses sample PCAP packets
- Matches packets with TOR nodes
- Produces a final correlated forensic report
"""

import pandas as pd

from forensic_logs.pcap_parser import PCAPParser
from forensic_logs.log_matcher import LogMatcher


def load_tor_nodes(csv_path="data/samples/sample_tor_nodes.csv"):
    """
    Loads TOR relay metadata needed for matching.
    """
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError("TOR nodes file missing. Expected at: data/samples/sample_tor_nodes.csv")


def run_forensic_pipeline():
    print("\n🚀 Running Forensic Analysis Pipeline...\n")

    # 1. Load TOR relay metadata
    print("📌 Loading TOR nodes...")
    tor_df = load_tor_nodes()

    # 2. Parse packet logs
    print("📌 Parsing PCAP sample packets...")
    parser = PCAPParser()              # uses default sample file
    packets = parser.parse()

    # 3. Match packets to TOR nodes
    print("📌 Matching packets with TOR nodes...")
    matcher = LogMatcher(tor_df)
    matches = matcher.match(packets)

    # 4. Build DataFrame output
    print("📌 Building report...")

    if matches:
        df = pd.DataFrame(matches)
        df.to_csv("forensic_output.csv", index=False)
        print("\n✅ Forensic output saved as forensic_output.csv")
        print("\n🔍 Matched Entries:")
        print(df)
    else:
        print("\n❌ No matches found in packets.")


if __name__ == "__main__":
    run_forensic_pipeline()
