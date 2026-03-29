# HydroMind Setup Guide

## ✅ Current Status

You have all the necessary files! Here's what you need to do to get everything working:

## 📋 Prerequisites

- Python 3.11+ installed (`py --version` works ✓)
- Node.js 18+ and npm
- Firebase CLI (`npm install -g firebase-tools`)
- Firebase project created

## 🚀 Step-by-Step Setup

### 1. Install ML Dependencies

```bash
cd hydromind/ml
py -m pip install -r requirements.txt
```

### 2. Generate Training Data & Train Models

```bash
# Generate synthetic sensor data
py lstm_crash_predictor/generate_synthetic_data.py

# Train LSTM crash predictor
py lstm_crash_predictor/train_lstm.py

# Export LSTM to ONNX format
py lstm_crash_predictor/export_onnx.py

# Train yield prediction models
py yield_predictor/train_yield_model.py

# Export all models to backend
py yield_predictor/export_yield_model.py
```

### 3. Configure Firebase Credentials

```bash
cd ..
py fill_credentials.py
```

This will ask for:
- Firebase Project ID
- API Key
- Messaging Sender ID
- App ID
- VAPID Public Key

Get these from: Firebase Console → Project Settings → Your Apps → Web App

### 4. Copy Scaler to Backend

After training, copy the scaler file:

```bash
# Windows
copy ml\lstm_crash_predictor\scaler.pkl backend\functions\scaler.pkl
```

### 5. Deploy Backend to Firebase

```bash
cd backend
firebase login
firebase deploy --only functions,database
```

### 6. Install & Run Frontend

```bash
cd ../pwa
npm install
npm run dev
```

The PWA will open at `http://localhost:5173`

### 7. Test with Simulator (Optional)

In a separate terminal:

```bash
cd hydromind
py simulator.py                    # Normal mode
py simulator.py --anomaly aq       # Air quality spike
py simulator.py --anomaly water    # Water level drop
```

## 📁 Missing Files Created

I've created these missing files for you:
- `backend/.firebaserc` - Firebase project config
- `backend/database.rules.json` - Database security rules
- `pwa/src/components/SensorChart.jsx` - Chart component for dashboard

## ⚠️ Important Notes

1. **Firebase Rules**: The current database rules allow public read/write for development. Secure them before production!

2. **Service Account**: For the simulator and local testing, download a service account key from Firebase Console → Project Settings → Service Accounts

3. **Models Location**: After training, these files should exist:
   - `ml/models/model.onnx`
   - `backend/functions/model.onnx`
   - `backend/functions/scaler.pkl`
   - `backend/functions/yieldPercent_model.pkl`
   - `backend/functions/harvestDays_model.pkl`

## 🧪 Verification Checklist

- [ ] ML models trained successfully
- [ ] Models copied to backend/functions/
- [ ] Firebase credentials filled in
- [ ] Backend deployed to Firebase
- [ ] Frontend running locally
- [ ] Simulator pushing data to Firebase
- [ ] Dashboard showing live sensor data
- [ ] Predictions updating

## 🐛 Troubleshooting

**Import errors during training:**
```bash
py -m pip install --upgrade tensorflow scikit-learn pandas numpy
```

**Firebase deploy fails:**
- Check you're logged in: `firebase login`
- Verify project ID in `.firebaserc`

**Frontend not connecting:**
- Check Firebase config in `pwa/src/firebase/firebaseConfig.js`
- Verify database URL matches your Firebase region

## 📚 Next Steps

Once everything is running:
1. Test motor controls from the Controls page
2. Trigger anomalies with the simulator
3. Watch predictions update in real-time
4. Check alerts history
5. Connect actual Arduino/ESP8266 hardware
