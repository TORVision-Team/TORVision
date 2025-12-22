from predictor.exit_node_forecast import forecast_exit_nodes
from predictor.country_load_forecast import forecast_busiest_countries
from predictor.node_stability_predictor import predict_offline_nodes

def run_dashboard():
    print("\n===== TOR WEATHER FORECAST DASHBOARD =====\n")

    print(">>> Exit Node Growth Forecast:")
    print(forecast_exit_nodes())
    print("\n----------------------------------------\n")

    print(">>> Busiest Countries Forecast:")
    print(forecast_busiest_countries())
    print("\n----------------------------------------\n")

    print(">>> Nodes Likely to Go Offline:")
    print(predict_offline_nodes())
    print("\n========================================\n")

if __name__ == "__main__":
    run_dashboard()

