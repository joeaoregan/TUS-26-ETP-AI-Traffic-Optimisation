# API Endpoints

## Traffic Prediction

!!! note "GET `/api/traffic/action`"
    **Demo endpoint** - Picks a random junction and generates dummy observations.

    **Response (200)**:
    ``` json
    {
      "junctionId": "300839359",
      "predictedAction": 1,
      "signalState": "YELLOW",
      "timestamp": 1710000000000,
      "status": "success"
    }
    ```

    **Response (Fallback - Inference Down)**:
    ``` json
    {
      "junctionId": "300839359",
      "predictedAction": 0,
      "signalState": "RED",
      "timestamp": 1710000000000,
      "status": "fallback_mode (inference service down)"
    }
    ```

!!! success "POST `/api/traffic/action`"
    **Production endpoint** - Accepts junction ID and custom observation vector.

    **Request**:
    ``` json
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
    - `500`: Unexpected internal error

## State Management

!!! success "POST `/api/traffic/reset`"
    **Reset GRU hidden states** for all junctions (call at start of simulation run).

    **Response (200)**:

    ``` json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

## Health & Monitoring

!!! note "GET `/api/traffic/health`"
    **Service health check** - Verifies inference service availability.

    **Response (200 - Healthy)**:
    ``` json
    {
      "status": "healthy",
      "inferenceService": "up",
      "timestamp": 1710000000000
    }
    ```

    **Response (503 - Degraded)**:
    ``` json
    {
      "status": "degraded",
      "inferenceService": "down",
      "timestamp": 1710000000000
    }
    ```
