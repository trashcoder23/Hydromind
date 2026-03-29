// hydromind/pwa/src/pages/Settings.jsx
export default function Settings() {
  return (
    <div className="px-4 sm:px-6 pt-6 pb-24 max-w-7xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl sm:text-4xl font-bold gradient-text mb-2">Settings</h2>
        <p className="text-text-secondary text-sm">System configuration and information</p>
      </div>

      {/* System Info */}
      <div className="bg-secondary border-2 border-accent-green/30 rounded-2xl p-6 mb-6">
        <h3 className="text-xl font-bold text-accent-green mb-4 flex items-center gap-2">
          <span>ℹ️</span> System Information
        </h3>
        <div className="space-y-3">
          <InfoRow label="Project" value="HydroMind v1.0" />
          <InfoRow label="Database" value="Firebase Realtime Database" />
          <InfoRow label="Region" value="Asia Southeast 1" />
          <InfoRow label="ML Models" value="LSTM + Gradient Boosting" />
          <InfoRow label="Update Interval" value="5 seconds" />
        </div>
      </div>

      {/* About */}
      <div className="bg-secondary border-2 border-accent-green/30 rounded-2xl p-6">
        <h3 className="text-xl font-bold text-accent-green mb-4 flex items-center gap-2">
          <span>🌱</span> About HydroMind
        </h3>
        <p className="text-text-secondary text-sm leading-relaxed mb-4">
          HydroMind is an AI-powered IoT hydroponic monitoring and control system with predictive analytics.
          It combines real-time sensor monitoring, LSTM-based crash prediction, and yield forecasting to
          optimize your hydroponic setup.
        </p>
        <div className="flex flex-wrap gap-2">
          <Badge text="React" />
          <Badge text="Firebase" />
          <Badge text="TensorFlow" />
          <Badge text="ONNX" />
          <Badge text="Python" />
          <Badge text="ESP8266" />
        </div>
      </div>

      {/* Footer */}
      <div className="mt-8 text-center">
        <p className="text-text-muted text-xs">
          Made with 💚 for smart agriculture
        </p>
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between items-center py-2 border-b border-accent-green/10">
      <span className="text-text-muted text-sm">{label}</span>
      <span className="text-text-primary font-semibold text-sm">{value}</span>
    </div>
  );
}

function Badge({ text }) {
  return (
    <span className="px-3 py-1 bg-accent-green/10 border border-accent-green/30 
                     rounded-full text-accent-green text-xs font-semibold uppercase tracking-wide">
      {text}
    </span>
  );
}
