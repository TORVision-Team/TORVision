import streamlit as st
from predictor.exit_node_forecast import forecast_exit_nodes
from predictor.country_load_forecast import forecast_busiest_countries
from predictor.node_stability_predictor import predict_offline_nodes

st.set_page_config(
    page_title="TOR Weather Forecast",
    page_icon="🌩️",
    layout="centered"
)

st.title("🌩️ TOR Weather Forecast Dashboard")
st.subheader("Predicting the future of the TOR network like weather")

st.divider()

st.header("📈 Exit Node Growth Forecast")
st.success(forecast_exit_nodes())

st.divider()

st.header("🌍 Busiest Countries Forecast")
st.info(forecast_busiest_countries())

st.divider()

st.header("⚠️ Node Stability Alerts")
offline_nodes = predict_offline_nodes()

if offline_nodes:
    for node in offline_nodes:
        st.warning(node)
else:
    st.success("No nodes expected to go offline soon.")

st.divider()

st.caption("TORVision — Never-seen TOR Weather Prediction System")
