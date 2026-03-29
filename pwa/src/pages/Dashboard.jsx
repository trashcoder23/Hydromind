// hydromind/pwa/src/pages/Dashboard.jsx
import { useState } from "react";
import { useSensorData } from "../firebase/realtimeDB";
import HealthScore from "../components/HealthScore";
import SensorCard from "../components/SensorCard";
import SensorChart from "../components/SensorChart";

function getSensorStatus(field, value) {
  if (value === null || value === undefined) return "unknown";
  switch (field) {
    case "temperature":
      return value >= 18 && value <= 30 ? "ok" : value >= 15 && value <= 35 ? "warn" : "critical";
    case "humidity":
      return value >= 40 && value <= 80 ? "ok" : value >= 25 && value <= 90 ? "warn" : "critical";
    case "airQuality":
      return value < 400 ? "ok" : value < 600 ? "warn" : "critical";
    case "waterLevel":
      return value > 50 ? "ok" : value > 20 ? "warn" : "critical";
    default:
      return "ok";
  }
}

const SENSORS = [
  { field: "temperature", label: "Temperature", unit: "°C", icon: "🌡️" },
  { field: "humidity", label: "Humidity", unit: "%", icon: "💧" },
  { field: "airQuality", label: "Air Quality", unit: "AQI", icon: "🌿" },
  { field: "waterLevel", label: "Water Level", unit: "%", icon: "💦" },
];

const CHART_FIELDS = ["temperature", "airQuality", "waterLevel"];

export default function Dashboard() {
  const { data, loading } = useSensorData();
  const [showCharts, setShowCharts] = useState(false);

  const ts = data?.timestamp
    ? new Date(data.timestamp).toLocaleTimeString()
    : null;

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-text-secondary">Connecting to HydroMind...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 sm:px-6 pt-6 pb-24 max-w-7xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-8 gap-4">
        <div>
          <h1 className="text-4xl sm:text-5xl font-bold gradient-text mb-2">
            HydroMind
          </h1>
          <p className="text-text-secondary text-sm flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${data ? "bg-accent-green animate-pulse-glow" : "bg-text-muted"}`} />
            {ts ? `Last update: ${ts}` : "Waiting for data..."}
          </p>
        </div>

        {/* Live indicator */}
        <div className={`px-4 py-2 rounded-full border-2 ${
          data ? "border-accent-green bg-accent-green/10" : "border-text-muted bg-secondary"
        }`}>
          <span className={`text-sm font-bold uppercase tracking-wider ${
            data ? "text-accent-green" : "text-text-muted"
          }`}>
            {data ? "● LIVE" : "○ OFFLINE"}
          </span>
        </div>
      </div>

      {/* Health Score */}
      <div className="flex justify-center mb-10">
        <HealthScore score={data?.healthScore || 0} />
      </div>

      {/* Vibration Alert */}
      {data?.vibration === 1 && (
        <div className="mb-6 bg-accent-red/10 border-2 border-accent-red rounded-2xl px-6 py-4 shadow-glow-red animate-pulse">
          <div className="flex items-center gap-3">
            <span className="text-3xl">⚠️</span>
            <div>
              <p className="text-accent-red font-bold text-lg">Vibration Detected</p>
              <p className="text-text-secondary text-sm">Pump may be experiencing issues</p>
            </div>
          </div>
        </div>
      )}

      {/* Sensor Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {SENSORS.map(({ field, label, unit, icon }) => (
          <SensorCard
            key={field}
            label={label}
            value={data?.[field]}
            unit={unit}
            icon={icon}
            status={getSensorStatus(field, data?.[field])}
          />
        ))}
      </div>

      {/* Toggle Charts Button */}
      <button
        onClick={() => setShowCharts(v => !v)}
        className="w-full py-3 px-4 bg-secondary border-2 border-accent-green/30 rounded-xl
                   text-accent-green font-semibold hover:bg-accent-green/10 hover:border-accent-green
                   transition-all duration-300 mb-4"
      >
        {showCharts ? "▲ Hide Trend Charts" : "▼ Show Trend Charts"}
      </button>

      {/* Trend Charts */}
      {showCharts && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 animate-slide-up">
          {CHART_FIELDS.map(f => (
            <SensorChart key={f} field={f} points={60} />
          ))}
        </div>
      )}
    </div>
  );
}
