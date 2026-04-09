# Architecture (LSTM)

## Technology Stack

- **Framework**: FastAPI 0.115.0 (async Python web framework)
- **Server**: Uvicorn 0.28.0 (ASGI server)
- **ML Framework**: TensorFlow/Keras 2.13.0 (LSTM neural networks)
- **Data Processing**: Pandas 2.0+ (time-series data manipulation)
- **Numerical Computing**: NumPy 1.26.4 (array operations)
- **Validation**: Pydantic 2.6.4 (request/response validation)
- **Templating**: Jinja2 3.1.3
- **Preprocessing**: scikit-learn 1.3+ (scaling, normalization)
- **Environment**: Python 3.9

## Deployment

- **Container**: Docker (Python 3.9-slim base)
- **Port**: 8001 (configurable via `API_PORT`)
- **Production URL**: https://lstm-predictor-service.onrender.com (planned)
- **Local Development**: http://localhost:8001

## File Structure

```
lstm-predictor-service/
├── app/
│   ├── main.py                 # FastAPI application & LSTM inference logic
│   ├── data/
│   │   ├── loader.py           # SUMO edgeData.xml parser
│   │   └── preprocessor.py     # Data normalization and windowing
│   ├── models/
│   │   └── lstm_model.pt       # Trained LSTM model weights (future)
│   ├── templates/
│   │   └── index.html          # Landing page
│   └── static/                 # Static assets (logo, favicon)
├── trained_models/
│   └── lstm_traffic_forecast.pt # Trained LSTM checkpoint (future)
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

## Configuration

| Environment Variables | Default | Purpose |
|---|---|---|
| `API_PORT` | `8001` | Service port |
| `SUMO_DATA_PATH` | `./data/edgeData.xml` | Path to SUMO traffic data |
| `MODEL_PATH` | `./app/models/lstm_model.pt` | Path to trained LSTM model |
| `FORECAST_HORIZON` | `15` | Forecast window (minutes ahead) |
| `LOOKBACK_WINDOW` | `60` | Historical window for LSTM input (minutes) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

## Core Components

**FastAPI Application** (`app/main.py`)

- Initializes the LSTM model and scaler on startup
- Handles HTTP prediction requests
- Provides health checks and model information endpoints
- Manages error responses and validation

**Data Loader** (`app/data/loader.py`)

- Parses SUMO `edgeData.xml` output files
- Extracts per-edge vehicle flow, speed, and occupancy data
- Handles missing or corrupt data gracefully

**Preprocessor** (`app/data/preprocessor.py`)

- Normalizes and scales raw traffic data using fitted scaler
- Creates sliding windows for LSTM input (lookback window)
- Handles stationarity transformations if needed

**LSTM Model** (`app/models/lstm_model.pt`)

- Trained TensorFlow/Keras LSTM network
- Input: Historical observation window (60 minutes, multi-feature)
- Output: Vehicle flow forecast for next 15 minutes
- Target accuracy: MAE < 10%

## Data Flow

```text
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

## Integration with Other Services

**Inference Service (rl-inference-service)**

- LSTM forecasts are optionally consumed by the RL inference service
- Provides traffic flow context for decision-making
- Port: 8000

**API Gateway (java-api-gateway)**

- Gateway can optionally proxy forecast requests to LSTM service
- Provides unified API authentication and orchestration
- Port: 8080

**SUMO Simulation (SUMO/)**

- Generates edgeData.xml output files
- Source of truth for historical traffic data
- Used for model training and validation