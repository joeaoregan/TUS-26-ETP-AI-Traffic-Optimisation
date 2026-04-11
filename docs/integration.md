# Service Integration Guide

## Architecture Overview

The system uses three independently deployed services orchestrated by the Java API Gateway:

```text
Client (SUMO / external)
        │
        ▼ JWT-authenticated requests
┌─────────────────────────┐
│   Java API Gateway      │  :8080
│   (Spring Boot)         │
└────────┬───────┬────────┘
         │       │  parallel calls (no pipeline)
         ▼       ▼
┌──────────┐  ┌────────────────┐
│RL Service│  │ LSTM Predictor │
│  :8000   │  │    :8001       │
└──────────┘  └────────────────┘
```

- **RL Inference Service** — PPO/MAPPO model, returns optimal signal phase (action 0–3) per junction
- **LSTM Predictor Service** — time-series model, returns predicted edge density for next hour (5 edges)
- **Java API Gateway** — authenticates clients, calls both services independently, aggregates responses

The RL and LSTM services are **not a pipeline** — the gateway calls them in parallel for their respective purposes. LSTM forecasts are not fed into the RL model.

---

## Request Flows

### Signal Phase Prediction (`POST /api/traffic/action`)

```text
Client → Gateway (JWT check)
       → RL Service POST /predict_action
       ← action (0–3) + signal state
       → Client
```

### Traffic Density Forecast (`GET /api/traffic/forecast`)

```text
Client → Gateway (JWT check)
       → LSTM Service POST /predict
       ← predicted density for 5 edges
       → Client (with inferenceTimeMs)
```

### Combined Health Check (`GET /api/traffic/health`)

```text
Client → Gateway
       → RL Service   GET /health  (parallel)
       → LSTM Service GET /health  (parallel)
       ← aggregated status: { inferenceService, lstmPredictorService }
       → Client
```

### Combined Model Info (`GET /api/traffic/model_info`)

```text
Client → Gateway
       → RL Service   GET /model_info  (parallel)
       → LSTM Service GET /model-info  (parallel)
       ← { "rl": {...}, "lstm": {...} }
       → Client
```

---

## API Endpoints Summary

### Java API Gateway (port 8080)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/auth/login` | — | Get JWT token |
| `GET` | `/api/traffic/action` | JWT | Demo: random junction action |
| `POST` | `/api/traffic/action` | JWT | Production: action for given junction |
| `POST` | `/api/traffic/reset` | JWT | Reset GRU hidden states |
| `GET` | `/api/traffic/forecast` | JWT | Proxy to LSTM single prediction |
| `POST` | `/api/traffic/forecast-batch` | JWT | Proxy to LSTM batch prediction |
| `GET` | `/api/traffic/model_info` | — | Combined RL + LSTM model metadata |
| `GET` | `/api/traffic/health` | — | Combined RL + LSTM health status |

### RL Inference Service (port 8000)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/predict_action` | Predict signal phase |
| `POST` | `/reset_hidden` | Reset GRU hidden states |
| `GET` | `/model_info` | Model architecture info |
| `GET` | `/health` | Health check |

### LSTM Predictor Service (port 8001)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/predict` | Predict density for next hour |
| `POST` | `/predict-batch` | Batch density predictions |
| `GET` | `/model-info` | Model metadata and performance |
| `GET` | `/metrics` | Service usage statistics |
| `GET` | `/health` | Health check |

---

## Deployment

### Local (Docker Compose)

```bash
docker compose up
```

Services start on ports 8000, 8001, 8080.

### AWS EC2

| Service | EC2 Private IP | Port |
|---------|---------------|------|
| RL Inference | 172.31.x.x | 8000 |
| LSTM Predictor | 172.31.47.204 | 8001 |
| Java Gateway | 172.31.x.x | 8080 |

Security groups allow traffic between services on private IPs only. Public access via gateway port 8080 only.

---

## Integration Testing

Run the end-to-end integration test (requires all 3 services running):

```bash
python lstm-predictor-service/test_rl_integration.py
```

Or test individual endpoints:

```bash
# Health (all services)
curl http://localhost:8080/api/traffic/health

# Get JWT token
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r .accessToken)

# Forecast via gateway
curl -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -X GET http://localhost:8080/api/traffic/forecast \
  -d '{"data":[[18.93,10.13,5.23,4.14,3.08],[24.02,11.01,8.98,5.42,4.26],[22.14,9.34,5.62,4.57,3.81]]}'

# Signal action via gateway
curl -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -X POST http://localhost:8080/api/traffic/action \
  -d '{"junctionId":"joinedS_265580996_300839357","observations":[0,1,0,0,0,1,0,1,0.12,0.08,0.33,0.41,0.22,0.55,0.18,0.62,0.70,0.81,0.50]}'
```

---

## Environment Variables

See `.env.example` in each service directory for full configuration reference.

| Variable | Service | Default | Purpose |
|----------|---------|---------|---------|
| `API_PORT` | RL / LSTM | 8000 / 8001 | Service port |
| `RL_INFERENCE_SERVICE_URL` | Gateway | `http://localhost:8000` | RL service base URL |
| `LSTM_PREDICTOR_SERVICE_URL` | Gateway | `http://localhost:8001/predict` | LSTM predict endpoint |
| `LSTM_PREDICTOR_SERVICE_TIMEOUT` | Gateway | `5000` | LSTM call timeout (ms) |
| `JWT_SECRET` | Gateway | — | JWT signing secret |
