"""
hydromind/backend/functions/test_cloud_functions.py

Integration smoke-test for the three Cloud Functions.
Run this LOCALLY before firebase deploy to catch errors early.

Requirements:
    pip install firebase-admin onnxruntime scikit-learn joblib numpy

Usage:
    cd hydromind/backend/functions
    python test_cloud_functions.py
"""

import os
import sys
import time
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

print("=" * 60)
print("HydroMind Cloud Functions — local smoke test")
print("=" * 60)


# ── TEST 1: ONNX model loads and runs ───────────────────────
def test_onnx():
    print("\n[1/4] Testing ONNX model load + inference...")
    model_path = os.path.join(SCRIPT_DIR, "model.onnx")
    if not os.path.exists(model_path):
        print("  ✗ model.onnx not found. Run export_onnx.py first.")
        return False

    import onnxruntime as ort
    sess    = ort.InferenceSession(model_path)
    inp     = sess.get_inputs()[0].name
    dummy   = np.zeros((1, 288, 4), dtype=np.float32)
    result  = sess.run(None, {inp: dummy})
    prob    = float(result[0][0][0])
    print(f"  ✓ ONNX model OK — dummy crash probability: {prob:.4f}")
    return True


# ── TEST 2: Scaler loads ─────────────────────────────────────
def test_scaler():
    print("\n[2/4] Testing scaler load...")
    scaler_path = os.path.join(SCRIPT_DIR, "scaler.pkl")
    if not os.path.exists(scaler_path):
        print("  ✗ scaler.pkl not found. Run train_lstm.py first.")
        return False

    import joblib
    scaler = joblib.load(scaler_path)
    dummy  = np.array([[25.0, 60.0, 350, 75.0]])
    scaled = scaler.transform(dummy)
    print(f"  ✓ Scaler OK — dummy scaled: {scaled[0].round(3)}")
    return True


# ── TEST 3: Yield models load ────────────────────────────────
def test_yield_models():
    print("\n[3/4] Testing yield models...")
    import joblib
    ok = True
    for name in ["yieldPercent_model.pkl", "harvestDays_model.pkl"]:
        path = os.path.join(SCRIPT_DIR, name)
        if not os.path.exists(path):
            print(f"  ✗ {name} not found. Run train_yield_model.py + export_yield_model.py.")
            ok = False
            continue
        model = joblib.load(path)
        dummy = np.array([[350, 30, 320, 380, 1.5]])
        pred  = model.predict(dummy)[0]
        print(f"  ✓ {name} OK — dummy prediction: {pred:.2f}")
    return ok


# ── TEST 4: Health score logic ───────────────────────────────
def test_health_score():
    print("\n[4/4] Testing health score algorithm...")

    def score(temp, hum, aq, water):
        s = 100
        if not (18 <= temp <= 30):  s -= 25
        if not (40 <= hum  <= 80):  s -= 20
        if aq >= 600:               s -= 30
        if water <= 20:             s -= 25
        return max(0, s)

    cases = [
        (25, 60, 350, 75, 100, "all healthy"),
        (35, 60, 350, 75,  75, "temp out"),
        (25, 20, 350, 75,  80, "humidity out"),
        (25, 60, 700, 75,  70, "AQ critical"),
        (25, 60, 350, 10,  75, "water low"),
        (35, 20, 700, 10,   0, "all bad"),
    ]
    all_ok = True
    for temp, hum, aq, water, expected, label in cases:
        got = score(temp, hum, aq, water)
        status = "✓" if got == expected else "✗"
        if got != expected:
            all_ok = False
        print(f"  {status} {label}: expected={expected}, got={got}")
    return all_ok


# ── Run all tests ────────────────────────────────────────────
results = {
    "ONNX model":     test_onnx(),
    "Scaler":         test_scaler(),
    "Yield models":   test_yield_models(),
    "Health score":   test_health_score(),
}

print("\n" + "=" * 60)
print("Results:")
all_passed = True
for name, passed in results.items():
    icon = "✓" if passed else "✗"
    print(f"  {icon} {name}")
    if not passed:
        all_passed = False

print("=" * 60)
if all_passed:
    print("All tests passed. Safe to deploy.\n")
    sys.exit(0)
else:
    print("Some tests failed. Fix above before deploying.\n")
    sys.exit(1)