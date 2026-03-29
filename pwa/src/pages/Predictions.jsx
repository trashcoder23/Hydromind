// hydromind/pwa/src/pages/Predictions.jsx
import { usePredictions } from "../firebase/realtimeDB";

function GaugeBar({ value, max = 1, colorClass }) {
  const pct = Math.round((value / max) * 100);
  return (
    <div className="w-full bg-secondary border border-accent-green/20 rounded-full h-4 overflow-hidden">
      <div
        className={`h-4 rounded-full transition-all duration-700 ${colorClass}`}
        style={{ width: `${Math.min(pct, 100)}%` }}
      />
    </div>
  );
}

function StatCard({ label, value, sub, highlight, icon }) {
  return (
    <div className="bg-secondary border-2 border-accent-green/30 rounded-2xl p-5 flex flex-col gap-2 card-hover">
      <div className="flex items-center justify-between">
        <p className="text-text-secondary text-xs uppercase tracking-wide font-semibold">{label}</p>
        {icon && <span className="text-2xl">{icon}</span>}
      </div>
      <p className={`text-4xl sm:text-5xl font-bold font-mono ${highlight}`}>{value}</p>
      {sub && <p className="text-text-muted text-xs">{sub}</p>}
    </div>
  );
}

export default function Predictions() {
  const { data, loading } = usePredictions();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-text-secondary">Loading predictions...</p>
        </div>
      </div>
    );
  }

  const crashProb = data?.crashProbability ?? 0;
  const hoursToFail = data?.hoursToFailure ?? 48;
  const yieldPct = data?.yieldPercent ?? 0;
  const harvestDays = data?.harvestDays ?? "—";
  const updatedAt = data?.updatedAt
    ? new Date(data.updatedAt).toLocaleString()
    : "Not yet updated";

  const crashColor =
    crashProb >= 0.7 ? "bg-accent-red shadow-glow-red" :
    crashProb >= 0.4 ? "bg-accent-yellow shadow-glow-yellow" :
                       "bg-accent-green shadow-glow-green";

  const crashTextColor =
    crashProb >= 0.7 ? "text-accent-red" :
    crashProb >= 0.4 ? "text-accent-yellow" :
                       "text-accent-green";

  return (
    <div className="px-4 sm:px-6 pt-6 pb-24 max-w-7xl mx-auto animate-slide-up">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl sm:text-4xl font-bold gradient-text mb-2">AI Predictions</h2>
        <p className="text-text-secondary text-sm">Last updated: {updatedAt}</p>
      </div>

      {/* Crash Prediction Section */}
      <section className="mb-8">
        <h3 className="text-lg font-bold text-accent-green uppercase tracking-wide mb-4 flex items-center gap-2">
          <span>🤖</span> LSTM Crash Prediction
        </h3>
        <div className="bg-secondary border-2 border-accent-green/30 rounded-2xl p-6 shadow-glow-green">
          <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-4 mb-4">
            <div>
              <p className="text-text-secondary text-sm mb-2">Crash Probability</p>
              <p className={`text-5xl sm:text-6xl font-bold font-mono ${crashTextColor}`}>
                {Math.round(crashProb * 100)}%
              </p>
            </div>
            {crashProb >= 0.7 && (
              <div className="px-4 py-2 bg-accent-red/20 border-2 border-accent-red rounded-full">
                <span className="text-accent-red font-bold text-sm uppercase tracking-wider">
                  ⚠️ High Risk
                </span>
              </div>
            )}
          </div>
          
          <GaugeBar value={crashProb} max={1} colorClass={crashColor} />
          
          <div className="mt-4 p-4 bg-primary/50 rounded-xl">
            <p className="text-text-secondary text-sm">
              Estimated time to threshold breach:{" "}
              <span className="text-accent-green font-bold text-lg">{hoursToFail}h</span>
            </p>
          </div>
        </div>
      </section>

      {/* Yield Prediction Section */}
      <section className="mb-8">
        <h3 className="text-lg font-bold text-accent-green uppercase tracking-wide mb-4 flex items-center gap-2">
          <span>🌱</span> Yield Forecast
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <StatCard
            label="Growth Progress"
            value={`${Math.round(yieldPct)}%`}
            sub="Based on CO₂ uptake rate"
            highlight="text-accent-green"
            icon="📈"
          />
          <StatCard
            label="Days to Harvest"
            value={harvestDays}
            sub="Estimated remaining"
            highlight="text-accent-green"
            icon="📅"
          />
        </div>
        <div className="bg-secondary border-2 border-accent-green/30 rounded-2xl p-6">
          <GaugeBar value={yieldPct} max={100} colorClass="bg-accent-green shadow-glow-green" />
        </div>
      </section>

      {/* Info Note */}
      <div className="bg-secondary/50 border border-accent-green/20 rounded-xl p-4">
        <p className="text-text-muted text-xs text-center">
          💡 LSTM model runs on every sensor write. Yield model updates every 6 hours.
        </p>
      </div>
    </div>
  );
}
