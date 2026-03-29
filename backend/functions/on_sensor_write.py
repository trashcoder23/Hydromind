"""
hydromind/backend/functions/on_sensor_write.py  [UPDATED]

Triggered every time ESP8266 writes to /hydromind/sensor_data.
  1. Appends row to /hydromind/sensor_history (rolling buffer).
  2. Fetches last SEQUENCE_LEN rows.
  3. Runs LSTM ONNX model → crash probability + hours to failure.
  4. Writes prediction to /hydromind/predictions.
  5. If crash_probability > 0.7, sends FCM push + logs alert.
  6. If waterLevel < 20, sends water-low FCM.
"""

import os
import time
import numpy as np
import onnxruntime as ort
import joblib
import firebase_admin
from firebase_admin import db, messaging
import firebase_functions.db_fn as db_fn
from firebase_functions.options import SupportedRegion
from sensor_history_writer import append_sensor_history
from sensor_history_writer import append_sensor_history

# ── Constants ───────────────────────────────────────────────
SEQUENCE_LEN    = 288
FEATURES        = ["temperature", "humidity", "airQuality", "waterLevel"]
CRASH_THRESHOLD = 0.7
WATER_LOW_PCT   = 20.0
SCRIPT_DIR      = os.path.dirname(__file__)

# ── Firebase Admin init (idempotent) ────────────────────────
if not firebase_admin._apps:
    firebase_admin.initialize_app()

# ── Lazy-loaded model + scaler ──────────────────────────────
_session = None
_scaler  = None

def _sess():
    global _session
    if _session is None:
        _session = ort.InferenceSession(os.path.join(SCRIPT_DIR, "model.onnx"))
    return _session

def _sc():
    global _scaler
    if _scaler is None:
        _scaler = joblib.load(os.path.join(SCRIPT_DIR, "scaler.pkl"))
    return _scaler


# ── Cloud Function ───────────────────────────────────────────
@db_fn.on_value_written(
    reference="/hydromind/sensor_data",
    region=SupportedRegion.ASIA_SOUTHEAST1
)
def on_sensor_write(event):
    new_val = event.data.after.val()
    if not new_val:
        return
    try:
        # 1. Persist to history
        append_sensor_history(new_val)

        # 2. Run LSTM
        crash_prob, hours = _run_lstm()

        # 3. Write predictions
        db.reference("/hydromind/predictions").update({
            "crashProbability": round(crash_prob, 4),
            "hoursToFailure":   round(hours, 1),
            "updatedAt":        int(time.time() * 1000),
        })

        # 4. Crash alert
        if crash_prob > CRASH_THRESHOLD:
            _send_fcm(
                title="⚠️ HydroMind — Crash Predicted",
                body=f"Crash likely in ~{hours:.0f}h. Probability: {crash_prob*100:.0f}%",
                data={"type": "crash_predicted",
                      "crashProbability": str(round(crash_prob, 4)),
                      "hoursToFailure":   str(round(hours, 1))},
            )
            _log_alert("crash_predicted", {
                "crashProbability": crash_prob,
                "hoursToFailure":   hours,
            })

        # 5. Water-low alert
        water = float(new_val.get("waterLevel", 100))
        if water < WATER_LOW_PCT:
            _send_fcm(
                title="💧 HydroMind — Water Low",
                body=f"Reservoir at {water:.0f}%. Refill needed.",
                data={"type": "water_low", "waterLevel": str(water)},
            )
            _log_alert("water_low", {"waterLevel": water})

        # 6. Autonomous CIRC command when water is critically low
        if water < 10:
            db.reference("/hydromind/commands/pending").set("CIRC_ON")

    except Exception as e:
        print(f"[on_sensor_write] ERROR: {e}")
        raise


def _run_lstm():
    history_ref  = db.reference("/hydromind/sensor_history")
    history_data = history_ref.order_by_key().limit_to_last(SEQUENCE_LEN).get()

    if not history_data:
        return 0.0, 48.0

    rows = list(history_data.values())
    while len(rows) < SEQUENCE_LEN:
        rows.insert(0, {f: 0.0 for f in FEATURES})

    raw    = np.array([[r.get(f, 0.0) for f in FEATURES] for r in rows[-SEQUENCE_LEN:]], dtype=np.float32)
    scaled = _sc().transform(raw)
    X      = scaled.reshape(1, SEQUENCE_LEN, len(FEATURES)).astype(np.float32)

    inp    = _sess().get_inputs()[0].name
    result = _sess().run(None, {inp: X})
    prob   = float(result[0][0][0])
    hours  = max(0.0, 48.0 * (1.0 - prob) / 0.3) if prob >= CRASH_THRESHOLD else 48.0
    return prob, hours


def _send_fcm(title: str, body: str, data: dict):
    try:
        messaging.send(messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            topic="hydromind_alerts",
            data=data,
            android=messaging.AndroidConfig(priority="high"),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(aps=messaging.Aps(sound="default"))
            ),
        ))
    except Exception as e:
        print(f"FCM send failed: {e}")


def _log_alert(alert_type: str, data: dict):
    db.reference("/hydromind/alerts").push({
        "type":      alert_type,
        "timestamp": int(time.time() * 1000),
        "data":      data,
    })