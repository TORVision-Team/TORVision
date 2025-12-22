import os
import sys
import streamlit as st

# -------- FIX PROJECT ROOT PATH --------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# --------------------------------------

from tor_weather_forecast.dashboard_section import tor_weather_section

st.set_page_config(page_title="TOR Weather Forecast", layout="wide")

st.title("🌦️ TOR Weather Forecasting")
st.caption("Predictive intelligence for TOR network behavior")

tor_weather_section()
