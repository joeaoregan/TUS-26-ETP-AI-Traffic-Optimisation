# 📡 API Endpoints

## Python Service (Port 8000)

```
GET  /health              - Service health status (lists controlled junctions)
POST /predict_action      - Predict action for a junction (requires junction_id + obs_data)
POST /reset_hidden        - Reset GRU hidden states (call at start of each simulation run)
GET  /model_info          - MAPPO model details (architecture, junctions, action masks)
GET  /docs                - Swagger UI documentation
```

## Java Gateway (Port 8080)

```
GET  /api/traffic/health  - Service health status
GET  /api/traffic/action  - Demo prediction (random junction, auto-generated observations)
POST /api/traffic/action  - Predict action (requires junctionId + observations)
POST /api/traffic/reset   - Reset MAPPO GRU hidden states
```