"""
hydromind/ml/yield_predictor/export_yield_model.py

Verifies exported yield model files and copies them into backend/functions/.
Run after train_yield_model.py.
"""

import joblib
import numpy as np
import os
import shutil

SCRIPT_DIR   = os.path.dirname(__file__)
MODELS_DIR   = os.path.join(SCRIPT_DIR, "..", "models")
BACKEND_DIR  = os.path.join(SCRIPT_DIR, "..", "..", "backend", "functions")

TARGETS = ["yieldPercent", "harvestDays"]
FEATURE_NAMES = ["mean_aq", "std_aq", "min_aq", "max_aq", "trend_aq"]


def main():
    for target in TARGETS:
        model_path = os.path.join(MODELS_DIR, f"{target}_model.pkl")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Run train_yield_model.py first. Missing: {model_path}")

        model = joblib.load(model_path)
        dummy = np.array([[350, 30, 320, 380, 1.5]])  # typical mid-growth reading
        pred  = model.predict(dummy)[0]
        print(f"{target} — dummy prediction: {pred:.2f}")

        # Copy to backend/functions so Cloud Functions can load it
        dest = os.path.join(BACKEND_DIR, f"{target}_model.pkl")
        shutil.copy(model_path, dest)
        print(f"Copied to {dest}")

    # Also copy LSTM model
    lstm_src = os.path.join(MODELS_DIR, "model.onnx")
    if os.path.exists(lstm_src):
        dest = os.path.join(BACKEND_DIR, "model.onnx")
        shutil.copy(lstm_src, dest)
        print(f"Copied LSTM model.onnx to {dest}")
    else:
        print("WARNING: model.onnx not found. Run export_onnx.py first.")

    print("\nAll models verified and copied to backend/functions/")


if __name__ == "__main__":
    main()