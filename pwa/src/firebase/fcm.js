// hydromind/pwa/src/firebase/fcm.js
// Handles FCM push notification permission + token registration.

import { messaging } from "./firebaseConfig";
import { getToken, onMessage } from "firebase/messaging";

// Get this from Firebase Console → Project Settings → Cloud Messaging → Web Push certificates
const VAPID_KEY = "BC0YLUVu2wfQR-SLbE8JTT1ZwBPWPiqfTAWkrEKnEWO324v__c3BUzs7uxak3fBbWWiMXwVuVzmdWalT1q-2rJE";

/**
 * Request notification permission and get FCM token.
 * Subscribe the device to the "hydromind_alerts" topic via your backend,
 * or use the token directly for targeted messages.
 */
export async function initFCM() {
  try {
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      console.warn("Notification permission denied.");
      return null;
    }

    const token = await getToken(messaging, { vapidKey: VAPID_KEY });
    if (token) {
      console.log("FCM token:", token);
      // Save token to Firebase so Cloud Functions can target this device
      // In production: write to /hydromind/fcm_tokens/{token}
      return token;
    }
  } catch (err) {
    console.error("FCM init error:", err);
  }
  return null;
}

/**
 * Listen for foreground messages (when app is open).
 * When app is closed, the service worker handles it.
 */
export function onForegroundMessage(callback) {
  return onMessage(messaging, (payload) => {
    console.log("Foreground FCM message:", payload);
    callback(payload);
  });
}