import json
import os
from datetime import datetime

class PCAPParser:
    """
    Fake PCAP parser using JSON samples (no real PCAP needed)
    Converts packet logs into normalized structure:
    - src_ip, dst_ip
    - timestamp
    - protocol
    """

    def __init__(self, sample_file="data/samples/sample_pcap.json"):
        self.sample_file = sample_file

    def parse(self):
        if not os.path.exists(self.sample_file):
            raise FileNotFoundError(f"Sample PCAP file missing: {self.sample_file}")

        with open(self.sample_file, "r") as f:
            data = json.load(f)

        parsed_packets = []

        for pkt in data["packets"]:
            parsed_packets.append({
                "src_ip": pkt["src"],
                "dst_ip": pkt["dst"],
                "timestamp": datetime.fromisoformat(pkt["time"]),
                "protocol": pkt.get("protocol", "unknown")
            })

        return parsed_packets
