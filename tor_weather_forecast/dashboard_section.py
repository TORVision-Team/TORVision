import streamlit as st

from tor_weather_forecast.predictor.exit_node_forecast import forecast_exit_nodes
from tor_weather_forecast.predictor.country_load_forecast import forecast_busiest_countries
from tor_weather_forecast.predictor.node_stability_predictor import predict_offline_nodes

def tor_weather_section():
    st.subheader(" TOR Weather Forecast")
    st.caption("Predicting TOR network behavior like weather")

    st.markdown("### Exit Node Growth")
    st.success(forecast_exit_nodes())

    st.markdown("###  Busiest Countries")
    st.info(forecast_busiest_countries())

    st.markdown("###  Node Stability Alerts")
    offline_nodes = predict_offline_nodes()

    if offline_nodes:
        for node in offline_nodes:
            st.warning(node)
    else:
        st.success("No nodes expected to go offline soon.")
