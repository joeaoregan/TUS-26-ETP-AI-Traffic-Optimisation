# LSTM Traffic Flow Predictor

## 📋 Project Overview

Predictive Modelling service for the Athlone "Orange Loop" traffic optimization system.

**Purpose:** Forecast vehicle flow 15 minutes into the future using Long Short-Term Memory (LSTM) neural networks.

**Target Performance:** Mean Absolute Error (MAE) < 10%

**Port:** 8001

**Why LSTM?**

- Learns temporal patterns (e.g., morning rush 8:15-9:00am)
- Handles non-linear traffic spikes (sudden congestion)
- Captures "memory" of traffic events across hours
- Superior to ARIMA for complex urban traffic

---

## 🚀 Quick Start

```bash
python -m venv venv
venv\Scripts\activate  # Windows

pip install -r requirements.txt

python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 📊 Data Flow

```
SUMO Simulation
    ↓
edgeData.xml (vehicle counts, speed, occupancy per junction)
    ↓
Data Loader (extract hourly vehicle flow)
    ↓
Preprocessor (scale, normalize, create sliding windows)
    ↓
LSTM Model (trained on historical patterns)
    ↓
Forecast (predicted vehicle flow 15 min ahead)
    ↓
RL Inference Service (uses forecast for signal timing)
    ↓
Traffic Signal Control
```

---

## 🔑 Key Concepts

### What is LSTM?

A type of neural network that:

- **Remembers** long-term patterns (e.g., "Mondays are always congested 8-9am with School / Work traffic")
- **Forgets** irrelevant old events (e.g., "An accident that happend 3 hours ago is now irrelevant")
- **Learns** non-linear relationships (e.g., "When School Reopens, rush hour is 8:15-9:00, but on holidays it's 9:30-10:30")

### LSTM vs ARIMA

| Aspect                 | ARIMA                  | LSTM                |
| ---------------------- | ---------------------- | ------------------- |
| **Pattern Type**       | Linear trends          | Non-linear spikes   |
| **Memory**             | Limited (p,d,q params) | Long-term via gates |
| **Sudden Changes**     | Poor                   | Good                |
| **Rush Hour Patterns** | Struggles              | Excellent           |
| **Data Amount Needed** | Small                  | Large (1000+)       |

## 📁 Service Endpoints

- `GET /health` — Service health check
- `POST /forecast` — Predict vehicle flow 15 min ahead  
- `GET /model_info` — Model details