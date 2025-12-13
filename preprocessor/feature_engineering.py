import pandas as pd

class FeatureEngineer:

    def _init_(self):
        pass  # No data needed during initialization

    def transform(self, df):
        df = df.copy()

        # ─────────────── Basic Features ───────────────
        # Uptime in hours
        if 'uptime' in df.columns:
            df['uptime_hours'] = df['uptime'] / 3600
        else:
            df['uptime_hours'] = 0

        # Exit / Middle flags
        if 'flags' in df.columns:
            df['is_exit'] = df['flags'].apply(lambda x: 1 if 'Exit' in str(x) else 0)
            df['is_middle'] = df['flags'].apply(lambda x: 1 if 'Middle' in str(x) else 0)
        else:
            df['is_exit'] = 0
            df['is_middle'] = 0

        # Country encoding
        if 'country' in df.columns:
            df['country_code'] = df['country'].astype('category').cat.codes
        else:
            df['country_code'] = -1

        # Bandwidth normalization
        if 'bandwidth' in df.columns:
            bw_min = df['bandwidth'].min()
            bw_max = df['bandwidth'].max()
            df['bandwidth_norm'] = (df['bandwidth'] - bw_min) / (bw_max - bw_min + 1e-9)
        else:
            df['bandwidth_norm'] = 0

        return df