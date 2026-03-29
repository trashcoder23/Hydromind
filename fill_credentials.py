"""
hydromind/fill_credentials.py

Run this ONCE after cloning the repo.
It asks for your Firebase credentials interactively
and patches every file that needs them.

Usage:
    cd hydromind
    python fill_credentials.py
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

FILES_TO_PATCH = [
    os.path.join(ROOT, "pwa", "src", "firebase", "firebaseConfig.js"),
    os.path.join(ROOT, "pwa", "public", "firebase-messaging-sw.js"),
    os.path.join(ROOT, "backend", ".firebaserc"),
    os.path.join(ROOT, "simulator.py"),
]

REPLACEMENTS = {
    "YOUR_API_KEY":            None,
    "YOUR_PROJECT_ID":         None,
    "YOUR_SENDER_ID":          None,
    "YOUR_APP_ID":             None,
    "YOUR_VAPID_PUBLIC_KEY":   None,
}


def ask(prompt, key):
    val = input(f"  {prompt}: ").strip()
    if not val:
        print(f"  Skipped (keeping placeholder for {key})")
        return None
    return val


def main():
    print("\n🌱 HydroMind — Credential Setup")
    print("=" * 50)
    print("Get these values from:")
    print("  Firebase Console → Project Settings → Your Apps → Web App")
    print("  Cloud Messaging tab → Web Push certificates (for VAPID key)")
    print("=" * 50 + "\n")

    REPLACEMENTS["YOUR_PROJECT_ID"]       = ask("Firebase Project ID (e.g. hydromind-abc12)", "YOUR_PROJECT_ID")
    REPLACEMENTS["YOUR_API_KEY"]          = ask("Firebase API Key", "YOUR_API_KEY")
    REPLACEMENTS["YOUR_SENDER_ID"]        = ask("Messaging Sender ID", "YOUR_SENDER_ID")
    REPLACEMENTS["YOUR_APP_ID"]           = ask("App ID (starts with 1:)", "YOUR_APP_ID")
    REPLACEMENTS["YOUR_VAPID_PUBLIC_KEY"] = ask("VAPID Public Key (from Cloud Messaging tab)", "YOUR_VAPID_PUBLIC_KEY")

    print("\nPatching files…")
    for filepath in FILES_TO_PATCH:
        if not os.path.exists(filepath):
            print(f"  ⚠ Skipping (not found): {filepath}")
            continue

        with open(filepath, "r") as f:
            content = f.read()

        original = content
        for placeholder, value in REPLACEMENTS.items():
            if value:
                content = content.replace(placeholder, value)

        if content != original:
            with open(filepath, "w") as f:
                f.write(content)
            print(f"  ✓ Patched: {os.path.relpath(filepath, ROOT)}")
        else:
            print(f"  – No changes: {os.path.relpath(filepath, ROOT)}")

    # Also patch databaseURL which is derived from project ID
    project_id = REPLACEMENTS["YOUR_PROJECT_ID"]
    if project_id:
        db_url = f"https://{project_id}-default-rtdb.asia-southeast1.firebasedatabase.app"
        db_placeholder = "https://YOUR_PROJECT_ID-default-rtdb.asia-southeast1.firebasedatabase.app"

        for filepath in FILES_TO_PATCH:
            if not os.path.exists(filepath):
                continue
            with open(filepath, "r") as f:
                content = f.read()
            if db_placeholder in content:
                content = content.replace(db_placeholder, db_url)
                with open(filepath, "w") as f:
                    f.write(content)
                print(f"  ✓ Database URL patched: {os.path.relpath(filepath, ROOT)}")

        # Patch simulator DATABASE_URL separately
        sim_path = os.path.join(ROOT, "simulator.py")
        if os.path.exists(sim_path):
            with open(sim_path, "r") as f:
                content = f.read()
            content = content.replace(
                'DATABASE_URL = "https://YOUR_PROJECT_ID-default-rtdb.asia-southeast1.firebasedatabase.app"',
                f'DATABASE_URL = "{db_url}"'
            )
            with open(sim_path, "w") as f:
                f.write(content)

    print("\n✅ Done! Credentials filled in.")
    print("\nNext steps:")
    print("  1. cd ml && pip install -r requirements.txt")
    print("  2. python lstm_crash_predictor/generate_synthetic_data.py")
    print("  3. python lstm_crash_predictor/train_lstm.py")
    print("  4. python lstm_crash_predictor/export_onnx.py")
    print("  5. python yield_predictor/train_yield_model.py")
    print("  6. python yield_predictor/export_yield_model.py")
    print("  7. cd ../backend && firebase deploy --only functions,database")
    print("  8. cd ../pwa && npm install && npm run dev\n")


if __name__ == "__main__":
    main()