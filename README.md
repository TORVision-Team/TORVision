🕸️ TORVision
An Analytical System for TOR Node Correlation, Origin Prediction & Forensic Intelligence

TORVision is an advanced metadata-driven analysis platform designed to help investigators understand TOR relay behavior, identify likely entry/guard nodes, visualize network flows, and correlate forensic logs — without breaking TOR encryption.

The system uses public metadata, ML-based scoring, graph correlation, timeline replay, weather forecasting, and suspicious activity alerts to deliver actionable intelligence.

🚀 Key Features
🔹 1. TOR Data Collection

Automatic extraction of TOR relay metadata using Onionoo API

Periodic scheduled updates

Stores historical snapshots (for forecasting & trend analysis)

🔹 2. Node Correlation Engine

Time-based matching of entry → middle → exit nodes

Similarity scoring based on timestamps, bandwidth & flags

Graph-based correlation using NetworkX

🔹 3. ML-Based Origin Prediction

Predicts likely entry/guard nodes

Confidence scoring model (Decision Tree / RandomForest)

Continuously improves as new data is fetched

🔹 4. Visualization Dashboard

Interactive relay map

Network graph animation

Timeline reconstruction

Confidence meter display

Forensic match overlay

🔹 5. Forensic Log Integration

Upload PCAP or network logs

Extract suspicious IPs & timestamps

Match against TOR relay database

Highlight overlapping or suspicious nodes

🔹 6. TOR Weather Forecasting ⭐ Unique Feature

Predicts:

Future number of exit nodes

Country-wise activity trends

Node stability probability

Possible outages

Example:
“Forecast: Exit nodes in Europe likely to increase by 12% in next 4 hours.”

🔹 7. Suspicious Activity Alerts

The system automatically detects:

Sudden drop in relay counts

Country-based spikes

Over-stable nodes (possible surveillance)

Bandwidth anomalies

Exit node bursts# TORVision
