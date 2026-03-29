// hydromind/pwa/src/components/MotorToggle.jsx
import { useState } from "react";
import { sendMotorCommand } from "../firebase/realtimeDB";

export default function MotorToggle({ motorKey, label, icon }) {
  const [isOn, setIsOn] = useState(false);
  const [loading, setLoading] = useState(false);

  async function toggle() {
    setLoading(true);
    const cmd = isOn ? `${motorKey}_OFF` : `${motorKey}_ON`;
    try {
      await sendMotorCommand(cmd);
      setIsOn(!isOn);
    } catch (err) {
      console.error(`Command failed: ${cmd}`, err);
      alert("Failed to send command. Check connection.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      onClick={toggle}
      disabled={loading}
      className={`flex flex-col items-center gap-3 rounded-2xl p-6 border-2 transition-all duration-300
                  active:scale-95 disabled:opacity-50 w-full card-hover
                  ${isOn
                    ? "bg-accent-green/10 border-accent-green shadow-glow-green"
                    : "bg-secondary border-accent-green/30 hover:border-accent-green/50"}`}
    >
      <span className="text-4xl">{icon}</span>
      <div className="text-center">
        <p className="text-sm font-bold text-text-primary uppercase tracking-wide">{label}</p>
        <p className={`text-xs font-semibold mt-1 uppercase tracking-wider ${
          isOn ? "text-accent-green" : "text-text-muted"
        }`}>
          {loading ? "⏳ Sending..." : isOn ? "● ON" : "○ OFF"}
        </p>
      </div>
      
      {/* Toggle switch */}
      <div className={`w-14 h-7 rounded-full transition-all duration-300 relative ${
        isOn ? "bg-accent-green shadow-glow-green" : "bg-text-muted/30"
      }`}>
        <span className={`absolute top-0.5 w-6 h-6 rounded-full bg-white shadow-lg
                          transition-transform duration-300 ${
          isOn ? "translate-x-7" : "translate-x-0.5"
        }`} />
      </div>
    </button>
  );
}
