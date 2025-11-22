import pandas as pd
from preprocessor.similarity import SimilarityEngine

# Load engineered features
FEATURE_FILE = "data/samples/engineered_output.csv"
df = pd.read_csv(FEATURE_FILE)

print("\nLoaded engineered features:")
print(df.head())

# Initialize similarity engine
sim_engine = SimilarityEngine()

# Calculate similarity matrix
similarity_matrix = sim_engine.calculate(df)

print("\n=== Similarity Matrix Shape ===")
print(similarity_matrix.shape)

# Save similarity matrix
OUTPUT_FILE = "data/samples/similarity_matrix.csv"
pd.DataFrame(similarity_matrix).to_csv(OUTPUT_FILE, index=False)

print(f"\nSimilarity matrix saved to: {OUTPUT_FILE}")
print("\n🎉 Similarity computation completed!")
