import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")
st.title("TOR Network – Node Confidence & Geo Visualization")

st.markdown("""
This dashboard visualizes TOR relay nodes and assigns **confidence levels**
to support **forensic and investigative analysis**.
""")

# ---------------- LOAD DATA ----------------
DATA_PATH = os.path.join("data", "real", "sample_tor_nodes.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

if not os.path.exists(DATA_PATH):
    st.error("❌ TOR node dataset not found at data/real/sample_tor_nodes.csv")
    st.stop()

df = load_data()
st.success(f"✅ Loaded {len(df)} TOR nodes")

# ---------------- CONFIDENCE LOGIC ----------------
def confidence_level(flags):
    flags = str(flags)
    if "Guard" in flags:
        return "HIGH"
    elif "Exit" in flags:
        return "MEDIUM"
    else:
        return "LOW"

df["confidence"] = df["flags"].apply(confidence_level)

# Limit nodes for demo
df = df.head(20)

# ---------------- DISPLAY TABLE ----------------
st.subheader("🔍 TOR Nodes with Confidence Levels")

st.dataframe(
    df[["nickname", "ip", "country", "flags", "confidence"]],
    use_container_width=True
)

# ---------------- GOOGLE MAP ----------------
st.subheader("🗺️ TOR Node Geographical Visualization")

MAPS_API_KEY = "AIzaSyDeNDTjsw2a1kb_xck2Wi1cQFms5DeQIGs"

html_map = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    #map {{ height: 600px; width: 100%; }}
    body {{ margin: 0; padding: 0; }}
  </style>

  <script src="https://maps.googleapis.com/maps/api/js?key={MAPS_API_KEY}"></script>

  <script>
    function initMap() {{
      var map = new google.maps.Map(document.getElementById('map'), {{
        zoom: 2,
        center: {{ lat: 20, lng: 0 }}
      }});
    }}
  </script>
</head>

<body onload="initMap()">
  <div id="map"></div>
</body>
</html>
"""

components.html(html_map, height=650)
