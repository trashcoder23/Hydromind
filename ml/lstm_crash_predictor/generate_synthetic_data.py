"""
hydromind/ml/lstm_crash_predictor/generate_synthetic_data.py

Generates synthetic hydroponic sensor data for LSTM training.
Outputs: ml/lstm_crash_predictor/sensor_data.csv
"""

import numpy as np
import pandas as pd
import os

SEED = 42
np.random.seed(SEED)

SAMPLES_PER_CYCLE = 1440   # 5-second intervals over 2 hours = 1440 rows per "day"
NUM_NORMAL_CYCLES = 60
NUM_ANOMALY_CYCLES = 30
SEQUENCE_LEN = 288          # 24-hour rolling window at 5s intervals = 288 per cycle

def generate_normal_cycle(n=SAMPLES_PER_CYCLE):
    t = np.linspace(0, 1, n)
    temp      = 24 + 3 * np.sin(2 * np.pi * t) + np.random.normal(0, 0.3, n)
    humidity  = 60 + 10 * np.sin(2 * np.pi * t + 1) + np.random.normal(0, 1, n)
    air       = 300 + 50 * np.sin(2 * np.pi * t) + np.random.normal(0, 10, n)
    water     = 75 - 5 * t + np.random.normal(0, 0.5, n)   # slow drain
    label     = np.zeros(n)
    return temp, humidity, air, water, label

def generate_anomaly_cycle(n=SAMPLES_PER_CYCLE, anomaly_type=None):
    t = np.linspace(0, 1, n)
    temp      = 24 + 3 * np.sin(2 * np.pi * t) + np.random.normal(0, 0.3, n)
    humidity  = 60 + 10 * np.sin(2 * np.pi * t + 1) + np.random.normal(0, 1, n)
    air       = 300 + 50 * np.sin(2 * np.pi * t) + np.random.normal(0, 10, n)
    water     = 75 - 5 * t + np.random.normal(0, 0.5, n)
    label     = np.zeros(n)

    anomaly_start = int(n * 0.5)   # anomaly starts at 50% of cycle
    label[anomaly_start:] = 1

    if anomaly_type == "nutrient_crash" or anomaly_type is None:
        # EC crash → temp spikes, humidity drops
        temp[anomaly_start:]     += np.linspace(0, 8, n - anomaly_start)
        humidity[anomaly_start:] -= np.linspace(0, 20, n - anomaly_start)

    elif anomaly_type == "ph_drift":
        # pH drift → air quality spikes (VOC proxy)
        air[anomaly_start:] += np.linspace(0, 350, n - anomaly_start)

    elif anomaly_type == "water_low":
        # Reservoir draining fast
        water[anomaly_start:] -= np.linspace(0, 60, n - anomaly_start)
        water = np.clip(water, 0, 100)

    elif anomaly_type == "pump_fault":
        # Pump stops → temp builds, humidity rises
        temp[anomaly_start:]     += np.linspace(0, 6, n - anomaly_start)
        humidity[anomaly_start:] += np.linspace(0, 15, n - anomaly_start)

    return temp, humidity, air, water, label


def main():
    rows = []

    for _ in range(NUM_NORMAL_CYCLES):
        temp, hum, air, water, lbl = generate_normal_cycle()
        for i in range(len(temp)):
            rows.append([temp[i], hum[i], air[i], water[i], lbl[i]])

    anomaly_types = ["nutrient_crash", "ph_drift", "water_low", "pump_fault", None]
    for i in range(NUM_ANOMALY_CYCLES):
        atype = anomaly_types[i % len(anomaly_types)]
        temp, hum, air, water, lbl = generate_anomaly_cycle(anomaly_type=atype)
        for j in range(len(temp)):
            rows.append([temp[j], hum[j], air[j], water[j], lbl[j]])

    df = pd.DataFrame(rows, columns=["temperature", "humidity", "airQuality", "waterLevel", "crash_label"])

    # Clip to realistic sensor ranges
    df["temperature"] = df["temperature"].clip(10, 45)
    df["humidity"]    = df["humidity"].clip(10, 100)
    df["airQuality"]  = df["airQuality"].clip(0, 1023)
    df["waterLevel"]  = df["waterLevel"].clip(0, 100)

    out_path = os.path.join(os.path.dirname(__file__), "sensor_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {len(df)} rows → {out_path}")
    print(f"Crash ratio: {df['crash_label'].mean():.2%}")


if __name__ == "__main__":
    main()