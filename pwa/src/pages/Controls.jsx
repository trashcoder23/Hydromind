// hydromind/pwa/src/pages/Controls.jsx
import { useState } from "react";
import MotorToggle from "../components/MotorToggle";
import { sendMotorCommand } from "../firebase/realtimeDB";

const MOTORS = [
  { key: "DOSE", label: "Dosing Pump", icon: "💉" },
  { key: "CIRC", label: "Circulation Pump", icon: "🌀" },
  { key: "PH", label: "pH Pump", icon: "⚗️" },
  { key: "FAN", label: "Ventilation Fan", icon: "💨" },
];

export default function Controls() {
  const [allOffLoading, setAllOffLoading] = useState(false);

  async function handleAllOff() {
    setAllOffLoading(true);
    try {
      await sendMotorCommand("ALL_OFF");
    } catch (err) {
      alert("Failed to send ALL_OFF command.");
    } finally {
      setAllOffLoading(false);
    }
  }

  return (
    <div className="px-4 sm:px-6 pt-6 pb-24 max-w-7xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl sm:text-4xl font-bold gradient-text mb-2">Motor Controls</h2>
        <p className="text-text-secondary text-sm">
          Manual override — commands route through Firebase → ESP8266 → Arduino
        </p>
      </div>

      {/* Motor Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {MOTORS.map((m) => (
          <MotorToggle
            key={m.key}
            motorKey={m.key}
            label={m.label}
            icon={m.icon}
          />
        ))}
      </div>

      {/* Emergency Stop */}
      <button
        onClick={handleAllOff}
        disabled={allOffLoading}
        className="w-full bg-accent-red/10 border-2 border-accent-red text-accent-red
                   rounded-2xl py-5 font-bold text-lg uppercase tracking-wider
                   hover:bg-accent-red/20 hover:shadow-glow-red active:scale-98 
                   transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {allOffLoading ? "⏳ Stopping All Motors..." : "⛔ EMERGENCY STOP — ALL OFF"}
      </button>

      {/* Info */}
      <div className="mt-6 bg-secondary/50 border border-accent-green/20 rounded-xl p-4">
        <p className="text-text-muted text-xs text-center">
          💡 Cloud Functions also send autonomous commands when anomalies are detected
        </p>
      </div>
    </div>
  );
}
