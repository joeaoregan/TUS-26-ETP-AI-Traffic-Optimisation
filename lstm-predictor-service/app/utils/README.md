# Utilities Module Documentation

## Overview
Utility functions and classes for LSTM-based traffic density forecasting. Includes metrics calculation, data preprocessing, feature engineering, and time series analysis.

---

## metrics.py

Evaluation metrics for model performance assessment.

### Functions:
- **`mae(y_true, y_pred)`** — Mean Absolute Error
  - Returns average absolute difference between predictions and actual values
  - Range: [0, ∞), lower is better
  
- **`mse(y_true, y_pred)`** — Mean Squared Error
  - Returns average squared difference between predictions and actual values
  - Penalizes larger errors more heavily than MAE
  - Range: [0, ∞), lower is better
  
- **`rmse(y_true, y_pred)`** — Root Mean Squared Error
  - Square root of MSE, same units as target variable
  - Useful for interpretability (e.g., "±2 vehicles/km prediction error")
  - Range: [0, ∞), lower is better

**Usage:**
```python
from app.utils.metrics import mae, mse, rmse
y_true = np.array([10.0, 20.0, 15.0])
y_pred = np.array([9.5, 21.0, 14.5])
print(mae(y_true, y_pred))    # 0.5
print(rmse(y_true, y_pred))   # 0.548
```

---

## feature_engineering.py

Data preprocessing and sequence generation for time series modeling.

### Functions:

- **`normalize_data(data)`** — Normalize to [0, 1] range
  - Uses MinMaxScaler from scikit-learn
  - Returns: (normalized_data, scaler) for later denormalization
  - Essential for LSTM training stability
  
- **`denormalize_data(normalized_data, scaler)`** — Reverse normalization
  - Converts predictions back to original scale
  - Required for interpretable results (e.g., density in vehicles/km)
  
- **`create_sequences(data, seq_length=3)`** — Create sliding window sequences
  - Converts time series into supervised learning format
  - Input: (N, n_features) → Output: X (N-seq_length, seq_length, n_features), y (N-seq_length, n_features)
  - Enables LSTM to learn temporal patterns

**Usage:**
```python
from app.utils.feature_engineering import normalize_data, create_sequences
raw_data = np.array([...])  # Shape: (N, 5)
normalized, scaler = normalize_data(raw_data)
X, y = create_sequences(normalized, seq_length=3)
# X.shape: (N-3, 3, 5) — 3 timesteps input, 5 features
# y.shape: (N-3, 5) — 1 timestep target
```

---

## stationarity.py

Time series stationarity testing and analysis.

### Functions:

- **`adf_test(timeseries)`** — Augmented Dickey-Fuller test
  - Tests for unit root (non-stationarity)
  - Returns: (test_statistic, p_value, is_stationary)
  - Null hypothesis: Series has unit root (non-stationary)
  - If p-value < 0.05: Reject null → Series is stationary ✓
  
- **`kpss_test(timeseries)`** — KPSS test (complementary to ADF)
  - Tests for stationarity around a trend
  - Returns: (test_statistic, p_value, is_stationary)
  - Null hypothesis: Series is stationary
  - If p-value > 0.05: Fail to reject null → Series is stationary ✓

- **`analyze_stationarity(timeseries)`** — Combined analysis
  - Runs both ADF and KPSS tests
  - Prints detailed results
  - Returns: consensus on stationarity

**Usage:**
```python
from app.utils.stationarity import analyze_stationarity
density_series = np.array([...])  # Time series data
analyze_stationarity(density_series)
# Output:
# ✓ ADF Test: Stationary (p=0.023)
# ✓ KPSS Test: Stationary (p=0.15)
# ✓ Consensus: Series is stationary
```

**Why it matters:**
- LSTM can handle non-stationary data better than traditional models
- Stationarity testing validates input data quality
- If non-stationary: Consider differencing or detrending

---

## preprocessor.py (in `app/models/`)

DataPreprocessor class for end-to-end data pipeline.

### Class: DataPreprocessor

- **`__init__(scaler_path)`** — Initialize with scaler location
  - Loads existing scaler or creates new one
  - Ensures consistent normalization across train/inference
  
- **`fit_scaler(data)`** — Fit MinMaxScaler on training data
  - Persists scaler to disk for later use
  - Call once during training
  
- **`normalize(data)`** — Normalize new data
  - Uses fitted scaler
  - For preprocessing both training and test data
  
- **`denormalize(normalized_data)`** — Convert predictions back to original scale
  - Required for interpretable results
  
- **`create_sequences(data, seq_length=3)`** — Static method for sliding window creation
  - Same as `feature_engineering.create_sequences()`
  - Integrated here for convenience
  
- **`create_sequences_with_validation_split(data, seq_length, train_split=0.8)`** — Create sequences + temporal split
  - Splits into train/validation while preserving time order
  - No shuffling (important for time series!)
  - Returns: X_train, X_val, y_train, y_val

### Function: prepare_prediction_input(historical_data, preprocessor, seq_length=3)

- Prepares real-time prediction input
- Takes 3 recent measurements, normalizes, and batches
- Returns: Ready-to-feed tensor for `model.predict()`

**Usage:**
```python
from app.models.preprocessor import DataPreprocessor, prepare_prediction_input

# Training
preprocessor = DataPreprocessor()
normalized = preprocessor.fit_scaler(raw_training_data)
X, y = DataPreprocessor.create_sequences(normalized)
# Train model...

# Inference
preprocessor = DataPreprocessor()  # Loads fitted scaler
recent_data = [[18.93, 10.13, 5.23, 4.14, 3.08],
               [24.02, 11.01, 8.98, 5.42, 4.26],
               [22.14, 9.34, 5.62, 4.57, 3.81]]
batch_input = prepare_prediction_input(recent_data, preprocessor)
prediction = model.predict(batch_input)
original_scale = preprocessor.denormalize(prediction)
```

---

## Testing

Run `test_utils_demo.py` to validate all utilities:

```bash
python lstm-predictor-service/test_utils_demo.py
```

Tests include:
- ✅ Metrics calculations
- ✅ Normalization/denormalization accuracy
- ✅ Sequence creation logic
- ✅ DataPreprocessor class
- ✅ Real SUMO edge data loading (optional)