# File Structure (LSTM Traffic Predictor)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
lstm-predictor-service/
├── app/
│   ├── main.py                              # FastAPI application (LSTM model inference)
│   ├── data/
│   │   ├── loader.py                        # SUMO edgeData.xml parser
│   │   └── preprocessor.py                  # Data normalization, windowing, scaling
│   ├── models/
│   │   └── lstm_model.pt                    # Trained LSTM model weights (TensorFlow/Keras) [FUTURE]
│   ├── templates/
│   │   └── index.html                       # Landing page with navigation links
│   └── static/
│       ├── logo.png                         # Project logo
│       └── favicon.ico                      # Browser tab icon
├── Dockerfile                               # Python 3.9-slim base, Uvicorn server
├── requirements.txt                         # FastAPI, Uvicorn, TensorFlow, Keras, Pandas, Numpy, scikit-learn
├── .env.example                             # Template: API_PORT, SUMO_DATA_PATH, MODEL_PATH, etc.
├── .gitignore
├── README.md                                # Setup and deployment guide
└── docker-compose.override.yml              # Local development overrides (optional)
```

---

## app/ Directory Structure

```
app/
├── main.py                                  # FastAPI instance, route handlers
│   ├── startup events (load model, initialize scaler)
│   ├── POST /forecast (junction_id, historical_data → predicted_flow, confidence)
│   ├── GET /health (service status, model_loaded)
│   ├── GET /model_info (model architecture, training date, target accuracy)
│   ├── GET / (landing page)
│   └── GET /docs (Swagger UI)
├── data/
│   ├── loader.py
│   │   ├── parse_sumo_edgedata_xml()
│   │   ├── extract_traffic_metrics()
│   │   └── handle_missing_data()
│   └── preprocessor.py
│       ├── normalize_features()
│       ├── create_sliding_windows()
│       ├── stationarity_check()
│       └── fit_scaler()
├── models/
│   └── lstm_model.pt (TensorFlow/Keras H5 format) [FUTURE]
├── templates/
│   └── index.html (static HTML with links)
└── static/
    └── assets (logo, favicon, etc.)
```

---

## Key Files

- **main.py** — FastAPI application:
  - LSTM model loading from `MODEL_PATH`
  - MinMaxScaler initialization for feature normalization
  - 5 route handlers (forecast, health, model_info, health)
  - Pydantic request/response models

- **data/loader.py** — SUMO integration:
  - Parse `edgeData.xml` from `SUMO_DATA_PATH`
  - Extract vehicle count, speed, occupancy metrics
  - Handle missing sensor data (KNN imputation)

- **data/preprocessor.py** — Feature engineering:
  - Scale traffic features to [0, 1] range
  - Create sliding windows (60-min lookback, 15-min forecast)
  - Check for stationarity
  - Handle categorical variables

- **models/lstm_model.pt** — Trained model (future):
  - Input shape: (batch, 60, 3) — 60 minutes × 3 features
  - Output: 15-min ahead vehicle flow prediction
  - Target MAE: < 10%

- **Dockerfile** — Production image build
  - Base: `python:3.9-slim`
  - Installs requirements
  - Runs: `uvicorn main:app --host 0.0.0.0 --port $API_PORT`

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `API_PORT` | `8001` | Service port |
| `SUMO_DATA_PATH` | `./data/edgeData.xml` | Path to SUMO output |
| `MODEL_PATH` | `./app/models/lstm_model.pt` | Path to trained model |
| `FORECAST_HORIZON` | `15` | Forecast window (minutes) |
| `LOOKBACK_WINDOW` | `60` | Historical window (minutes) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## Status

⚠️ **Framework Stage**: Endpoints defined, data pipeline ready. Requires model training on SUMO data to achieve MAE < 10%.