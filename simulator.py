"""
hydromind/simulator.py

Hardware simulator — pushes fake sensor readings to Firebase
so you can develop and demo the full software stack without
the Arduino/ESP8266 physically connected.

Usage:
    pip install firebase-admin
    python simulator.py                   # normal healthy cycle
    python simulator.py --anomaly aq      # spike air quality (Demo Moment 1)
    python simulator.py --anomaly water   # drain water level (Demo Moment 2)
    python simulator.py --anomaly temp    # temperature crash
    python simulator.py --anomaly all     # random anomaly injection

Press Ctrl+C to stop.
"""

import argparse
import math
import random
import time
import firebase_admin
from firebase_admin import credentials, db

# ── CONFIG — fill these in ──────────────────────────────────
DATABASE_URL = "https://hydromind-f4ee5-default-rtdb.asia-southeast1.firebasedatabase.app"
# For local testing use a service account JSON:
SERVICE_ACCOUNT_JSON = "serviceAccountKey.json"  # Place the key file in hydromind/ folder
# ────────────────────────────────────────────────────────────

INTERVAL_SECONDS = 5   # match Arduino's 5-second send rate


def compute_health_score(temp, humidity, air_quality, water_level):
    score = 100
    if not (18 <= temp <= 30):      score -= 25
    if not (40 <= humidity <= 80):  score -= 20
    if air_quality >= 600:          score -= 30
    if water_level <= 20:           score -= 25
    return max(0, score)


def normal_reading(t: float):
    """Smooth sinusoidal healthy baseline."""
    temp        = 24 + 3 * math.sin(t * 0.05) + random.gauss(0, 0.2)
    humidity    = 60 + 8 * math.sin(t * 0.03 + 1) + random.gauss(0, 0.5)
    air_quality = int(320 + 40 * math.sin(t * 0.02) + random.gauss(0, 8))
    water_level = max(20, 80 - (t * 0.01))    # slow drain over time
    vibration   = 0
    return temp, humidity, air_quality, water_level, vibration


def anomaly_aq(t: float, step: int):
    """Demo Moment 1 — spike air quality to simulate deodorant spray."""
    temp, hum, _, water, vib = normal_reading(t)
    # Spike that lingers for ~10 readings then decays
    spike = max(0, 700 - step * 30) if step < 30 else 0
    air_quality = int(320 + spike + random.gauss(0, 10))
    return temp, hum, air_quality, water, vib


def anomaly_water(t: float, step: int):
    """Demo Moment 2 — drain reservoir quickly."""
    temp, hum, air, _, vib = normal_reading(t)
    water_level = max(0, 80 - step * 4)   # drops 4% per tick
    return temp, hum, air, water_level, vib


def anomaly_temp(t: float, step: int):
    """Rising temperature crash."""
    _, hum, air, water, vib = normal_reading(t)
    temp = 24 + step * 0.5 + random.gauss(0, 0.3)   # climbs 0.5°C per tick
    return temp, hum, air, water, vib


def anomaly_all(t: float, step: int):
    """Random anomaly injection — hits a random sensor each cycle."""
    choice = step % 3
    if choice == 0:   return anomaly_aq(t, step)
    if choice == 1:   return anomaly_water(t, step)
    return anomaly_temp(t, step)


def push_reading(sensor_ref, history_ref, temp, humidity, air_quality, water_level, vibration):
    score = compute_health_score(temp, humidity, air_quality, water_level)
    ts    = int(time.time() * 1000)

    payload = {
        "temperature": round(temp, 1),
        "humidity":    round(humidity, 1),
        "airQuality":  int(air_quality),
        "waterLevel":  round(water_level, 1),
        "vibration":   int(vibration),
        "healthScore": score,
        "timestamp":   ts,
    }

    sensor_ref.set(payload)
    history_ref.push(payload)

    status = "🟢 OK" if score >= 70 else "🟡 WARN" if score >= 40 else "🔴 CRITICAL"
    print(
        f"[{time.strftime('%H:%M:%S')}] {status}  "
        f"T={temp:.1f}°C  H={humidity:.1f}%  "
        f"AQ={air_quality}  W={water_level:.1f}%  "
        f"Score={score}"
    )


def main():
    parser = argparse.ArgumentParser(description="HydroMind sensor simulator")
    parser.add_argument(
        "--anomaly",
        choices=["aq", "water", "temp", "all"],
        default=None,
        help="Inject anomaly type (default: normal healthy cycle)"
    )
    args = parser.parse_args()

    # Init Firebase
    if SERVICE_ACCOUNT_JSON:
        cred = credentials.Certificate(SERVICE_ACCOUNT_JSON)
        firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})
    else:
        firebase_admin.initialize_app(options={"databaseURL": DATABASE_URL})

    sensor_ref  = db.reference("/hydromind/sensor_data")
    history_ref = db.reference("/hydromind/sensor_history")

    mode_label = args.anomaly or "normal"
    print(f"\n🌱 HydroMind Simulator — mode: {mode_label}")
    print(f"   Pushing to: {DATABASE_URL}")
    print(f"   Interval:   {INTERVAL_SECONDS}s\n")
    print("Press Ctrl+C to stop.\n")

    t    = 0.0
    step = 0

    anomaly_fn = {
        "aq":    anomaly_aq,
        "water": anomaly_water,
        "temp":  anomaly_temp,
        "all":   anomaly_all,
    }.get(args.anomaly)

    try:
        while True:
            if anomaly_fn:
                readings = anomaly_fn(t, step)
            else:
                readings = normal_reading(t)

            push_reading(sensor_ref, history_ref, *readings)

            time.sleep(INTERVAL_SECONDS)
            t    += INTERVAL_SECONDS
            step += 1

    except KeyboardInterrupt:
        print("\n\nSimulator stopped.")


if __name__ == "__main__":
    main()