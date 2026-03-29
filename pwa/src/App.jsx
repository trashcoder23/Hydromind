// hydromind/pwa/src/App.jsx
import { useEffect, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import Predictions from "./pages/Predictions";
import Controls from "./pages/Controls";
import Alerts from "./pages/Alerts";
import Settings from "./pages/Settings";
import { initFCM, onForegroundMessage } from "./firebase/fcm";

export default function App() {
  const [toast, setToast] = useState(null);

  useEffect(() => {
    // Init FCM once on mount
    initFCM().then((token) => {
      if (token) console.log("FCM ready");
    });

    // Foreground notification toast
    const unsub = onForegroundMessage((payload) => {
      const title = payload.notification?.title || "HydroMind Alert";
      const body = payload.notification?.body || "";
      setToast({ title, body });
      setTimeout(() => setToast(null), 5000);
    });

    return () => typeof unsub === "function" && unsub();
  }, []);

  return (
    <BrowserRouter>
      {/* Foreground notification toast */}
      {toast && (
        <div className="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-11/12 max-w-md
                        bg-accent-yellow border-2 border-accent-yellow-dark rounded-2xl 
                        px-6 py-4 shadow-glow-yellow animate-bounce-once">
          <div className="flex items-start gap-3">
            <span className="text-2xl">🔔</span>
            <div className="flex-1">
              <p className="font-bold text-primary text-sm">{toast.title}</p>
              <p className="text-primary text-xs mt-1">{toast.body}</p>
            </div>
          </div>
        </div>
      )}

      <div className="flex flex-col min-h-screen">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/predictions" element={<Predictions />} />
          <Route path="/controls" element={<Controls />} />
          <Route path="/alerts" element={<Alerts />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>

      <Navbar />
    </BrowserRouter>
  );
}
