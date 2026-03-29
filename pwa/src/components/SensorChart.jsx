// hydromind/pwa/src/components/SensorChart.jsx
import { useEffect, useState } from "react";
import { ref, query, orderByKey, limitToLast, onValue } from "firebase/database";
import { database } from "../firebase/firebaseConfig";
import { LineChart, Line, ResponsiveContainer, YAxis } from "recharts";

const FIELD_CONFIG = {
  temperature: { color: "#f59e0b", label: "Temperature", unit: "°C" },
  airQuality:  { color: "#10b981", label: "Air Quality", unit: "AQI" },
  waterLevel:  { color: "#3b82f6", label: "Water Level", unit: "%" },
};

export default function SensorChart({ field, points = 60 }) {
  const [data, setData] = useState([]);
  const config = FIELD_CONFIG[field];

  useEffect(() => {
    const historyRef = ref(database, "/hydromind/sensor_history");
    const historyQuery = query(historyRef, orderByKey(), limitToLast(points));

    const unsub = onValue(historyQuery, (snapshot) => {
      if (!snapshot.exists()) return;
      const vals = Object.values(snapshot.val()).map(row => ({
        value: row[field] || 0
      }));
      setData(vals);
    });

    return () => unsub();
  }, [field, points]);

  if (!config || data.length === 0) return null;

  const latest = data[data.length - 1]?.value || 0;
  const min = Math.min(...data.map(d => d.value));
  const max = Math.max(...data.map(d => d.value));

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-gray-500 uppercase tracking-wide">{config.label}</span>
        <span className="text-sm font-semibold text-white">
          {latest.toFixed(1)} {config.unit}
        </span>
      </div>
      <ResponsiveContainer width="100%" height={60}>
        <LineChart data={data}>
          <YAxis domain={[min * 0.95, max * 1.05]} hide />
          <Line
            type="monotone"
            dataKey="value"
            stroke={config.color}
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
      <div className="flex justify-between text-xs text-gray-600 mt-1">
        <span>Min: {min.toFixed(1)}</span>
        <span>Max: {max.toFixed(1)}</span>
      </div>
    </div>
  );
}
