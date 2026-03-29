"""
hydromind/backend/functions/sensor_history_writer.py

Helper imported by on_sensor_write.py.
Appends the latest sensor reading to /hydromind/sensor_history
and trims it to the last MAX_HISTORY entries so Firebase doesn't grow unbounded.

This is NOT a standalone Cloud Function — it is called inside on_sensor_write.
"""

import time
import firebase_admin
from firebase_admin import db

MAX_HISTORY = 2016   # 7 days at 5-second intervals = 7*24*60*12 = 10080;
                     # keep 7 days but trim to last 2016 (1 week at 5-second = ~1.4 days)
                     # For MVP demo: 2016 rows is ~2.8 hours — enough for LSTM window


def append_sensor_history(sensor_data: dict):
    """
    Push one sensor row into /hydromind/sensor_history.
    Trim oldest entries beyond MAX_HISTORY.
    Called from on_sensor_write before LSTM inference.
    """
    history_ref = db.reference("/hydromind/sensor_history")

    # Push new row
    history_ref.push({
        "temperature": sensor_data.get("temperature", 0),
        "humidity":    sensor_data.get("humidity", 0),
        "airQuality":  sensor_data.get("airQuality", 0),
        "waterLevel":  sensor_data.get("waterLevel", 0),
        "vibration":   sensor_data.get("vibration", 0),
        "healthScore": sensor_data.get("healthScore", 0),
        "timestamp":   sensor_data.get("timestamp", int(time.time() * 1000)),
    })

    # Trim: count current entries, delete oldest if over limit
    snapshot = history_ref.order_by_key().get()
    if snapshot and len(snapshot) > MAX_HISTORY:
        keys_sorted = sorted(snapshot.keys())
        keys_to_delete = keys_sorted[:len(snapshot) - MAX_HISTORY]
        for key in keys_to_delete:
            history_ref.child(key).delete()