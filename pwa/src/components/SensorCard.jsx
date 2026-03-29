// hydromind/pwa/src/components/SensorCard.jsx
export default function SensorCard({ label, value, unit, icon, status }) {
  const statusColors = {
    ok: 'border-accent-green text-accent-green',
    warn: 'border-accent-yellow text-accent-yellow',
    critical: 'border-accent-red text-accent-red',
    unknown: 'border-text-muted text-text-muted',
  };

  const statusGlow = {
    ok: 'shadow-glow-green',
    warn: 'shadow-glow-yellow',
    critical: 'shadow-glow-red',
    unknown: '',
  };

  const colorClass = statusColors[status] || statusColors.unknown;
  const glowClass = statusGlow[status] || '';

  return (
    <div className={`
      relative bg-secondary border-2 ${colorClass} ${glowClass}
      rounded-2xl p-4 card-hover transition-all duration-300
      flex flex-col justify-between h-full
    `}>
      {/* Status indicator dot */}
      <div className="absolute top-3 right-3">
        <div className={`w-2 h-2 rounded-full ${
          status === 'ok' ? 'bg-accent-green animate-pulse-glow' :
          status === 'warn' ? 'bg-accent-yellow' :
          status === 'critical' ? 'bg-accent-red animate-pulse' :
          'bg-text-muted'
        }`} />
      </div>

      {/* Icon and label */}
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">{icon}</span>
        <span className="text-xs font-medium text-text-secondary uppercase tracking-wider">
          {label}
        </span>
      </div>

      {/* Value */}
      <div className="flex items-baseline gap-1">
        <span className={`text-3xl font-bold font-mono ${
          status === 'ok' ? 'text-accent-green' :
          status === 'warn' ? 'text-accent-yellow' :
          status === 'critical' ? 'text-accent-red' :
          'text-text-muted'
        }`}>
          {value !== null && value !== undefined ? value.toFixed(1) : '--'}
        </span>
        <span className="text-sm text-text-muted font-medium">{unit}</span>
      </div>

      {/* Status text */}
      <div className="mt-2">
        <span className={`text-xs font-semibold uppercase ${
          status === 'ok' ? 'text-accent-green' :
          status === 'warn' ? 'text-accent-yellow' :
          status === 'critical' ? 'text-accent-red' :
          'text-text-muted'
        }`}>
          {status === 'ok' ? '● Optimal' :
           status === 'warn' ? '⚠ Warning' :
           status === 'critical' ? '✕ Critical' :
           '○ Unknown'}
        </span>
      </div>
    </div>
  );
}
