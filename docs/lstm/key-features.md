# Key Features (LSTM Traffic Predictor)

[Feature List](../features.md#lstm-traffic-predictor-service)

## Prime Target

**Status**: Not yet implemented

- [ ] Achieve MAE < 10% on raw traffic values

## Time-Series Forecasting

- **LSTM Neural Network**: Long Short-Term Memory architecture for temporal pattern recognition
  - [x] Learns long-term traffic patterns (morning/evening peaks)
  - [x] Remembers relevant historical events, forgets irrelevant ones
  - [x] Handles non-linear traffic spikes and sudden congestion
  - [x] **Architecture**: 64-unit LSTM layer with dropout regularization (0.2)

## Prediction Capabilities

- [x] **1-Hour Ahead Forecasting**: Predicts edge traffic density for the next hour
- [x] **Sequence Length**: Uses 3 hourly measurements (timesteps) for predictions
- [x] **Achieved Performance**: MAE 0.2084 on normalized density values (test set)
- [x] **Input**: 3 consecutive hourly measurements × 5 edge features
- [x] **Output**: Predicted density for each of the 5 edges at next hour

## Data Processing

- [x] **SUMO Integration**: Loads historical traffic data from `edgeData.xml`
- [x] **Feature Selection**: Focuses on top 5 most congested edges by average density
- [x] **Normalization**: MinMaxScaler (0-1 range) for numerical stability
- [x] **Sliding Windows**: Creates sequences of 3 timesteps with 1-step forecast target
- [x] **Data Split**: 80/20 train-test split (temporal, no shuffle)

## Supported Edges

Trained on the 5 most congested edges from SUMO simulation:
- `-269002813`
- `-55825089`
- `617128762`
- `-617128762`
- `-312266114#2`

## API Endpoints

- [x] `GET /health` — Service health check
- [x] `GET /model-info` — Model architecture and performance metadata
- [x] `POST /predict` — Predict edge density for next hour

**Request Format**: Array of (3 × 5) raw density measurements
**Response Format**: Array of 5 predicted density values

## Model Performance

- **Test Loss (MSE)**: 0.0698
- **Test MAE**: 0.2084 (normalized scale)
- **Training**: 50 epochs with batch size 2
- **Optimizer**: Adam (learning rate: 0.001)
- **Validation**: Evaluated on 20% test set

## Integration

- [ ] **RL Inference Service**: Can consume predictions for context-aware signal timing decisions
- [ ] **API Gateway**: Can proxy `/predict` requests with unified authentication
- [x] **SUMO Source**: Uses simulation outputs (`edgeData.xml`) as training data

## Future Enhancements

- [ ] 15-minute ahead forecasting (requires model retraining)
- [ ] Handle missing sensor data (KNN imputation)
- [ ] Bidirectional LSTM for enhanced accuracy
- [ ] Attention mechanism for temporal weighting
- [ ] Real-time model retraining capability
- [ ] Weather data integration