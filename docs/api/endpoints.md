# 📡 API Endpoints (Quick Reference)

## 🔐 Authentication Summary

| Service | Endpoints | Auth Required |
|---------|-----------|---|
| [**Java Gateway**](#java-api-gateway-port-8080) | `/api/auth/login`, `/api/traffic/*` | ✅ **JWT** (except login & health) |
| [**Inference Service**](#python-inference-service-port-8000) | All endpoints | ❌ **Public** |
| [**LSTM Predictor**](#lstm-traffic-predictor-port-8001) | All endpoints | ❌ **Public** |

---

## Java API Gateway (Port 8080)

!!! success "POST `/api/auth/login`"
    **Authenticate and receive JWT bearer token** — No authentication required (public endpoint)
    
    **Request**:
    ```json
    {
      "username": "admin",
      "password": "admin123"
    }
    ```
    
    **Response (200)**:
    ```json
    {
      "tokenType": "Bearer",
      "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
      "expiresIn": 3600,
      "timestamp": 1710000000000
    }
    ```
    
    **Errors**: `401` Invalid credentials

!!! note "GET `/api/traffic/action`"
    **Demo prediction** (random junction, auto-generated observations) — **Requires JWT**
    
    **Headers**: `Authorization: Bearer <token>`
    
    **Response (200)**: 
    ```json
    {
      "junctionId": "300839359",
      "predictedAction": 1,
      "signalState": "YELLOW",
      "timestamp": 1710000000000,
      "status": "success"
    }
    ```

!!! success "POST `/api/traffic/action`"
    **Production prediction** (custom observations) — **Requires JWT**
    
    **Headers**: `Authorization: Bearer <token>`
    
    **Request**:
    ```json
    {
      "junctionId": "joinedS_265580996_300839357",
      "observations": [0.0, 1.0, 0.0, ...],
      "metadata": "morning-peak"
    }
    ```
    
    **Response (200)**: Same as demo
    
    **Errors**: `400` Invalid obs, `401` Invalid token

!!! success "POST `/api/traffic/reset`"
    **Reset GRU hidden states** — **Requires JWT**
    
    **Headers**: `Authorization: Bearer <token>`
    
    **Response (200)**:
    ```json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

!!! note "GET `/api/traffic/health`"
    **Service health check** — No authentication required (public endpoint)
    
    **Response (200 - Healthy)**:
    ```json
    {
      "status": "healthy",
      "inferenceService": "up",
      "timestamp": 1710000000000
    }
    ```
    
    **Response (503 - Degraded)**:
    ```json
    {
      "status": "degraded",
      "inferenceService": "down",
      "timestamp": 1710000000000
    }
    ```

---

## Python Inference Service (Port 8000)

!!! success "POST `/predict_action`"
    **Predict optimal signal action** — No authentication
    
    **Request**:
    ```json
    {
      "junction_id": "300839359",
      "obs_data": [0.0, 1.0, 1.0, 0.12, 0.33, 0.41, 0.22, 0.55]
    }
    ```
    
    **Response (200)**:
    ```json
    {
      "junction_id": "300839359",
      "action": 1,
      "confidence": 0.87
    }
    ```
    
    **Errors**: 
    - `404`: Unknown junction
    - `400`: Observation size > 19
    - `503`: Model not loaded

!!! success "POST `/reset_hidden`"
    **Reset GRU hidden states** (call at start of simulation run) — No authentication
    
    **Response (200)**:
    ```json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

!!! note "GET `/health`"
    **Service health check**
    
    **Response (200)**:
    ```json
    {
      "status": "healthy",
      "model_loaded": true,
      "junctions": [
        "joinedS_265580996_300839357",
        "300839359",
        "265580972",
        "1270712555",
        "8541180897"
      ]
    }
    ```

!!! note "GET `/model_info`"
    **Model architecture and junction metadata**
    
    **Response (200)**:
    ```json
    {
      "architecture": "RNNAgent (GRU)",
      "input_shape": 24,
      "hidden_dim": 128,
      "n_actions": 4,
      "n_agents": 5,
      "junctions": {
        "300839359": {
          "agent_index": 1,
          "avail_actions": [1, 1, 0, 0],
          "valid_actions": 2
        }
      }
    }
    ```

!!! note "GET `/docs`"
    **Interactive Swagger UI** — Auto-generated OpenAPI documentation

---

## LSTM Traffic Predictor (Port 8001)

!!! note "GET `/health`"
    **Service health check**
    
    **Response (200)**:
    ```json
    {
      "status": "healthy",
      "model_loaded": true,
      "model_version": "1.0",
      "forecast_horizon": 15,
      "timestamp": 1710000000000
    }
    ```

!!! success "POST `/forecast`"
    **Predict vehicle flow 15 minutes ahead**
    
    **Request**:
    ```json
    {
      "junction_id": "300839359",
      "historical_data": [
        {"timestamp": 1710000000, "vehicle_count": 45, "avg_speed": 35.2, "occupancy": 0.12}
      ]
    }
    ```
    
    **Response (200)**:
    ```json
    {
      "junction_id": "300839359",
      "forecast_timestamp": 1710000900,
      "predicted_flow": 52,
      "confidence": 0.92,
      "status": "success",
      "timestamp": 1710000000000
    }
    ```

!!! note "GET `/model_info`"
    **LSTM model metadata**
    
    **Response (200)**:
    ```json
    {
      "model_type": "LSTM",
      "model_version": "1.0",
      "input_features": 3,
      "input_window": 60,
      "output_window": 15,
      "target_accuracy": "MAE < 10%",
      "trained_on_junctions": ["300839359", "265580972", ...]
    }
    ```

!!! note "GET `/docs`"
    **Interactive Swagger UI**

---

## For Detailed Specifications

See service-specific documentation:
- **[Java API Gateway Endpoints](../api-gateway/endpoints.md)** — Full specs with error handling
- **[Python Inference Service Endpoints](../inference-service/endpoints.md)** — Full specs
- **[LSTM Predictor Endpoints](../lstm/endpoints.md)** — Full specs