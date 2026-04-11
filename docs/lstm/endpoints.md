# API Endpoints (LSTM Traffic Predictor)

## Health & Information

!!! note "GET `/health`"
    Service health check.

    Response (200):

    ```json
    {
      "status": "healthy",
      "message": "LSTM service is ready"
    }
    ```

!!! note "GET `/model-info`"
    Retrieve LSTM model metadata.

    Response (200):

    ```json
    {
      "model_type": "LSTM",
      "input_shape": [3, 5],
      "output_shape": [5],
      "description": "Predicts edge density for next hour based on 3 hourly measurements",
      "edges": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
      "test_loss": 0.0698,
      "test_mae": 0.2084
    }
    ```

## Traffic Density Prediction

!!! success "POST `/predict`"
    Predict traffic density for the next hour.

    **Request:**

    ```json
    {
      "data": [
        [18.93, 10.13, 5.23, 4.14, 3.08],
        [24.02, 11.01, 8.98, 5.42, 4.26],
        [22.14, 9.34, 5.62, 4.57, 3.81]
      ]
    }
    ```

    **Parameters:**
    - `data` (required): Array of 3 hourly measurements for 5 edges. Shape: (3, 5)
      - 3 timesteps (hours)
      - 5 edge density values per timestep

    **Response (200):**

    ```json
    {
      "prediction": [25.47, 12.15, 9.23, 6.81, 5.14],
      "edge_ids": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"]
    }
    ```

    **Error Responses:**

    - `400 Bad Request`: Invalid shape or missing `data` field
      ```json
      {
        "detail": "Expected shape (3, 5), got (2, 5)"
      }
      ```

    - `503 Service Unavailable`: Model not loaded
      ```json
      {
        "detail": "Model not loaded"
      }
      ```

    - `500 Internal Server Error`: Prediction inference failed
      ```json
      {
        "detail": "Prediction error: [error details]"
      }
      ```

---

## Testing

### Health Check

```bash
curl http://localhost:8001/health
```

### Model Info

```bash
curl http://localhost:8001/model-info
```

### Predict Density

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "data":[
      [18.93,10.13,5.23,4.14,3.08],
      [24.02,11.01,8.98,5.42,4.26],
      [22.14,9.34,5.62,4.57,3.81]
    ]
  }' \
  http://localhost:8001/predict
```

---

## Notes

- **Port**: 8001
- **Input Format**: Raw (non-normalized) traffic density values
- **Output Format**: Predicted density values for next hour (denormalized)
- **Normalization**: Handled internally using MinMaxScaler
- **Top 5 Edges**: Model trained on the 5 most congested edges from SUMO simulation