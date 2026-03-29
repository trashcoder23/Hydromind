// hydromind/pwa/src/pages/Alerts.jsx
import { useAlerts } from "../firebase/realtimeDB";

function AlertCard({ alert }) {
  const { type, timestamp, data } = alert;
  const date = new Date(timestamp);

  const getIcon = () => {
    switch (type) {
      case "crash_predicted": return "⚠️";
      case "water_low": return "💧";
      case "motor_command": return "🔧";
      default: return "🔔";
    }
  };

  const getColor = () => {
    switch (type) {
      case "crash_predicted": return "border-accent-red bg-accent-red/10 text-accent-red";
      case "water_low": return "border-accent-yellow bg-accent-yellow/10 text-accent-yellow";
      case "motor_command": return "border-accent-green bg-accent-green/10 text-accent-green";
      default: return "border-text-muted bg-secondary text-text-primary";
    }
  };

  const getTitle = () => {
    switch (type) {
      case "crash_predicted": return "System Crash Predicted";
      case "water_low": return "Low Water Level";
      case "motor_command": return `Motor: ${data?.motor || "Unknown"}`;
      default: return "Alert";
    }
  };

  const getDetails = () => {
    switch (type) {
      case "crash_predicted":
        return `Probability: ${(data?.crashProbability * 100).toFixed(0)}% | Time: ${data?.hoursToFailure}h`;
      case "water_low":
        return `Water level: ${data?.waterLevel?.toFixed(1)}%`;
      case "motor_command":
        return `Command: ${data?.command} | State: ${data?.state}`;
      default:
        return JSON.stringify(data);
    }
  };

  return (
    <div className={`border-2 rounded-2xl p-5 ${getColor()} card-hover`}>
      <div className="flex items-start gap-4">
        <span className="text-3xl">{getIcon()}</span>
        <div className="flex-1">
          <div className="flex items-start justify-between gap-2 mb-2">
            <h3 className="font-bold text-lg">{getTitle()}</h3>
            <span className="text-xs text-text-muted whitespace-nowrap">
              {date.toLocaleTimeString()}
            </span>
          </div>
          <p className="text-sm opacity-90">{getDetails()}</p>
          <p className="text-xs text-text-muted mt-2">
            {date.toLocaleDateString()}
          </p>
        </div>
      </div>
    </div>
  );
}

export default function Alerts() {
  const { alerts, loading } = useAlerts();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-text-secondary">Loading alerts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 sm:px-6 pt-6 pb-24 max-w-7xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl sm:text-4xl font-bold gradient-text mb-2">Alert History</h2>
        <p className="text-text-secondary text-sm">
          {alerts.length} total alerts
        </p>
      </div>

      {/* Alerts List */}
      {alerts.length === 0 ? (
        <div className="bg-secondary border-2 border-accent-green/30 rounded-2xl p-12 text-center">
          <span className="text-6xl mb-4 block">🔕</span>
          <p className="text-text-secondary text-lg">No alerts yet</p>
          <p className="text-text-muted text-sm mt-2">
            Alerts will appear here when triggered by the system
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <AlertCard key={alert.id} alert={alert} />
          ))}
        </div>
      )}
    </div>
  );
}
