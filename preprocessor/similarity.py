import numpy as np
import pandas as pd

class SimilarityEngine:

    def calculate(self, df):
        df = df.copy()

        # Basic similarity matrix using uptime + bandwidth
        features = ['uptime_hours', 'bandwidth_norm', 'country_code']

        for feature in features:
            if feature not in df.columns:
                df[feature] = 0

        mat = df[features].to_numpy()

        # Cosine similarity
        norm = np.linalg.norm(mat, axis=1, keepdims=True)
        norm[norm == 0] = 1

        cosine_sim = (mat @ mat.T) / (norm * norm.T)
        return cosine_sim