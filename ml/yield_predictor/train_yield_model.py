"""
hydromind/ml/yield_predictor/train_yield_model.py

Trains a gradient boosting regressor on CO2 (MQ-135) history
to predict yield percentage and days to harvest.

Output: ml/models/yield_model.pkl
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
import os

SCRIPT_DIR  = os.path.dirname(__file__)
OUTPUT_DIR  = os.path.join(SCRIPT_DIR, "..", "models")
SEED        = 42
N_SAMPLES   = 5000


def generate_yield_data(n=N_SAMPLES):
    """
    Synthetic dataset. Each row = one 6-hour window of MQ-135 readings.
    Features: mean, std, min, max, trend of air quality over 6h window.
    Targets:  yieldPercent (0-100), harvestDays (0-60).
    """
    np.random.seed(SEED)
    rows = []

    for _ in range(n):
        growth_stage = np.random.uniform(0, 1)      # 0 = seedling, 1 = harvest
        base_co2     = 300 + 200 * growth_stage      # more photosynthesis = higher CO2 uptake proxy
        noise        = np.random.normal(0, 20)

        mean_aq  = base_co2 + noise
        std_aq   = np.random.uniform(10, 60)
        min_aq   = mean_aq - std_aq * 0.5
        max_aq   = mean_aq + std_aq * 0.5
        trend_aq = np.random.uniform(-5, 5)          # rate of change per hour

        yield_pct    = growth_stage * 100 + np.random.normal(0, 3)
        harvest_days = int((1 - growth_stage) * 60 + np.random.randint(-2, 3))

        yield_pct    = np.clip(yield_pct, 0, 100)
        harvest_days = np.clip(harvest_days, 0, 60)

        rows.append([mean_aq, std_aq, min_aq, max_aq, trend_aq, yield_pct, harvest_days])

    df = pd.DataFrame(rows, columns=[
        "mean_aq", "std_aq", "min_aq", "max_aq", "trend_aq",
        "yieldPercent", "harvestDays"
    ])
    return df


def main():
    df = generate_yield_data()
    print(f"Generated {len(df)} training rows")

    features = ["mean_aq", "std_aq", "min_aq", "max_aq", "trend_aq"]
    X = df[features].values

    # Train two separate regressors
    for target in ["yieldPercent", "harvestDays"]:
        y = df[target].values
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=SEED)

        model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            random_state=SEED,
        )
        model.fit(X_train, y_train)
        preds = model.predict(X_val)
        mae = mean_absolute_error(y_val, preds)
        print(f"{target}: MAE = {mae:.2f}")

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_path = os.path.join(OUTPUT_DIR, f"{target}_model.pkl")
        joblib.dump(model, out_path)
        print(f"Saved → {out_path}")


if __name__ == "__main__":
    main()