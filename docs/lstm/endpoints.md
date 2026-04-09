# API Endpoints

## Health & Information

!!! note "GET `/health`"
    Service health check.

    Response (200):

    ```json
    {
      "status": "healthy",
      "model_loaded": true,
      "model_version": "1.0",
      "forecast_horizon": 15,
      "timestamp": 1710000000000
    }
    ```

!!! note "GET `/model_info`"
    Retrieve LSTM model metadata.

    Response (200):

    ```json
    {
      "model_type": "LSTM",
      "model_version": "1.0",
      "input_features": 3,
      "input_window": 60,
      "output_window": 15,
      "target_accuracy": "MAE < 10%",
      "training_date": "2026-04-01",
      "trained_on_junctions": ["300839359", "265580972", "1270712555", "8541180897", "joinedS_265580996_300839357"],
      "timestamp": 1710000000000
    }
    ```

## Traffic Forecasting

!!! success "POST `/forecast`"
    Predict vehicle flow 15 minutes ahead.

    Request:

    ```json
    {
      "junction_id": "300839359",
      "historical_data": [
        {"timestamp": 1710000000, "vehicle_count": 45, "avg_speed": 35.2, "occupancy": 0.12},
        {"timestamp": 1710000060, "vehicle_count": 48, "avg_speed": 34.8, "occupancy": 0.13}
      ]
    }
    ```

    Response (200):

    ```json
    {
      "junction_id": "300839359",
      "forecast_timestamp": 1710000900,
      "predicted_flow": 52,
      "confidence": 0.92,
      "lookback_window": 60,
      "forecast_window": 15,
      "status": "success",
      "timestamp": 1710000000000
    }
    ```

    Errors:

    - `400`: Missing or invalid `junction_id` / `historical_data`
    - `400`: Insufficient data points (< lookback window)
    - `500`: Model inference error