// hydromind/pwa/src/components/Navbar.jsx
import { NavLink } from "react-router-dom";

const NAV_ITEMS = [
  { path: "/", icon: "📊", label: "Dashboard" },
  { path: "/predictions", icon: "🔮", label: "Predictions" },
  { path: "/controls", icon: "🎛️", label: "Controls" },
  { path: "/alerts", icon: "🔔", label: "Alerts" },
  { path: "/settings", icon: "⚙️", label: "Settings" },
];

export default function Navbar() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-secondary/95 backdrop-blur-lg border-t-2 border-accent-green/20 z-50">
      <div className="max-w-7xl mx-auto px-2 sm:px-4">
        <div className="flex justify-around items-center h-16 sm:h-18">
          {NAV_ITEMS.map(({ path, icon, label }) => (
            <NavLink
              key={path}
              to={path}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center gap-1 px-3 py-2 rounded-xl transition-all duration-300 min-w-[60px] sm:min-w-[80px] ${
                  isActive
                    ? "text-accent-green bg-accent-green/10 shadow-glow-green"
                    : "text-text-muted hover:text-accent-green hover:bg-accent-green/5"
                }`
              }
            >
              <span className="text-xl sm:text-2xl">{icon}</span>
              <span className="text-[10px] sm:text-xs font-semibold uppercase tracking-wide">
                {label}
              </span>
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  );
}
