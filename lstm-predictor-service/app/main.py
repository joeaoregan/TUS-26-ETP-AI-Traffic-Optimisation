# main.py
# FastAPI service for LSTM traffic prediction

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np
import os
from colorama import Fore, init

init(autoreset=True)

# Initialize FastAPI
app = FastAPI(
    title="LSTM Traffic Predictor",
    version="1.0.0",
    docs_url=None,   # <--- Disable the default route
    redoc_url=None,  # <--- Disable redoc too if you want
    description="""
<img src="images/logo.png" width="360" alt="LSTM Traffic Prediction Logo" />

## LSTM-Based Traffic Density Prediction

Real-time edge congestion forecasting using Long Short-Term Memory neural networks.

### Overview
Predicts traffic density for the next hour based on 3 hourly measurements from the 5 most congested edges.

### Key Features
- **LSTM Neural Network**: 64-unit LSTM with dropout regularization
- **Real-time Predictions**: Sub-100ms inference latency
- **Normalized Input**: MinMax scaling for stable predictions
- **Production Ready**: TensorFlow SavedModel format support

### Model Performance
- Test Loss (MSE): 0.0698
- Test MAE: 0.2084
- Input: (3 timesteps, 5 edges)
- Output: (5 edge predictions)

### Endpoints
- `GET /health` - Service health check
- `GET /model-info` - Model specifications
- `POST /predict` - Generate predictions

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
    favicon_path = "app/images/favicon.ico"
    return FileResponse(favicon_path, media_type="image/x-icon")
# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("app/images/logo.png", media_type="image/png")

# Mount static files
app.mount("/images", StaticFiles(directory="app/images"), name="images")

# Load model and scaler at startup
MODEL_PATH = 'app/trained_models/lstm_model.keras'
SCALER_PATH = 'app/trained_models/scaler.pkl'

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    scaler = pickle.load(open(SCALER_PATH, 'rb'))
    print(f"{Fore.GREEN}✓ Model and scaler loaded successfully")
except FileNotFoundError as e:
    print(f"{Fore.RED}✗ Error loading model: {e}")
    model = None
    scaler = None

from pydantic import ConfigDict

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

# Routes
@app.get("/health")
def health_check():
    """Health check endpoint"""
    if model is None or scaler is None:
        return {"status": "unhealthy", "message": "Model not loaded"}
    return {"status": "healthy", "message": "LSTM service is ready"}

@app.post("/predict")
def predict(request: PredictionRequest) -> PredictionResponse:
    """
    Predict traffic density for next hour
    
    Input: 3 hourly edge density measurements (raw values)
    Output: Predicted density for each edge at next hour
    """
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
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
        
        return PredictionResponse(
            prediction=prediction_raw.tolist(),
            edge_ids=edge_ids
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info")
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
        "test_mae": 0.2084
    }

# Custom OpenAPI schema with logo and server info
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="LSTM Traffic Predictor",
#         version="1.0.0",
#         description="High-performance traffic prediction service",
#         routes=app.routes,
#         servers=[
#             {"url": "http://localhost:8000", "description": "Development"},
#             {"url": "http://your-production-url", "description": "Production"}
#         ]
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://your-logo-url.png"
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi

from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_favicon_url="/favicon.ico",  # matches the route above
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)