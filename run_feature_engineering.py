import pandas as pd
from preprocessor.feature_engineering import FeatureEngineer
from preprocessor.similarity import SimilarityEngine
from utils.config import DATA_PATH, TOR_NODES_FILE

# Load TOR nodes (REAL or SYNTHETIC based on DATA_MODE)
input_file = f"{DATA_PATH}/{TOR_NODES_FILE}"
print(f"Loading TOR nodes from: {input_file}")
df = pd.read_csv(input_file)

if df.empty:
    print("No TOR nodes found. Run fetch_nodes.py first.")
    exit()

# Feature engineering
fe = FeatureEngineer()
features = fe.transform(df)

# Save engineered features
features_file = f"{DATA_PATH}/engineered_output.csv"
features.to_csv(features_file, index=False)
print(f"Engineered features saved to: {features_file}")