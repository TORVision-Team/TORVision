from forensic_logs.pcap_parser import PCAPParser

parser = PCAPParser()
packets = parser.parse()

print("\n=== Parsed PCAP Packets ===")
for p in packets:
    print(p)

print("\nPCAP parsing complete!")
