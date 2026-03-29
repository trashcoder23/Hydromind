// hydromind/pwa/src/firebase/firebaseConfig.js
// ─────────────────────────────────────────────
// Firebase project credentials

import { initializeApp } from "firebase/app";
import { getDatabase }   from "firebase/database";
import { getMessaging }  from "firebase/messaging";

const firebaseConfig = {
  apiKey:            "AIzaSyCBeOIjXmbwOVT97c5__ThHeRm5nD1IOic",
  authDomain:        "hydromind-f4ee5.firebaseapp.com",
  databaseURL:       "https://hydromind-f4ee5-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId:         "hydromind-f4ee5",
  storageBucket:     "hydromind-f4ee5.firebasestorage.app",
  messagingSenderId: "989088195415",
  appId:             "1:989088195415:web:31919977b396ccadb8d412",
};

const app       = initializeApp(firebaseConfig);
export const database  = getDatabase(app);
export const messaging = getMessaging(app);
export default app;