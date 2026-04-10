# Trained LSTM Models

This directory contains trained LSTM models for traffic density prediction on the top 5 most congested edges in the SUMO traffic simulation network.

## Model Overview

**Purpose:** Predict edge density (vehicles/km) for the next hour based on the previous 3 hourly measurements.

**Training Data:** 
- Source: `SUMO/Results/MAPPO/edgeData.xml`
- Time Range: 0-43,200 seconds (~12 hours)
- Edges: Top 5 by average density
  - `-269002813` (density: 24.77)
  - `-55825089` (density: 8.72)
  - `617128762` (density: 8.51)
  - `-617128762` (density: 5.12)
  - `-312266114#2` (density: 4.35)

**Training Metrics:**
- Test Loss (MSE): 0.0698
- Test MAE: 0.2084
- Epochs: 50
- Batch Size: 2
- Optimizer: Adam (lr=0.001)

---

## Model Formats

### 1. Keras Native Format (`.keras`)
**File:** `lstm_model.keras`

**Use When:**
- Fast local inference and testing
- Integration with Keras/TensorFlow Python applications
- Development and debugging

**Advantages:**
- Smaller file size
- Faster loading
- Native Keras 3 format (future-proof)

**Loading:**
```python
import tensorflow as tf
model = tf.keras.models.load_model('lstm_model.keras')
```

### 2. TensorFlow SavedModel (Directory Format)

**Directory**: `lstm_model_tf/`

**Use When**:

- Production deployment
- TensorFlow Serving integration
- Cross-platform/language compatibility
- REST API inference services

**Advantages**:

- Optimized for production inference
- Language-agnostic (can be served via REST, gRPC)
- Compatible with TensorFlow Lite conversion
- Better support for model versioning

**Loading**:

```python
import tensorflow as tf
model = tf.keras.models.load_model('lstm_model_tf')
```

Serving with TensorFlow Serving:
  
```python
tensorflow_model_server --port=8500 --rest_api_port=8501 \
  --model_name=lstm_traffic --model_base_path=/path/to/lstm_model_tf
```

### 3. HDF5 Format (Legacy)
Status: ⚠️ Not saved - Deprecated in Keras 3

Legacy .h5 format is no longer used. Use .keras or SavedModel instead.

---

## Model Specifications

### Input

- **Shape**: (batch_size, 3, 5)
    - batch_size: Number of samples to predict
    - 3: Sequence length (3 hourly time steps)
    - 5: Number of edges/features
- **Data Type**: float32
- **Value Range**: [0.0, 1.0] (normalized via MinMaxScaler)

### Output

- **Shape**: (batch_size, 5)
    - Predicted density for each of the 5 edges at the next hour
- **Data Type**: float32
- **Value Range**: [0.0, 1.0] (normalized)

### Architecture

```
Input Layer
  ↓
LSTM (64 units, ReLU activation)
  ↓
Dropout (0.2)
  ↓
Dense (32 units, ReLU activation)
  ↓
Dropout (0.2)
  ↓
Dense (5 units) - Output Layer
```

---

## Data Preprocessing

### Required: MinMaxScaler

Before feeding data to the model, you must normalize it using the saved scaler.

**File**: `scaler.pkl`

**Usage**:

```python
import pickle
import numpy as np

# Load scaler
scaler = pickle.load(open('scaler.pkl', 'rb'))

# Normalize raw edge density data
# raw_data shape: (timesteps, 5_edges)
normalized_data = scaler.transform(raw_data)

# Create sequences for prediction
# sequences shape: (num_sequences, 3, 5)
```

### Example: Complete Inference Pipeline

```python
import tensorflow as tf
import pickle
import numpy as np

# 1. Load model
model = tf.keras.models.load_model('lstm_model.keras')

# 2. Load scaler
scaler = pickle.load(open('scaler.pkl', 'rb'))

# 3. Prepare input data (example: last 3 hours of edge density)
raw_data = np.array([
    [18.93, 10.13, 5.23, 4.14, 3.08],  # Hour 0
    [24.02, 11.01, 8.98, 5.42, 4.26],  # Hour 1
    [22.14,  9.34, 5.62, 4.57, 3.81]   # Hour 2
])

# 4. Normalize
normalized = scaler.transform(raw_data)

# 5. Reshape for LSTM (batch_size=1, timesteps=3, features=5)
input_sequence = np.expand_dims(normalized, axis=0)

# 6. Predict next hour
prediction_normalized = model.predict(input_sequence)

# 7. Denormalize to get actual density values
prediction_raw = scaler.inverse_transform(prediction_normalized)

print("Predicted density for next hour:", prediction_raw[0])
# Output: [23.5, 9.8, 7.2, 5.1, 4.1] (approximately)
```

## Training Script
Models were trained using:

```bash
python lstm-predictor-service/app/models/lstm_train.py
```

### Source Data Path: SUMO/Results/MAPPO/edgeData.xml

To retrain with new data:

1. Update the XML path in the training script
1. Run the training script
1. Models will be saved to this directory, overwriting previous versions

### Model Performance

| Metric | Value |
| ------ | ----- |
| Test Loss (MSE)	| 0.0698	|
| Test MAE	|	0.2084	|
| Training Samples	|	9 sequences	|
| Test Samples	|	2 sequences	|
| Input Sequence Length	|	3 hours	|

**Note**: Small dataset (12 hourly intervals) - model is proof-of-concept. For production use, retrain with:

- Longer simulation runs (100+ hours)
- Finer time granularity (5-10 minute intervals)
- More diverse traffic scenarios

### Integration with FastAPI Service

See lstm-predictor-service/app/main.py for REST API endpoints that load and use these models.

---

## Troubleshooting

### Model not found

```code
FileNotFoundError: lstm_model.keras not found
```
**Solution**: Ensure you've run lstm_train.py to generate the models.

### Scaler mismatch

```code
ValueError: X has 4 features but scaler was fitted with 5
```

**Solution**: Always use the saved scaler.pkl that was trained with the same data as the model.

### Incompatible shape
```Code
ValueError: Input 0 of layer "lstm" is incompatible with the layer: expected shape (None, 3, 5), found shape (None, 2, 5)
```

**Solution**: Ensure input sequence has exactly 3 timesteps and 5 features.

---

## References

- **TensorFlow/Keras Documentation**: https://www.tensorflow.org/api_docs/python/tf/keras
- **Model Training**: lstm_train.py
- **Data Analysis**: edge-analysis.py, trip-analysis.py