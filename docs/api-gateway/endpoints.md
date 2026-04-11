# API Endpoints (Java API Gateway)

## Authentication

!!! success "POST `/api/auth/login`"
    Authenticate and receive a JWT bearer token.

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

    **Errors**:
    - `401`: Invalid username or password

## Traffic Prediction

!!! note "GET `/api/traffic/action`"
    **Demo endpoint** - Picks a random junction and generates dummy observations. Requires JWT authentication.

    **Headers**:
    ```
    Authorization: Bearer <your_token>
    ```

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

    **Response (Fallback - Inference Down)**:
    ```json
    {
      "junctionId": "300839359",
      "predictedAction": 0,
      "signalState": "RED",
      "timestamp": 1710000000000,
      "status": "fallback_mode (inference service down)"
    }
    ```

!!! success "POST `/api/traffic/action`"
    **Production endpoint** - Accepts junction ID and custom observation vector. Requires JWT authentication.

    **Headers**:
    ```
    Authorization: Bearer <your_token>
    Content-Type: application/json
    ```

    **Request**:
    ```json
    {
      "junctionId": "joinedS_265580996_300839357",
      "observations": [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.12, 0.08, 0.33, 0.41, 0.22, 0.55, 0.18, 0.62, 0.70, 0.81, 0.50],
      "metadata": "morning-peak"
    }
    ```

    **Response (200)**: Same structure as demo endpoint

    **Errors**:
    - `400`: Missing or invalid `junctionId` / `observations`
    - `400`: Observations exceed maximum size (19)
    - `401`: Missing or invalid JWT token
    - `500`: Unexpected internal error

## State Management

!!! success "POST `/api/traffic/reset`"
    **Reset GRU hidden states** for all junctions (call at start of simulation run). Requires JWT authentication.

    **Headers**:
    ```
    Authorization: Bearer <your_token>
    ```

    **Response (200)**:
    ```json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

## Traffic Forecasting (LSTM)

!!! success "GET `/api/traffic/forecast`"
    **Proxy to LSTM predictor** - Predict traffic density for the next hour based on 3 recent hourly measurements. Requires JWT authentication.

    **Headers**:
    ```
    Authorization: Bearer <your_token>
    Content-Type: application/json
    ```

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

    **Response (200)**:
    ```json
    {
      "prediction": [25.47, 12.15, 9.23, 6.81, 5.14],
      "edge_ids": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
      "inferenceTimeMs": 48.3
    }
    ```

    **Errors**:
    - `400`: Invalid input shape (expected 3×5)
    - `401`: Missing or invalid JWT token
    - `503`: LSTM predictor service unavailable

!!! success "POST `/api/traffic/forecast-batch`"
    **Batch proxy to LSTM predictor** - Predict traffic density for multiple sequences. Requires JWT authentication.

    **Headers**:
    ```
    Authorization: Bearer <your_token>
    Content-Type: application/json
    ```

    **Request**:
    ```json
    {
      "sequences": [
        [
          [18.93, 10.13, 5.23, 4.14, 3.08],
          [24.02, 11.01, 8.98, 5.42, 4.26],
          [22.14, 9.34, 5.62, 4.57, 3.81]
        ],
        [
          [24.02, 11.01, 8.98, 5.42, 4.26],
          [22.14, 9.34, 5.62, 4.57, 3.81],
          [20.50, 10.75, 6.10, 4.90, 3.50]
        ]
      ]
    }
    ```

    **Response (200)**:
    ```json
    {
      "predictions": [
        [25.47, 12.15, 9.23, 6.81, 5.14],
        [24.02, 11.85, 8.50, 6.20, 4.80]
      ],
      "edge_ids": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
      "num_predictions": 2,
      "inference_time_ms": 65.3
    }
    ```

    **Errors**:
    - `400`: Invalid sequence shape or empty list
    - `401`: Missing or invalid JWT token
    - `503`: LSTM predictor service unavailable

## Model Information

!!! note "GET `/api/traffic/model_info`"
    **Combined model metadata** — Returns architecture and performance info for both RL and LSTM models. No authentication required.

    **Response (200)**:
    ```json
    {
      "rl": {
        "model_type": "MAPPO",
        "n_agents": 3,
        "obs_size": 19,
        "action_size": 4,
        "hidden_state_size": 64
      },
      "lstm": {
        "model_type": "LSTM",
        "input_shape": [3, 5],
        "output_shape": [5],
        "description": "Predicts edge density for next hour based on 3 hourly measurements",
        "edges": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
        "test_loss": 0.0698,
        "test_mae": 0.2084
      }
    }
    ```

## Health & Monitoring

!!! note "GET `/api/traffic/health`"
    **Service health check** - Verifies both RL inference and LSTM predictor availability. No authentication required.

    **Response (200 - Healthy)**:
    ```json
    {
      "status": "healthy",
      "inferenceService": "up",
      "lstmPredictorService": "up",
      "timestamp": 1710000000000
    }
    ```

    **Response (503 - Degraded)**:
    ```json
    {
      "status": "degraded",
      "inferenceService": "up",
      "lstmPredictorService": "down",
      "timestamp": 1710000000000
    }
    ```