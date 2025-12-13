# pcap_parser.py
import json
import os
from utils.config import DATA_PATH, PCAP_FILE

class PCAPParser:
    def __init__(self, sample_file=None):
        if sample_file is None:
            self.sample_file = os.path.join(DATA_PATH, PCAP_FILE)
        else:
            self.sample_file = sample_file

    def load_packets(self):
        if not os.path.exists(self.sample_file):
            raise FileNotFoundError(f"PCAP file not found: {self.sample_file}")

        with open(self.sample_file, "r") as f:
            return json.load(f)
