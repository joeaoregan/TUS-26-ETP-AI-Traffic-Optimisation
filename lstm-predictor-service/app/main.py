# main.py
# FastAPI service for LSTM traffic prediction

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np
import os
from colorama import Fore, init

init(autoreset=True)

# Initialize FastAPI
app = FastAPI(title="LSTM Traffic Predictor", version="1.0.0")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)