"""
hydromind/train_all_models.py

One-click script to train all ML models and export them to backend.
Run this after installing ML dependencies.

Usage:
    cd hydromind
    py train_all_models.py
"""

import os
import sys
import subprocess

STEPS = [
    ("Generating synthetic sensor data...", "ml/lstm_crash_predictor/generate_synthetic_data.py"),
    ("Training LSTM crash predictor...", "ml/lstm_crash_predictor/train_lstm.py"),
    ("Exporting LSTM to ONNX...", "ml/lstm_crash_predictor/export_onnx.py"),
    ("Training yield prediction models...", "ml/yield_predictor/train_yield_model.py"),
    ("Exporting models to backend...", "ml/yield_predictor/export_yield_model.py"),
]

def run_step(description, script_path):
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(__file__))
    
    if result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        return False
    
    print(f"\n✅ Completed: {description}")
    return True

def copy_scaler():
    """Copy scaler.pkl to backend/functions/"""
    import shutil
    src = "ml/lstm_crash_predictor/scaler.pkl"
    dst = "backend/functions/scaler.pkl"
    
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"\n✅ Copied scaler.pkl to backend/functions/")
        return True
    else:
        print(f"\n⚠️  Warning: {src} not found")
        return False

def main():
    print("\n🌱 HydroMind — Training All Models")
    print("="*60)
    
    # Check if we're in the right directory
    if not os.path.exists("ml") or not os.path.exists("backend"):
        print("❌ Error: Run this script from the hydromind/ root directory")
        sys.exit(1)
    
    # Run all training steps
    for description, script_path in STEPS:
        if not run_step(description, script_path):
            print("\n❌ Training pipeline failed. Fix errors and try again.")
            sys.exit(1)
    
    # Copy scaler
    copy_scaler()
    
    print("\n" + "="*60)
    print("✅ All models trained and exported successfully!")
    print("="*60)
    print("\nNext steps:")
    print("  1. py fill_credentials.py  (if not done yet)")
    print("  2. cd backend && firebase deploy --only functions,database")
    print("  3. cd ../pwa && npm install && npm run dev")
    print("  4. py simulator.py  (to test with fake sensor data)\n")

if __name__ == "__main__":
    main()
