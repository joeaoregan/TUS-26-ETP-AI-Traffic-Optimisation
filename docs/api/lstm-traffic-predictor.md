# LSTM Traffic Predictor

## Live Documentation

**[LSTM Swagger UI](http://localhost:8001/docs)** (Local Development)

**Production:** https://lstm-predictor-service.onrender.com/docs (future deployment)

---

## Detailed Endpoint Documentation

See **[Endpoints](../lstm/endpoints.md)** for comprehensive specifications of:

- `POST /forecast` — Predict vehicle flow 15 minutes ahead
- `GET /health` — Service health check
- `GET /model_info` — Model architecture and performance metadata

---

## Model Information

The LSTM service uses a Long Short-Term Memory neural network for time-series traffic forecasting:

- **Architecture:** LSTM layers with temporal attention
- **Input:** Historical traffic data (60-minute lookback window)
- **Output:** Vehicle flow predictions (15 minutes ahead)
- **Target Accuracy:** MAE < 10%
- **Supported Junctions:** All 5 major junctions

See **[Key Features](../lstm/key-features.md)** for neural network architecture details and time-series capabilities.

---

## Data Integration

The LSTM service integrates with SUMO simulation outputs:

- **Input Source:** `edgeData.xml` from SUMO simulations
- **Features:** Vehicle count, average speed, occupancy
- **Training:** Historical simulation data
- **Usage:** Provides traffic flow context to RL inference service

---

## Architecture & Features

- **[Architecture](../lstm/architecture.md)** — Technology stack, deployment, file structure, configuration
- **[Key Features](../lstm/key-features.md)** — Time-series forecasting, SUMO integration, supported junctions

---

## Swagger Auto-Generation

Documentation is automatically generated from Python type hints and docstrings:

- **FastAPI decorators** — `@app.get()`, `@app.post()`
- **Function docstrings** — Endpoint descriptions
- **Pydantic type hints** — Request/response schemas
- **Response models** — Expected HTTP structures
- **Tags** — Endpoint organization

This ensures documentation stays in sync with implementation.