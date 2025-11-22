class LogMatcher:
    """
    Matches parsed PCAP data with TOR nodes.
    """

    def __init__(self, tor_df):
        self.tor_df = tor_df

    def match(self, pcap_packets):
        matches = []

        for pkt in pcap_packets:
            # Match TOR node IPs
            hit = self.tor_df[self.tor_df["ip"] == pkt["src_ip"]]

            if not hit.empty:
                matches.append({
                    "src_ip": pkt["src_ip"],
                    "matched_node": hit.iloc[0]["fingerprint"],
                    "time": pkt["timestamp"],
                    "protocol": pkt["protocol"]
                })

        return matches
