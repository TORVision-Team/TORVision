from datetime import datetime
import pandas as pd
import numpy as np
import pycountry

# ----------------------------------------
# 1. Normalize timestamps
# ----------------------------------------
def normalize_timestamp(ts):
    if isinstance(ts, str):
        return datetime.fromisoformat(ts)
    return ts


# ----------------------------------------
# 2. Country code → numeric ID
# ----------------------------------------
def map_country(country_code):
    if not isinstance(country_code, str):
        return 0
    try:
        c = pycountry.countries.get(alpha_2=country_code.upper())
        return list(pycountry.countries).index(c) if c else 0
    except:
        return 0


# ----------------------------------------
# 3. Bandwidth smoothing
# e.g., 0, 100, 200, 100 → 100 average
# ----------------------------------------
def smooth_bandwidth(values):
    if not isinstance(values, (list, np.ndarray, pd.Series)):
        return 0
    values = np.array(values)
    return np.mean(values)


# ----------------------------------------
# 4. Create time windows for similarity
# e.g., first_seen → hour bucket
# ----------------------------------------
def time_window(dt):
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    return dt.hour  # bucket by hour


# ----------------------------------------
# 5. Safe int conversion
# ----------------------------------------
def safe_int(value):
    try:
        return int(value)
    except:
        return 0