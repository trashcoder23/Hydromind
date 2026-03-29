"""
hydromind/backend/functions/on_command_write.py

Triggered when a motor command is written to /hydromind/commands/pending.
Logs the command to /hydromind/alerts for the alert history screen.
"""

import time
import firebase_admin
from firebase_admin import db, messaging
import firebase_functions.db_fn as db_fn
from firebase_functions.options import SupportedRegion 

if not firebase_admin._apps:
    firebase_admin.initialize_app()

VALID_COMMANDS = {
    "DOSE_ON", "DOSE_OFF",
    "CIRC_ON", "CIRC_OFF",
    "PH_ON",   "PH_OFF",
    "FAN_ON",  "FAN_OFF",
    "ALL_OFF",
}

MOTOR_LABELS = {
    "DOSE": "Dosing pump",
    "CIRC": "Circulation pump",
    "PH":   "pH pump",
    "FAN":  "Ventilation fan",
    "ALL":  "All motors",
}


@db_fn.on_value_written(
    reference="/hydromind/commands/pending",
    region=SupportedRegion.ASIA_SOUTHEAST1
)
def on_command_write(event):
    """Logs motor command to alert history."""
    command = event.data.after.val()

    if not command or command not in VALID_COMMANDS:
        return

    print(f"Motor command received: {command}")

    # Parse motor name and state
    parts = command.split("_")
    motor_key = parts[0]
    state     = parts[1] if len(parts) > 1 else "OFF"
    label     = MOTOR_LABELS.get(motor_key, motor_key)

    # Log to alerts history
    alerts_ref = db.reference("/hydromind/alerts")
    alerts_ref.push({
        "type":      "motor_command",
        "timestamp": int(time.time() * 1000),
        "data": {
            "command": command,
            "motor":   label,
            "state":   state,
        }
    })

    # Optional: send push when an autonomous correction fires
    if state == "ON":
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=f"🔧 HydroMind — Motor activated",
                    body=f"{label} turned ON automatically",
                ),
                topic="hydromind_alerts",
                data={"type": "motor_command", "command": command},
            )
            messaging.send(message)
        except Exception as e:
            print(f"FCM send failed (non-critical): {e}")