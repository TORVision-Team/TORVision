import pandas as pd
from preprocessor.feature_engineering import FeatureEngineer
from preprocessor.similarity import SimilarityEngine

# Load sample data
df = pd.read_csv("data/samples/sample_tor_nodes.csv")

# Run feature engineering
fe = FeatureEngineer()
features = fe.transform(df)

print("=== Engineered Features ===")
print(features.head())

# Save output
features.to_csv("data/samples/engineered_output.csv", index=False)

# Run similarity matrix
sim_engine = SimilarityEngine()
sim_matrix = sim_engine.calculate(features)

print("\n=== Similarity Matrix (shape) ===")
print(sim_matrix.shape)

# Save similarity matrix
pd.DataFrame(sim_matrix).to_csv("data/samples/similarity_matrix.csv", index=False)

print("\nProcessing Complete!")
