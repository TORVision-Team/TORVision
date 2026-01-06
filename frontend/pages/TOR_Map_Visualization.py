import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
import json
import numpy as np

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
    st.error("TOR node dataset not found")
    st.stop()

df = load_data()
st.success(f"Loaded {len(df)} TOR nodes")

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

# ---------------- COUNTRY → COORDINATES ----------------
country_coords = {
    "us": (37.0902, -95.7129),
    "de": (51.1657, 10.4515),
    "in": (20.5937, 78.9629),
    "gb": (55.3781, -3.4360),
    "fr": (46.2276, 2.2137),
    "nl": (52.1326, 5.2913),
    "it": (41.8719, 12.5674),
    "no": (60.4720, 8.4689),
}

df["country"] = df["country"].str.lower()
df["lat"] = df["country"].map(lambda c: country_coords.get(c, (np.nan, np.nan))[0])
df["lng"] = df["country"].map(lambda c: country_coords.get(c, (np.nan, np.nan))[1])

df = df.dropna(subset=["lat", "lng"])

# Limit nodes for browser safety
df = df.head(200)

# ---------------- DISPLAY TABLE ----------------
st.subheader("🔍 TOR Nodes with Confidence Levels")

st.dataframe(
    df[["nickname", "ip", "country", "flags", "confidence"]],
    use_container_width=True
)

# ---------------- GOOGLE MAP ----------------
st.subheader("🌍 TOR Node Geographical Visualization (Google Maps)")

MAPS_API_KEY = "AIzaSyDeNDTjsw2a1kb_xck2Wi1cQFms5DeQIGs"

nodes_json = df[["nickname", "lat", "lng", "confidence"]].to_dict(orient="records")
nodes_json = json.dumps(nodes_json)

html_map = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    #map {{
      height: 650px;
      width: 100%;
    }}
  </style>

  <script src="https://maps.googleapis.com/maps/api/js?key={MAPS_API_KEY}"></script>

  <script>
    const nodes = {nodes_json};

    function initMap() {{
      const map = new google.maps.Map(document.getElementById("map"), {{
        zoom: 2,
        center: {{ lat: 20, lng: 0 }}
      }});

      nodes.forEach(node => {{
        const marker = new google.maps.Marker({{
          position: {{ lat: node.lat, lng: node.lng }},
          map: map
        }});

        const info = new google.maps.InfoWindow({{
          content: `<b>${{node.nickname}}</b><br/>Confidence: ${{node.confidence}}`
        }});

        marker.addListener("click", () => {{
          info.open(map, marker);
        }});
      }});
    }}
  </script>
</head>

<body onload="initMap()">
  <div id="map"></div>
</body>
</html>
"""

components.html(html_map, height=700)
