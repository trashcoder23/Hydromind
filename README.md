# 🌱 HydroMind

AI-powered IoT hydroponic monitoring and control system with predictive analytics.

![HydroMind](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![React](https://img.shields.io/badge/React-18.3-61dafb)
![Firebase](https://img.shields.io/badge/Firebase-Realtime-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Overview

HydroMind combines IoT sensors, real-time monitoring, and AI-powered predictions to optimize hydroponic farming. The system uses LSTM neural networks for crash prediction and gradient boosting for yield forecasting.

### Key Features

- 📊 **Real-time Monitoring** - Temperature, humidity, air quality, water level tracking
- 🤖 **LSTM Crash Prediction** - Predicts system failures before they happen
- 🌱 **Yield Forecasting** - Estimates crop growth and harvest timing
- 🎛️ **Remote Control** - Control pumps and fans from anywhere
- 📱 **Progressive Web App** - Works on mobile and desktop
- 🔔 **Push Notifications** - Instant alerts for critical events
- 🔥 **Firebase Backend** - Serverless, scalable infrastructure

## 🏗️ Architecture

```
┌─────────────────┐
│  ESP8266/Arduino │  ← Sensors (DHT22, MQ-135, HC-SR04, SW-420)
└────────┬────────┘
         │ WiFi
         ▼
┌─────────────────┐
│ Firebase RTDB   │  ← Real-time database
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ Cloud   │ │ React PWA    │
│Functions│ │ (Dashboard)  │
└─────────┘ └──────────────┘
    │
    ▼
┌─────────────────┐
│ LSTM + Yield    │  ← AI Models (ONNX)
│ Prediction      │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Firebase account
- Git

### 1. Clone Repository

```bash
git clone https://github.com/trashcoder23/Hydromind.git
cd Hydromind
```

### 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install ML dependencies
cd ml
pip install -r requirements.txt
```

### 3. Train ML Models

```bash
cd ..
python train_all_models.py
```

This will:
- Generate 130,000+ synthetic sensor readings
- Train LSTM crash predictor
- Train yield prediction models
- Export to ONNX format

### 4. Configure Firebase

```bash
python fill_credentials.py
```

Enter your Firebase credentials when prompted. Get them from:
- Firebase Console → Project Settings → Your Apps → Web App

### 5. Deploy Backend

```bash
cd backend
npm install -g firebase-tools
firebase login
firebase deploy --only functions,database
```

### 6. Run Frontend

```bash
cd ../pwa
npm install
npm run dev
```

Open `http://localhost:5173`

### 7. Test with Simulator

```bash
cd ..
python simulator.py
```

## 📦 Project Structure

```
hydromind/
├── backend/
│   ├── functions/          # Firebase Cloud Functions
│   │   ├── main.py
│   │   ├── on_sensor_write.py
│   │   ├── on_command_write.py
│   │   └── daily_yield_update.py
│   ├── firebase.json
│   └── database.rules.json
│
├── ml/
│   ├── lstm_crash_predictor/
│   │   ├── generate_synthetic_data.py
│   │   ├── train_lstm.py
│   │   └── export_onnx.py
│   ├── yield_predictor/
│   │   ├── train_yield_model.py
│   │   └── export_yield_model.py
│   └── models/             # Trained models
│
├── pwa/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── firebase/
│   └── package.json
│
├── simulator.py            # Hardware simulator
├── fill_credentials.py     # Credential setup
└── train_all_models.py     # One-click training
```

## 🧠 ML Models

### LSTM Crash Predictor
- **Input**: 288 timesteps (24 hours at 5-second intervals)
- **Features**: Temperature, Humidity, Air Quality, Water Level
- **Output**: Crash probability (0-1)
- **Architecture**: 2-layer LSTM (64 units) + Dense layers

### Yield Predictor
- **Input**: 6-hour window statistics
- **Features**: MQ-135 air quality (CO₂ proxy)
- **Output**: Yield % (0-100) and Harvest days (0-60)
- **Algorithm**: Gradient Boosting Regressor

## 🛠️ Hardware Requirements

- ESP8266 (NodeMCU or Wemos D1 Mini)
- Arduino Uno/Nano
- DHT22 (temperature & humidity)
- MQ-135 (air quality)
- HC-SR04 (ultrasonic water level)
- SW-420 (vibration sensor)
- 4-channel relay module

## 📱 Screenshots

### Dashboard
Real-time sensor monitoring with health score visualization

### Predictions
LSTM crash probability and yield forecasting

### Controls
Remote motor control with emergency stop

### Alerts
Push notification history and system events

## 🔒 Security Notes

⚠️ **IMPORTANT**: Never commit sensitive data to GitHub!

The `.gitignore` file excludes:
- Firebase credentials
- Service account keys
- API keys
- Trained models (large files)
- Virtual environments

Before deploying to production:
1. Enable Firebase Authentication
2. Update database security rules
3. Secure Cloud Functions with auth checks
4. Use environment variables for secrets

## 🤝 Contributing

This is an educational/demo project. Feel free to fork and adapt for your own hydroponic systems!

## 📄 License

MIT License - use freely for personal and commercial projects.

## 🙏 Acknowledgments

- TensorFlow & Keras for ML framework
- Firebase for real-time infrastructure
- React & Vite for frontend tooling
- Recharts for data visualization

## 📞 Contact

- GitHub: [@trashcoder23](https://github.com/trashcoder23)
- Repository: [Hydromind](https://github.com/trashcoder23/Hydromind)

---

Made with 💚 for smart agriculture
