# File Structure (LSTM Traffic Predictor)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
lstm-predictor-service/
├── app/
│   ├── main.py
│   ├── images/
│   │   ├── logo.png
│   │   └── favicon.ico
│   ├── models/
│   │   ├── lstm_model.py
│   │   └── lstm_train.py
│   ├── trained_models/
│   │   ├── lstm_model.keras
│   │   ├── lstm_model_tf/
│   │   └── scaler.pkl
│   └── utils/
│       ├── stationarity.py
│       ├── feature_engineering.py
│       └── metrics.py
├── edge-analysis.py
├── trip-analysis.py
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── docker-compose.override.yml
```

---

## File Descriptions

### app/main.py
FastAPI application for inference:
- Loads trained LSTM model from `app/trained_models/lstm_model.keras`
- Initializes MinMaxScaler from `app/trained_models/scaler.pkl`
- Implements 4 endpoints: `/health`, `/model-info`, `/predict`, `/favicon.ico`
- Pydantic models for request/response validation
- Comprehensive error handling with HTTP exceptions
- Custom Swagger UI with favicon support

### app/models/lstm_train.py
Complete training pipeline:
- Parses SUMO `edgeData.xml` 
- Identifies top 5 most congested edges by average density
- Normalizes data using MinMaxScaler
- Creates sequences: 3 timesteps input → 1 timestep forecast target
- Builds LSTM model: 64 units → Dense(32) → Dense(5 outputs)
- Trains for 50 epochs, batch size 2
- Evaluates on 20% test set (temporal split, no shuffle)
- Saves in both Keras `.keras` and TensorFlow SavedModel formats
- Output: Test Loss (MSE) 0.0698, Test MAE 0.2084

### app/models/lstm_model.py
Data preparation and exploration script:
- Parses edgeData.xml from SUMO results
- Identifies top 5 congested edges
- Normalizes data with MinMaxScaler
- Outputs dataset shape and sample records for inspection

### app/trained_models/lstm_model.keras
Trained LSTM model (production format):
- Keras native format (TensorFlow 2.11+)
- Input: (batch, 3, 5) — 3 timesteps × 5 edges
- Output: (batch, 5) — 5 edge density predictions
- MAE: 0.2084 (normalized scale)
- MSE: 0.0698 (normalized scale)

### app/trained_models/lstm_model_tf/
Alternative TensorFlow SavedModel format:
- For production deployment with TensorFlow Serving
- Compatible with cloud platforms
- Includes model signature and metadata

### app/trained_models/scaler.pkl
MinMaxScaler pickle file:
- Fitted on training data
- Scales density values to [0, 1] range
- Used for both training and inference normalization
- Loaded at startup in main.py

### app/utils/
Utility modules:
- **stationarity.py**: Stationarity checking with scipy
- **feature_engineering.py**: Feature engineering functions (placeholder)
- **metrics.py**: Model evaluation metrics (placeholder)

### app/images/
Static assets:
- **logo.png**: Project logo (used in docs)
- **favicon.ico**: Browser tab icon

### edge-analysis.py
SUMO data analysis script:
- Parses edgeData.xml from SUMO simulation
- Computes density, occupancy, waiting time statistics
- Groups by edge and identifies top 10 most congested
- Useful for data exploration and validation

### trip-analysis.py
Trip statistics script:
- Parses tripinfo.xml from SUMO simulation
- Analyzes trip duration, departure delays, waiting times
- Computes aggregate statistics across all vehicle trips
- Useful for understanding overall traffic performance

### Dockerfile
Production container build:
- Base: `python:3.9-slim`
- Installs dependencies from requirements.txt
- Runs: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### requirements.txt
Python dependencies:
- FastAPI, Uvicorn (web framework)
- TensorFlow, Keras (model training/inference)
- Pandas, Numpy, scikit-learn (data processing)
- Colorama (colored terminal output)

### README.md
Service documentation:
- Quick start guide
- Data flow diagram
- LSTM concepts explanation
- Available endpoints

### .env.example
Environment variable template:
- API_PORT, MODEL_PATH, etc.

---

## Status

✅ **Fully Operational**

**Working:**
- [x] Data loading and preprocessing from SUMO
- [x] Model training on historical patterns
- [x] Inference service (3 endpoints)
- [x] Swagger UI documentation
- [x] Health monitoring and logging

**Future:**
- [ ] 15-minute ahead forecasting
- [ ] MAE < 10% on raw traffic values
- [ ] Handle missing sensor data (KNN imputation)
- [ ] Docker containerization
- [ ] Integration with RL Inference Service