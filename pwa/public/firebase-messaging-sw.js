// hydromind/pwa/public/firebase-messaging-sw.js
// This file MUST be at the root of the hosted domain.
// It handles push notifications when the PWA is closed or in background.

importScripts("https://www.gstatic.com/firebasejs/10.11.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.11.0/firebase-messaging-compat.js");

// Must match firebaseConfig.js exactly
firebase.initializeApp({
  apiKey:            "AIzaSyCBeOIjXmbwOVT97c5__ThHeRm5nD1IOic",
  authDomain:        "hydromind-f4ee5.firebaseapp.com",
  databaseURL:       "https://hydromind-f4ee5-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId:         "hydromind-f4ee5",
  storageBucket:     "hydromind-f4ee5.firebasestorage.app",
  messagingSenderId: "989088195415",
  appId:             "1:989088195415:web:31919977b396ccadb8d412",
});

const messaging = firebase.messaging();

// Background message handler
messaging.onBackgroundMessage((payload) => {
  console.log("[SW] Background message:", payload);

  const { title, body } = payload.notification || {};
  const notificationTitle = title || "HydroMind Alert";
  const notificationOptions = {
    body:    body || "Check your hydroponic system.",
    icon:    "/icon-192.png",
    badge:   "/icon-192.png",
    tag:     "hydromind-alert",
    renotify: true,
    data:    payload.data || {},
    actions: [
      { action: "open", title: "Open App" },
      { action: "dismiss", title: "Dismiss" },
    ],
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});

// Notification click handler
self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  if (event.action === "dismiss") return;

  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then((clientList) => {
      for (const client of clientList) {
        if (client.url.includes(self.location.origin) && "focus" in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow("/");
      }
    })
  );
});