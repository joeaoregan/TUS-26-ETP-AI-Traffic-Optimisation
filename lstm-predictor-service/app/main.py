# main.py
# FastAPI service for LSTM traffic prediction

import os
import time
from datetime import datetime
from typing import List, Optional

import numpy as np
from colorama import Fore, init
from fastapi import FastAPI, HTTPException, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict

init(autoreset=True)

class HealthResponse(BaseModel):
    status: str
    message: str
    service: str
    version: str
    
class ModelInfoResponse(BaseModel):
    model_type: str
    input_shape: List[int]
    output_shape: List[int]
    description: str
    edges: List[str]
    test_loss: float
    test_mae: float
    training_samples: int
    test_samples: int
    sequence_length: int
    batch_prediction_supported: bool
    max_batch_size: int

class MetricsResponse(BaseModel):
    service: str
    version: str
    status: str
    total_predictions: int
    total_batch_predictions: int
    avg_inference_time_ms: float
    last_prediction_time: str
    model_loaded: bool
    scaler_loaded: bool

tags_metadata = [
    {
        "name": "LSTM Predictor",
        "description": "Endpoints for traffic density prediction using LSTM model.",
    },
    {
        "name": "System Health",
        "description": "Endpoints to monitor service status and model availability.",
    },
    {
        "name": "Navigation",
        "description": "Main landing pages and UI components.",
    },
]

# Initialize FastAPI
app = FastAPI(
    title="LSTM Traffic Predictor",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,    
    openapi_tags=tags_metadata,
    servers=[
        {"url": "http://localhost:8001", "description": "Local development server"},
        {"url": "https://lstm-predictor-service.onrender.com/", "description": "Production Cloud server (Render)"},
    ],
    description="""
<img src="static/logo.png" width="360" alt="LSTM Traffic Prediction Logo" />

## LSTM-Based Traffic Density Prediction

Real-time edge congestion forecasting using Long Short-Term Memory neural networks.

### Overview
Predicts traffic density for the next hour based on 3 hourly measurements from the 5 most congested edges.

### Key Features
- **LSTM Neural Network**: 64-unit LSTM with dropout regularization
- **Real-time Predictions**: Sub-100ms inference latency
- **Normalized Input**: MinMax scaling for stable predictions
- **Production Ready**: TensorFlow SavedModel format support
- **Batch Predictions**: Multi-step ahead forecasting for RL integration

### Model Performance
- **Test Loss (MSE)**: 0.0698
- **Test MAE**: 0.2084
- **Input**: (3 timesteps, 5 edges)
- **Output**: (5 edge predictions)

### Endpoints
- `GET /health` - Service health check
- `GET /model-info` - Model specifications
- `POST /predict` - Single prediction
- `POST /predict-batch` - Multi-step batch predictions (RL integration)
- `GET /metrics` - Service metrics

[Documentation](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/)  
[API Gateway OpenAPI Docs](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)  
[RL Inference OpenAPI Docs](https://traffic-inference-service.onrender.com/docs)  
[Repository](https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation)  
""",
    contact={
        "name": "Traffic Optimization Team",
        "url": "https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation",
        "email": "A00258304@student.tus.ie"
    }
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = "app/static/favicon.ico"
    return FileResponse(favicon_path, media_type="image/x-icon")


# Mount static files
# app.mount("/images", StaticFiles(directory="app/images"), name="images")
# templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Load model and scaler at startup
SCALER_PATH = 'trained_models/scaler.joblib'
WEIGHTS_PATH = 'trained_models/lstm_model.weights.h5'


# Define model architecture
def create_model():
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    from tensorflow.keras.models import Sequential
    return Sequential([
        LSTM(64, activation='relu', input_shape=(3, 5)),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(5)
    ])


try:
    model = create_model()
    model.load_weights(WEIGHTS_PATH)
    print(f"{Fore.GREEN}✓ Model loaded successfully")
except Exception as e:
    print(f"{Fore.RED}✗ Error loading model: {e}")
    model = None

try:
    import joblib
    scaler = joblib.load(SCALER_PATH)
    print(f"{Fore.GREEN}✓ Scaler loaded successfully")
except Exception as e:
    print(f"{Fore.RED}✗ Error loading scaler: {e}")
    scaler = None

# Metrics tracking
prediction_metrics = {
    "total_predictions": 0,
    "total_batch_predictions": 0,
    "avg_inference_time_ms": 0.0,
    "last_prediction_time": None,
    "inference_times": []  # Track last 100 for rolling average
}


class PredictionRequest(BaseModel):
    """
    Input: 3 hourly measurements for 5 edges
    Shape: (3, 5) - 3 timesteps, 5 edges
    """
    data: list[list[float]]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "data": [
                    [18.93, 10.13, 5.23, 4.14, 3.08],
                    [24.02, 11.01, 8.98, 5.42, 4.26],
                    [22.14, 9.34, 5.62, 4.57, 3.81]
                ]
            }
        }
    )


class PredictionResponse(BaseModel):
    """Predicted density for next hour (5 edges)"""
    prediction: list[float]
    edge_ids: list[str]
    timestamp: str = None
    inference_time_ms: float = None


class BatchPredictionRequest(BaseModel):
    """
    Batch prediction for multiple sequences.
    Each sequence is 3 timesteps x 5 edges.

    Use case: Get multi-step ahead forecasts for RL service.
    Example: 3 sequences -> 3 consecutive hourly predictions
    """
    sequences: list[list[list[float]]]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
                    ],
                    [
                        [22.14, 9.34, 5.62, 4.57, 3.81],
                        [20.50, 10.75, 6.10, 4.90, 3.50],
                        [21.75, 11.20, 6.85, 5.15, 3.95]
                    ]
                ]
            }
        }
    )


class BatchPredictionResponse(BaseModel):
    """Multiple predictions for batch request"""
    predictions: list[list[float]]
    edge_ids: list[str]
    timestamp: str = None
    inference_time_ms: float = None
    num_predictions: int = None


# Routes
@app.get("/health", tags=["System Health"], response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    if model is None or scaler is None:
        return {"status": "unhealthy", "message": "Model not loaded"}
    return {
        "status": "healthy",
        "message": "LSTM service is ready",
        "service": "lstm-predictor",
        "version": "1.0.0"
    }


@app.post("/predict", tags=["LSTM Predictor"], response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Predict traffic density for next hour

    Input: 3 hourly edge density measurements (raw values)
    Output: Predicted density for each edge at next hour

    **RL Service Integration**: Call this endpoint to get 1-hour ahead density predictions.
    """
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    start_time = time.time()

    try:
        # Convert to numpy array
        raw_data = np.array(request.data, dtype=np.float32)

        # Validate shape
        if raw_data.shape != (3, 5):
            raise ValueError(f"Expected shape (3, 5), got {raw_data.shape}")

        # Normalize
        normalized = scaler.transform(raw_data)

        # Reshape for LSTM (batch_size=1, timesteps=3, features=5)
        input_sequence = np.expand_dims(normalized, axis=0)

        # Predict
        prediction_normalized = model.predict(input_sequence, verbose=0)

        # Denormalize
        prediction_raw = scaler.inverse_transform(prediction_normalized)[0]

        # Edge IDs (from training data)
        edge_ids = ['-269002813', '-55825089', '617128762', '-617128762', '-312266114#2']

        # Calculate inference time
        inference_time = (time.time() - start_time) * 1000  # Convert to ms

        # Update metrics
        prediction_metrics["total_predictions"] += 1
        prediction_metrics["inference_times"].append(inference_time)

        # Keep only last 100 inference times for rolling average
        if len(prediction_metrics["inference_times"]) > 100:
            prediction_metrics["inference_times"].pop(0)

        prediction_metrics["avg_inference_time_ms"] = np.mean(prediction_metrics["inference_times"])
        prediction_metrics["last_prediction_time"] = datetime.now().isoformat()

        # Log prediction
        total = prediction_metrics['total_predictions']
        print(f"{Fore.GREEN}✓ Prediction #{total} generated in {inference_time:.2f}ms")
        print(f"{Fore.CYAN}  Predicted densities: {[f'{p:.2f}' for p in prediction_raw.tolist()]}")

        return PredictionResponse(
            prediction=prediction_raw.tolist(),
            edge_ids=edge_ids,
            timestamp=prediction_metrics["last_prediction_time"],
            inference_time_ms=inference_time
        )

    except ValueError as e:
        print(f"{Fore.RED}✗ Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"{Fore.RED}✗ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/predict-batch", tags=["LSTM Predictor"], response_model=BatchPredictionResponse)
def predict_batch(request: BatchPredictionRequest) -> BatchPredictionResponse:
    """
    Batch prediction for multiple sequences.

    Use case: Get multi-step ahead forecasts for RL service planning.

    Input: List of sequences, each with 3 timesteps x 5 edges
    Output: List of predictions, one per input sequence

    Example: Pass 3 consecutive sequences to get hours 4, 5, 6 predictions.

    **RL Service Integration**: Use this for lookahead planning and proactive signal timing.
    """
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    start_time = time.time()

    try:
        sequences = request.sequences

        # Validate number of sequences
        if not sequences or len(sequences) == 0:
            raise ValueError("At least 1 sequence required")

        if len(sequences) > 100:
            raise ValueError("Maximum 100 sequences per request")

        # Validate and normalize all sequences
        normalized_sequences = []
        for i, seq in enumerate(sequences):
            raw_seq = np.array(seq, dtype=np.float32)

            if raw_seq.shape != (3, 5):
                raise ValueError(f"Sequence {i}: expected shape (3, 5), got {raw_seq.shape}")

            normalized_seq = scaler.transform(raw_seq)
            normalized_sequences.append(normalized_seq)

        # Convert to batch array (N, 3, 5)
        batch_data = np.array(normalized_sequences, dtype=np.float32)

        # Predict all sequences in batch
        predictions_normalized = model.predict(batch_data, verbose=0)

        # Denormalize all predictions
        predictions_raw = scaler.inverse_transform(predictions_normalized)

        # Convert to list format
        predictions_list = predictions_raw.tolist()

        # Edge IDs (from training data)
        edge_ids = ['-269002813', '-55825089', '617128762', '-617128762', '-312266114#2']

        # Calculate inference time
        inference_time = (time.time() - start_time) * 1000  # Convert to ms

        # Update metrics
        prediction_metrics["total_batch_predictions"] += 1
        prediction_metrics["inference_times"].append(inference_time)

        # Keep only last 100 inference times for rolling average
        if len(prediction_metrics["inference_times"]) > 100:
            prediction_metrics["inference_times"].pop(0)

        prediction_metrics["avg_inference_time_ms"] = np.mean(prediction_metrics["inference_times"])
        prediction_metrics["last_prediction_time"] = datetime.now().isoformat()

        # Log batch prediction
        total = prediction_metrics['total_batch_predictions']
        n_seq = len(sequences)
        print(f"{Fore.GREEN}✓ Batch prediction #{total} ({n_seq} sequences) in {inference_time:.2f}ms")
        for idx, pred in enumerate(predictions_list):
            print(f"{Fore.CYAN}  Sequence {idx}: {[f'{p:.2f}' for p in pred]}")

        return BatchPredictionResponse(
            predictions=predictions_list,
            edge_ids=edge_ids,
            timestamp=prediction_metrics["last_prediction_time"],
            inference_time_ms=inference_time,
            num_predictions=len(sequences)
        )

    except ValueError as e:
        print(f"{Fore.RED}✗ Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"{Fore.RED}✗ Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/model-info", tags=["LSTM Predictor"], response_model=ModelInfoResponse)
def model_info():
    """Get model specifications"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    return {
        "model_type": "LSTM",
        "input_shape": (3, 5),
        "output_shape": (5,),
        "description": "Predicts edge density for next hour based on 3 hourly measurements",
        "edges": ['-269002813', '-55825089', '617128762', '-617128762', '-312266114#2'],
        "test_loss": 0.0698,
        "test_mae": 0.2084,
        "training_samples": 9,
        "test_samples": 2,
        "sequence_length": 3,
        "batch_prediction_supported": True,
        "max_batch_size": 100
    }


@app.get("/metrics", tags=["LSTM Predictor"], response_model=MetricsResponse)
def get_metrics():
    """
    Get service performance metrics

    Returns:
    - total_predictions: Number of single predictions served
    - total_batch_predictions: Number of batch predictions served
    - avg_inference_time_ms: Average inference latency (last 100 predictions)
    - last_prediction_time: Timestamp of last prediction
    - service_status: Health status
    """
    status = "healthy" if model and scaler else "unhealthy"

    return {
        "service": "lstm-predictor",
        "version": "1.0.0",
        "status": status,
        "total_predictions": prediction_metrics["total_predictions"],
        "total_batch_predictions": prediction_metrics["total_batch_predictions"],
        "avg_inference_time_ms": round(prediction_metrics["avg_inference_time_ms"], 2),
        "last_prediction_time": prediction_metrics["last_prediction_time"],
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url="/favicon.ico",  # matches the route above
    )


@app.get("/", response_class=HTMLResponse, tags=["Navigation"])
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
        request=request  # Explicitly passing it as a keyword argument as well
    )

if __name__ == "__main__":
    import uvicorn

    ssl_kwargs = {}
    if os.getenv("TLS_ENABLED", "false").lower() == "true":
        ssl_kwargs = {
            "ssl_certfile": os.getenv("TLS_CERT_FILE"),
            "ssl_keyfile": os.getenv("TLS_KEY_FILE"),
            "ssl_ca_certs": os.getenv("TLS_CA_FILE"),
        }

    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8001)),
        **ssl_kwargs,
    )
