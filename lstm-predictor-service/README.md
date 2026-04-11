# LSTM Traffic Flow Predictor

![TUS](https://img.shields.io/badge/TUS-2026-black?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iMTU3LjU1OTM2bW0iCiAgIGhlaWdodD0iMjA1LjE3MTE2bW0iCiAgIHZpZXdCb3g9IjAgMCAxNTcuNTU5MzYgMjA1LjE3MTE2IgogICB2ZXJzaW9uPSIxLjEiCiAgIGlkPSJzdmcxIgogICB4bWw6c3BhY2U9InByZXNlcnZlIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxzb2RpcG9kaTpuYW1lZHZpZXcKICAgICBpZD0ibmFtZWR2aWV3MSIKICAgICBwYWdlY29sb3I9IiNmZmZmZmYiCiAgICAgYm9yZGVyY29sb3I9IiMwMDAwMDAiCiAgICAgYm9yZGVyb3BhY2l0eT0iMC4yNSIKICAgICBpbmtzY2FwZTpzaG93cGFnZXNoYWRvdz0iMiIKICAgICBpbmtzY2FwZTpwYWdlb3BhY2l0eT0iMC4wIgogICAgIGlua3NjYXBlOnBhZ2VjaGVja2VyYm9hcmQ9IjAiCiAgICAgaW5rc2NhcGU6ZGVza2NvbG9yPSIjZDFkMWQxIgogICAgIGlua3NjYXBlOmRvY3VtZW50LXVuaXRzPSJtbSI+PGlua3NjYXBlOnBhZ2UKICAgICAgIHg9IjAiCiAgICAgICB5PSIwIgogICAgICAgd2lkdGg9IjE1Ny41NTkzNiIKICAgICAgIGhlaWdodD0iMjA1LjE3MTE2IgogICAgICAgaWQ9InBhZ2UyIgogICAgICAgbWFyZ2luPSIwIgogICAgICAgYmxlZWQ9IjAiIC8+PC9zb2RpcG9kaTpuYW1lZHZpZXc+PGRlZnMKICAgICBpZD0iZGVmczEiPjxzdHlsZQogICAgICAgaWQ9InN0eWxlMSI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48c3R5bGUKICAgICAgIGlkPSJzdHlsZTEtNCI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48L2RlZnM+PGcKICAgICBpbmtzY2FwZTpsYWJlbD0iTGF5ZXIgMSIKICAgICBpbmtzY2FwZTpncm91cG1vZGU9ImxheWVyIgogICAgIGlkPSJsYXllcjEiCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjA4LjE2MDkzLDQ4Ljg3NTE2MikiPjxnCiAgICAgICBpZD0iQXJ0d29yayIKICAgICAgIHRyYW5zZm9ybT0ibWF0cml4KDAuMjY0NTgzMzMsMCwwLDAuMjY0NTgzMzMsLTIwOC4xNjA5NCwtNDguODc1MTU4KSI+PHBhdGgKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICBkPSJNIDU5NS40OCwwIEggNDc2LjM4IFYgNTguNTIgSCAzNTcuMyBWIDAgSCAyMzguMiBWIDU4LjUyIEggMTE5LjEgViAwIEggMCB2IDM1Ny4yOSBoIDExOS4xIGEgMTc4LjY0LDE3OC42NCAwIDEgMSAzNTcuMjgsMCBoIDExOS4wNiB6IgogICAgICAgICBpZD0icGF0aDEiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSI0NzYuMzgiCiAgICAgICAgIHk9IjcxNS45MDAwMiIKICAgICAgICAgd2lkdGg9IjExOS4xIgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3QxIiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNzE1LjkwMDAyIgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDIiCiAgICAgICAgIHg9IjAiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB5PSI1OTYuNzk5OTkiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSI1OS41NDk5OTkiCiAgICAgICAgIGlkPSJyZWN0MyIKICAgICAgICAgeD0iMCIgLz48cmVjdAogICAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICAgIHg9IjQ3Ni4zOTk5OSIKICAgICAgICAgeT0iNTk2Ljc5OTk5IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDQiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSIxMTkuMSIKICAgICAgICAgeT0iNTM3LjI1IgogICAgICAgICB3aWR0aD0iMzU3LjI5OTk5IgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3Q1IiAvPjxwb2x5Z29uCiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgcG9pbnRzPSI0NzYuMzksNjU2LjM1IDExOS4xLDY1Ni4zNSAxMTkuMSw3MTUuOSAyMzguMiw3MTUuOSAyMzguMiw3NzUuNDUgMzU3LjI5LDc3NS40NSAzNTcuMjksNzE1LjkgNDc2LjM5LDcxNS45ICIKICAgICAgICAgaWQ9InBvbHlnb241IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeD0iNDc2LjM5OTk5IgogICAgICAgICB5PSI0MTguMTYiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSIxMTkuMSIKICAgICAgICAgaWQ9InJlY3Q2IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNDE4LjE2IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iMTE5LjEiCiAgICAgICAgIGlkPSJyZWN0NyIKICAgICAgICAgeD0iMCIgLz48L2c+PC9nPjwvc3ZnPgo=)
![Module](https://img.shields.io/badge/Module-Engineering%20Team%20Project-blue?style=flat-square)
![Topic](https://img.shields.io/badge/Topic-AI%20Traffic%20Optimisation-blue?style=flat-square)

## 📋 Project Overview

Predictive modelling service for the Athlone "Orange Loop" traffic optimization system.

**Purpose**: Forecast edge traffic density for the next hour using Long Short-Term Memory (LSTM) neural networks.

**Current Performance**: MAE 0.2084, MSE 0.0698 (on normalized density values)

**Port**: 8001

**Why LSTM?**

- Learns temporal patterns (e.g., morning rush 8:15-9:00am)
- Handles non-linear traffic spikes (sudden congestion)
- Captures "memory" of traffic events across hours
- Superior to ARIMA for complex urban traffic

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- TensorFlow 2.11+
- SUMO traffic simulator (for data generation/analysis)

### Installation

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the service**:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

4. **Access**:
- API Docs: http://localhost:8001/docs
- Health Check: http://localhost:8001/health
- Model Info: http://localhost:8001/model-info

---

## 📊 Data Flow

```
SUMO Simulation
    ↓
edgeData.xml (edge metrics: density, occupancy, speed)
    ↓
lstm_train.py (load, preprocess, train)
    ↓
Normalize data (MinMaxScaler)
    ↓
Create sequences (3 timesteps → 1 forecast)
    ↓
Train LSTM (64 units, dropout 0.2)
    ↓
Evaluate (80/20 split)
    ↓
Save model (Keras + TensorFlow SavedModel)
    ↓
FastAPI Service (main.py)
    ↓
REST Endpoints (/health, /model-info, /predict)
    ↓
Prediction Response (5 edge densities)
```

---

## 🔑 Key Concepts

### What is LSTM?

A type of neural network that:

- **Remembers** long-term patterns (e.g., "Mondays are always congested 8-9am")
- **Forgets** irrelevant old events (e.g., "An accident 3 hours ago is now irrelevant")
- **Learns** non-linear relationships (e.g., traffic peaks vary by day of week/weather)

### LSTM vs ARIMA

| Aspect                 | ARIMA                  | LSTM                |
| ---------------------- | ---------------------- | ------------------- |
| **Pattern Type**       | Linear trends          | Non-linear spikes   |
| **Memory**             | Limited (p,d,q params) | Long-term via gates |
| **Sudden Changes**     | Poor                   | Good                |
| **Rush Hour Patterns** | Struggles              | Excellent           |
| **Data Amount Needed** | Small (100+)           | Large (1000+)       |

---

## 📁 Service Endpoints

### GET `/health`
Service health check.

**Response (200)**:
```json
{
  "status": "healthy",
  "message": "LSTM service is ready"
}
```

### GET `/model-info`
Retrieve model metadata and performance.

**Response (200)**:
```json
{
  "model_type": "LSTM",
  "input_shape": [3, 5],
  "output_shape": [5],
  "description": "Predicts edge density for next hour based on 3 hourly measurements",
  "edges": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
  "test_loss": 0.0698,
  "test_mae": 0.2084
}
```

### POST `/predict`
Predict traffic density for next hour.

**Request**:
```json
{
  "data": [
    [18.93, 10.13, 5.23, 4.14, 3.08],
    [24.02, 11.01, 8.98, 5.42, 4.26],
    [22.14, 9.34, 5.62, 4.57, 3.81]
  ]
}
```

**Parameters**:
- `data` (required): Array of 3 hourly measurements for 5 edges
  - Shape: (3, 5) — 3 timesteps × 5 edge density values
  - Values: Raw (non-normalized) density measurements

**Response (200)**:
```json
{
  "prediction": [25.47, 12.15, 9.23, 6.81, 5.14],
  "edge_ids": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"]
}
```

**Errors**:
- `400 Bad Request`: Invalid shape or missing `data`
- `503 Service Unavailable`: Model not loaded
- `500 Internal Server Error`: Prediction failed

---

## 🏋️ Training the Model

Training is handled by `app/models/lstm_train.py`:

```bash
python app/models/lstm_train.py
```

**What it does**:
1. Parses SUMO `edgeData.xml` 
2. Identifies top 5 most congested edges by average density
3. Normalizes data using MinMaxScaler
4. Creates sequences: 3 timesteps input → 1 timestep forecast
5. Builds LSTM model (64 units → Dense(32) → Dense(5))
6. Trains for 50 epochs with batch size 2
7. Evaluates on 20% test set (temporal split, no shuffle)
8. Saves model in Keras and TensorFlow SavedModel formats

**Output**:
- `app/trained_models/lstm_model.keras` (production model)
- `app/trained_models/lstm_model_tf/` (alternative format)
- `app/trained_models/scaler.pkl` (normalizer)

---

## 📊 Data Analysis Scripts

### edge-analysis.py
Analyze SUMO edge data:
```bash
python edge-analysis.py
```

Outputs:
- Total edge-interval records
- Unique edges in simulation
- Density/occupancy/waiting time statistics
- Top 10 edges by average density

### trip-analysis.py
Analyze SUMO trip data:
```bash
python trip-analysis.py
```

Outputs:
- Total trips and time range
- Trip duration statistics
- Waiting time statistics
- Departure delay statistics

---

## 📦 Dependencies

**Core**:
- `fastapi` (0.110.0): Web framework
- `uvicorn` (0.28.0): ASGI server
- `tensorflow` (2.15+): Model training and inference
- `keras` (3.0+): Model architecture

**Data Processing**:
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `scikit-learn`: MinMaxScaler normalization
- `scipy`: Signal processing utilities

**Utilities**:
- `pydantic`: Request/response validation
- `colorama`: Colored terminal output

See `requirements.txt` for exact versions.

---

## 🔧 Model Architecture

**Input**: (batch, 3, 5)
- 3 consecutive hourly measurements
- 5 edge density features

**Architecture**:
```
Input Layer (3, 5)
    ↓
LSTM(64 units, activation='relu')
    ↓
Dropout(0.2)
    ↓
Dense(32, activation='relu')
    ↓
Dropout(0.2)
    ↓
Dense(5)  # Output: 5 edge predictions
```

**Training**:
- Optimizer: Adam (lr=0.001)
- Loss: Mean Squared Error (MSE)
- Metrics: Mean Absolute Error (MAE)
- Epochs: 50
- Batch Size: 2
- Validation: 20% test set

**Performance**:
- Test Loss (MSE): 0.0698
- Test MAE: 0.2084 (normalized scale)

---

## 🚦 Supported Edges

Model trained on 5 most congested edges from SUMO simulation:

1. `-269002813`
2. `-55825089`
3. `617128762`
4. `-617128762`
5. `-312266114#2`

---

## 🔮 Future Enhancements

- [ ] 15-minute ahead forecasting (requires retraining)
- [ ] Achieve MAE < 10% on raw traffic values
- [ ] Handle missing sensor data (KNN imputation)
- [ ] Bidirectional LSTM for enhanced accuracy
- [ ] Attention mechanism for temporal weighting
- [ ] Real-time model retraining capability
- [ ] Weather data integration
- [ ] Integration with RL Inference Service

---

## 📚 Documentation

- [API Endpoints](../docs/lstm/endpoints.md)
- [Key Features](../docs/lstm/key-features.md)
- [File Structure](../docs/lstm/file-structure.md)
- [Overall Project Docs](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/)

---

## 🐛 Troubleshooting

### Model not loading
```
FileNotFoundError: app/trained_models/lstm_model.keras not found
```
**Solution**: Run `python app/models/lstm_train.py` to train and save model.

### Port already in use
```
OSError: [Errno 48] Address already in use
```
**Solution**: Change port with `--port 8001` or kill existing process.

### Shape mismatch in prediction
```
ValueError: Expected shape (3, 5), got (2, 5)
```
**Solution**: Ensure input data has exactly 3 hourly measurements.

---

## 📝 License

Part of TUS Engineering Team Project 2026.

---

## 🔗 Quick Links

- **GitHub**: https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation
- **API Docs (Local)**: http://localhost:8001/docs
- **Project Docs**: https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/