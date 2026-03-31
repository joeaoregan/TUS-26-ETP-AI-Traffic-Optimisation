# 🔐 Environment Variables

## Python Service

```
MAPPO_AGENT_PATH=/app/trained_models/agent.th  # MAPPO checkpoint location
API_HOST=0.0.0.0                               # Bind address
API_PORT=8000                                  # Service port
```

## Java Gateway

```
RL_INFERENCE_SERVICE_URL=http://localhost:8000/predict_action
RL_INFERENCE_SERVICE_TIMEOUT=10000  # milliseconds
```
