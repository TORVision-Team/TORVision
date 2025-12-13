# run_similarity.py
import os
import pandas as pd
from preprocessor.similarity import SimilarityEngine
from utils.config import DATA_PATH

def main():
    FEATURE_FILE = os.path.join(DATA_PATH, "engineered_output.csv")
    OUTPUT_FILE = os.path.join(DATA_PATH, "similarity_matrix.csv")

    print(f"\nLoading engineered features from: {FEATURE_FILE}")

    # Check if engineered features exist
    if not os.path.exists(FEATURE_FILE):
        print("engineered_output.csv not found.")
        print("Run run_feature_engineering.py on REAL TOR data first.")
        return

    df = pd.read_csv(FEATURE_FILE)

    if df.empty:
        print("Engineered features file is empty.")
        return

    print("\nLoaded engineered features (preview):")
    print(df.head())

    # Initialize similarity engine
    sim_engine = SimilarityEngine()

    # Calculate similarity matrix
    similarity_matrix = sim_engine.calculate(df)

    # Save similarity matrix
    pd.DataFrame(similarity_matrix).to_csv(OUTPUT_FILE, index=False)

    print(f"\nSimilarity matrix saved to: {OUTPUT_FILE}")
    print("Similarity computation completed successfully")

if __name__ == "__main__":
    main()
