"""
hydromind/ml/lstm_crash_predictor/train_lstm.py

Trains a 2-layer LSTM on rolling 24-hour sensor windows.
Input:  ml/lstm_crash_predictor/sensor_data.csv
Output: ml/lstm_crash_predictor/lstm_model.keras  (saved Keras model)
"""

import numpy as np
import pandas as pd
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib

SEQUENCE_LEN = 288          # 24h at 5-second intervals
FEATURES     = ["temperature", "humidity", "airQuality", "waterLevel"]
BATCH_SIZE   = 64
EPOCHS       = 30
SCRIPT_DIR   = os.path.dirname(__file__)


def build_sequences(data, labels, seq_len):
    X, y = [], []
    for i in range(seq_len, len(data)):
        X.append(data[i - seq_len:i])
        y.append(labels[i])
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


def main():
    csv_path = os.path.join(SCRIPT_DIR, "sensor_data.csv")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Run generate_synthetic_data.py first. Not found: {csv_path}")

    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows. Crash ratio: {df['crash_label'].mean():.2%}")

    # Scale features
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[FEATURES])
    labels = df["crash_label"].values

    # Save scaler — needed at inference time
    scaler_path = os.path.join(SCRIPT_DIR, "scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved → {scaler_path}")

    X, y = build_sequences(scaled, labels, SEQUENCE_LEN)
    print(f"Sequences: X={X.shape}, y={y.shape}")

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(SEQUENCE_LEN, len(FEATURES))),
        Dropout(0.2),
        LSTM(64),
        Dropout(0.2),
        Dense(32, activation="relu"),
        Dense(1, activation="sigmoid"),   # crash probability
    ])

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy", tf.keras.metrics.AUC(name="auc")]
    )
    model.summary()

    checkpoint_path = os.path.join(SCRIPT_DIR, "lstm_model.keras")
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True, monitor="val_auc", mode="max"),
        ModelCheckpoint(checkpoint_path, save_best_only=True, monitor="val_auc", mode="max"),
    ]

    model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=callbacks,
        class_weight={0: 1.0, 1: 3.0},   # handle imbalance
    )

    print(f"\nModel saved → {checkpoint_path}")

    # Quick evaluation
    loss, acc, auc = model.evaluate(X_val, y_val, verbose=0)
    print(f"Val loss={loss:.4f}  acc={acc:.4f}  AUC={auc:.4f}")


if __name__ == "__main__":
    main()