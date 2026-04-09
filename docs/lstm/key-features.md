# Key Features (LSTM Traffic Predictor)

[Feature List](../features.md#lstm-traffic-predictor-service)

## Time-Series Forecasting

- **LSTM Neural Network**: Long Short-Term Memory architecture for temporal pattern recognition
  - Learns long-term traffic patterns (morning/evening peaks)
  - Remembers relevant historical events, forgets irrelevant ones
  - Handles non-linear traffic spikes and sudden congestion

## Prediction Capabilities

- **15-Minute Ahead Forecasting**: Predicts vehicle flow for the next 15 minutes
- **Target Accuracy**: MAE < 10% on historical validation data
- **Lookback Window**: Uses 60 minutes of historical data for predictions
- **Multi-Feature Input**: Considers vehicle count, average speed, and occupancy

## Data Processing

- **SUMO Integration**: Loads historical traffic data from `edgeData.xml`
- **Automatic Normalization**: Scales traffic features to 0-1 range
- **Missing Data Handling**: KNN imputation for gaps in sensor data
- **Sliding Windows**: Creates temporal windows for training

## Supported Junctions

Trained to forecast for all 5 major junctions:
- `joinedS_265580996_300839357`
- `300839359`
- `265580972`
- `1270712555`
- `8541180897`

## API Endpoints

- `GET /health` — Service health check
- `GET /model_info` — Model architecture and performance metadata
- `POST /forecast` — Predict vehicle flow 15 minutes ahead

## Integration

- **Optional Consumer**: RL Inference Service can use forecasts for context-aware decisions
- **API Gateway**: Can proxy forecast requests with unified authentication
- **SUMO Source**: Uses simulation outputs as training data