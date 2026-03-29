// hydromind/pwa/src/components/HealthScore.jsx
export default function HealthScore({ score = 0 }) {
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 80) return '#00ff88';
    if (score >= 50) return '#ffaa00';
    return '#ff3366';
  };

  const getStatus = () => {
    if (score >= 80) return 'Excellent';
    if (score >= 50) return 'Good';
    if (score >= 30) return 'Fair';
    return 'Critical';
  };

  return (
    <div className="relative flex flex-col items-center">
      {/* Circular progress */}
      <div className="relative w-48 h-48">
        <svg className="transform -rotate-90 w-full h-full">
          {/* Background circle */}
          <circle
            cx="96"
            cy="96"
            r={radius}
            stroke="#1b2e1b"
            strokeWidth="12"
            fill="none"
          />
          {/* Progress circle */}
          <circle
            cx="96"
            cy="96"
            r={radius}
            stroke={getColor()}
            strokeWidth="12"
            fill="none"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-out"
            style={{
              filter: `drop-shadow(0 0 8px ${getColor()})`
            }}
          />
        </svg>

        {/* Center content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-5xl font-bold font-mono" style={{ color: getColor() }}>
            {score}
          </div>
          <div className="text-sm text-text-secondary font-medium mt-1">
            Health Score
          </div>
        </div>
      </div>

      {/* Status label */}
      <div className="mt-4 px-6 py-2 rounded-full border-2" style={{
        borderColor: getColor(),
        backgroundColor: `${getColor()}15`
      }}>
        <span className="text-sm font-bold uppercase tracking-wider" style={{ color: getColor() }}>
          {getStatus()}
        </span>
      </div>
    </div>
  );
}
