"""
hydromind/backend/functions/daily_yield_update.py

Scheduled Cloud Function — runs every 6 hours.
Reads MQ-135 history, computes feature window, runs yield regression,
writes yieldPercent + harvestDays to /hydromind/predictions.
"""

import os
import time
import numpy as np
import joblib
import firebase_admin
from firebase_admin import db
import firebase_functions.scheduler_fn as scheduler_fn
from firebase_functions.options import SupportedRegion

if not firebase_admin._apps:
    firebase_admin.initialize_app()

SCRIPT_DIR = os.path.dirname(__file__)
WINDOW_ROWS = 72   # 6h at 5-second intervals

_yield_model   = None
_harvest_model = None


def _get_models():
    global _yield_model, _harvest_model
    if _yield_model is None:
        _yield_model   = joblib.load(os.path.join(SCRIPT_DIR, "yieldPercent_model.pkl"))
        _harvest_model = joblib.load(os.path.join(SCRIPT_DIR, "harvestDays_model.pkl"))
    return _yield_model, _harvest_model


def _compute_features(aq_values: list) -> np.ndarray:
    """Extract the 5 statistical features the model was trained on."""
    arr = np.array(aq_values, dtype=float)
    mean_aq  = float(np.mean(arr))
    std_aq   = float(np.std(arr))
    min_aq   = float(np.min(arr))
    max_aq   = float(np.max(arr))
    # Linear trend: slope of air quality over the window
    x = np.arange(len(arr))
    trend_aq = float(np.polyfit(x, arr, 1)[0]) if len(arr) > 1 else 0.0
    return np.array([[mean_aq, std_aq, min_aq, max_aq, trend_aq]])


@scheduler_fn.on_schedule(
    schedule="every 6 hours",
    region=SupportedRegion.ASIA_SOUTHEAST1
)
def daily_yield_update(event):
    """Fetch 6h MQ-135 history, predict yield and harvest days."""
    try:
        history_ref = db.reference("/hydromind/sensor_history")
        history_data = history_ref.order_by_key().limit_to_last(WINDOW_ROWS).get()

        if not history_data or len(history_data) < 10:
            print("Not enough sensor history for yield prediction. Skipping.")
            return

        aq_values = [row.get("airQuality", 300) for row in history_data.values()]
        features  = _compute_features(aq_values)

        yield_model, harvest_model = _get_models()
        yield_pct    = float(yield_model.predict(features)[0])
        harvest_days = int(round(harvest_model.predict(features)[0]))

        yield_pct    = max(0.0, min(100.0, yield_pct))
        harvest_days = max(0, min(60, harvest_days))

        print(f"Yield: {yield_pct:.1f}%  Harvest in: {harvest_days} days")

        db.reference("/hydromind/predictions").update({
            "yieldPercent": round(yield_pct, 1),
            "harvestDays":  harvest_days,
            "updatedAt":    int(time.time() * 1000),
        })

    except Exception as e:
        print(f"[daily_yield_update] ERROR: {e}")
        raise