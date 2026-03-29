// hydromind/pwa/src/firebase/realtimeDB.js
// All Firebase Realtime Database read/write helpers used by the PWA.

import { database } from "./firebaseConfig";
import {
  ref, onValue, set, push, serverTimestamp, get
} from "firebase/database";
import { useEffect, useState } from "react";

// ── Paths ───────────────────────────────────────────────────
const PATHS = {
  sensorData:    "hydromind/sensor_data",
  predictions:   "hydromind/predictions",
  commandPending:"hydromind/commands/pending",
  alerts:        "hydromind/alerts",
  history:       "hydromind/sensor_history",
};

// ── Hook: live sensor data ──────────────────────────────────
export function useSensorData() {
  const [data, setData]     = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onValue(ref(database, PATHS.sensorData), (snap) => {
      setData(snap.val());
      setLoading(false);
    });
    return () => unsub();
  }, []);

  return { data, loading };
}

// ── Hook: live predictions ──────────────────────────────────
export function usePredictions() {
  const [data, setData]     = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onValue(ref(database, PATHS.predictions), (snap) => {
      setData(snap.val());
      setLoading(false);
    });
    return () => unsub();
  }, []);

  return { data, loading };
}

// ── Hook: alert history (last 50) ──────────────────────────
export function useAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsub = onValue(ref(database, PATHS.alerts), (snap) => {
      const val = snap.val();
      if (!val) { setAlerts([]); setLoading(false); return; }
      const list = Object.entries(val)
        .map(([id, item]) => ({ id, ...item }))
        .sort((a, b) => b.timestamp - a.timestamp)
        .slice(0, 50);
      setAlerts(list);
      setLoading(false);
    });
    return () => unsub();
  }, []);

  return { alerts, loading };
}

// ── Send motor command ──────────────────────────────────────
export async function sendMotorCommand(command) {
  const validCommands = [
    "DOSE_ON","DOSE_OFF","CIRC_ON","CIRC_OFF",
    "PH_ON","PH_OFF","FAN_ON","FAN_OFF","ALL_OFF"
  ];
  if (!validCommands.includes(command)) {
    throw new Error(`Invalid command: ${command}`);
  }
  await set(ref(database, PATHS.commandPending), command);
  console.log(`Motor command sent: ${command}`);
}

// ── Write sensor data (used by test simulator) ──────────────
export async function writeSensorData(sensorObj) {
  const payload = {
    ...sensorObj,
    timestamp: Date.now(),
  };
  // Write to current reading
  await set(ref(database, PATHS.sensorData), payload);
  // Also push to history
  await push(ref(database, PATHS.history), payload);
}