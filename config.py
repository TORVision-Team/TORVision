# utils/config.py
import os

# =========================
# DATA MODE CONFIGURATION
# =========================
# Options: "REAL" or "SYNTHETIC"
DATA_MODE = "REAL"

# =========================
# TOR API CONFIG
# =========================
ONIONOO_BASE_URL = "https://onionoo.torproject.org/details"

# Fetch interval (hours)
FETCH_INTERVAL_HOURS = 6

# =========================
# PATH CONFIG
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REAL_DATA_PATH = os.path.join(BASE_DIR, "data", "real")
SYNTHETIC_DATA_PATH = os.path.join(BASE_DIR, "data", "samples")

DATA_PATH = REAL_DATA_PATH if DATA_MODE == "REAL" else SYNTHETIC_DATA_PATH

# =========================
# FILE NAMES
# =========================
TOR_NODES_FILE = "sample_tor_nodes.csv"
PCAP_FILE = "sample_pcap.json"

# =========================
# FALLBACK
# =========================
ENABLE_FALLBACK = True

# =========================
# DATABASE
# =========================
DB_NAME = "tor_nodes.db"

# Ensuring directories exist
os.makedirs(REAL_DATA_PATH, exist_ok=True)
os.makedirs(SYNTHETIC_DATA_PATH, exist_ok=True)
