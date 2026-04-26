# RL Inference Service

## Overview

The [RL Inference Service](https://traffic-inference-service.onrender.com/) is a FastAPI-based Python microservice that hosts a trained MAPPO (Multi-Agent Proximal Policy Optimization) neural network model for traffic signal prediction. It serves as the "AI brain" of the traffic optimization system, making real-time predictions about optimal traffic signal states for 5 junctions in the Athlone town network.

- [Render App](https://traffic-inference-service.onrender.com)
- [FastAPI Docs](https://traffic-inference-service.onrender.com/docs)

## Purpose

This service provides:

- **Real-time Traffic Signal Prediction**: Uses a trained MAPPO RL model to predict the next optimal green phase for any junction
- **Stateful Inference**: Maintains separate GRU hidden states per junction across multiple prediction calls
- **Multi-junction Support**: Handles 5 different junctions with varying numbers of valid actions (2-4 per junction)
- **Model Management**: Exposes endpoints to reset GRU hidden states between simulation runs
- **Health Monitoring**: Provides service health checks and model information endpoints
- **Auto-documented API**: Built with FastAPI for automatic OpenAPI/Swagger documentation

## Configuration

### Environment Variables

**Required:**

- `MAPPO_AGENT_PATH`: Path to trained model weights file (e.g., `/app/trained_models/agent.th`)

**Optional (with defaults):**

- `API_HOST`: Host to bind to (default: `0.0.0.0`)
- `API_PORT`: Port to listen on (default: `8000`)
- `API_RELOAD`: Enable auto-reload on code changes (default: `false`)

### Local Development Setup

1. Install dependencies:
``` bash
pip install -r requirements.txt
```

2. Set environment variables:
``` bash
export MAPPO_AGENT_PATH=/path/to/agent.th
```

3. Run the service:
``` bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4. Access:
- Swagger UI: <http://localhost:8000/docs>
- Landing page: <http://localhost:8000/>
- Health check: <http://localhost:8000/health>

### Docker Deployment

**Build:**
``` bash
docker build -t rl-inference-service:latest .
```

**Run (with model volume):**
``` bash
docker run -p 8000:8000 \
  -e MAPPO_AGENT_PATH=/app/trained_models/agent.th \
  -v /path/to/models:/app/trained_models \
  rl-inference-service:latest
```

**Run on Render:**

- Set `MAPPO_AGENT_PATH` environment variable in Render dashboard
- Container exposes port 8000
- Model file must be present in `/app/trained_models/` at runtime

## Model Training & Weights

### Training Source

The model was trained using EPyMARL (Epyc PyMARL) with the MAPPO algorithm:

- Framework: EPyMARL/SMAC
- Algorithm: MAPPO (Multi-Agent Proximal Policy Optimization)
- Configuration: mappo_sumo_v4.yaml
- Environment: SUMO traffic simulator with 5-junction Athlone town network

### Model File

- **Format**: PyTorch state dict (.th)
- **Size**: ~1-2 MB
- **Location**: `rl-inference-service/trained_models/agent.th`
- **Must be present** for service startup

### Loading Process

1. Service reads `MAPPO_AGENT_PATH` environment variable
2. Creates RNNAgent with correct input/hidden/output dimensions
3. Loads weights from file using `torch.load()`
4. Sets model to eval mode (disables dropout/batch norm)
5. Initializes GRU hidden states to zeros for all junctions

## Integration Points

### With API Gateway

This inference service is consumed by the Java API Gateway via REST calls at the configured `RL_INFERENCE_URL`:

!!! success "POST `/predict_action`"
    Accepts a junction ID and observation vector from the gateway.
    
    **Request**:
    ``` json
    {
      "junction_id": "joinedS_265580996_300839357",
      "obs_data": [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.12, 0.08, 0.33, 0.41, 0.22, 0.55, 0.18, 0.62, 0.70, 0.81, 0.50]
    }
    ```
    
    **Response (200)**:
    ``` json
    {
      "junction_id": "joinedS_265580996_300839357",
      "action": 2,
      "confidence": 0.92
    }
    ```

!!! note "GET `/health`"
    Health check endpoint for service availability monitoring.
    
    **Response (200)**:
    ``` json
    {
      "status": "healthy",
      "model_loaded": true,
      "junctions": [
        "joinedS_265580996_300839357",
        "300839359",
        "265580972",
        "1270712555",
        "8541180897"
      ]
    }
    ```

!!! success "POST `/reset_hidden`"
    Resets GRU hidden states for all junctions. **Call at the start of each simulation run.**
    
    **Response (200)**:
    ``` json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

**Gateway Configuration**:

- **Local Development**: `http://localhost:8000/predict_action`
- **Production (Cloud)**: Configured via `RL_INFERENCE_URL` environment variable
- **Timeouts**: 2 seconds (local) / 20 seconds (cloud)

### With SUMO Simulator

Training and validation use the SUMO (Simulation of Urban Mobility) traffic simulator:

- **Training Data Source**: SUMO generates observations from vehicle positions and lane queue lengths
- **Action Application**: Predicted actions are applied as signal phase changes in the simulation
- **Reward Calculation**: SUMO provides traffic metrics (wait times, throughput) for RL training
- **Validation**: Model performance tested on historical SUMO scenarios

### With LSTM Traffic Predictor

The LSTM Traffic Predictor service is now operational and can optionally provide traffic flow forecasts to enhance RL decision-making:

- **Status**: Service operational, predictions available via `/predict` endpoint
- **Forecast Horizon**: 1-hour ahead edge density predictions
- **Input**: 3 hourly edge density measurements for 5 most congested edges
- **Output**: Predicted density for each edge at next hour
- **Integration**: Not yet integrated with MAPPO model (planned for future)
- **Purpose**: Can provide context for signal timing decisions when integrated

## Performance Characteristics

### Prediction Latency
- **Average**: ~5-10ms per prediction
- **Bottleneck**: Matrix operations in GRU forward pass
- **Scaling**: Linear with observation size

### Memory Usage
- **Model weights**: ~1-2 MB
- **Runtime**: ~50-100 MB (PyTorch + app overhead)
- **Per-junction state**: ~1 KB per hidden state

### Throughput
- **Single-threaded**: ~100-150 predictions/second
- **Bottleneck**: Not throughput-limited; typically limited by upstream system

## Error Handling

| Error | Status | Response |
|-------|--------|----------|
| Unknown junction ID | 404 | `{"detail": "Unknown junction '...'. Known: [...]"}` |
| Observation too large | 400 | `{"detail": "obs_data has X values, expected <= 19"}` |
| Model not loaded | 503 | `{"detail": "Model not loaded"}` |
| Server error | 500 | FastAPI default error response |

## Logging

### Log Levels
- `INFO`: Startup messages, prediction details, state resets
- `WARNING`: Non-critical errors (e.g., health check failures)
- `ERROR`: Critical failures (model loading, prediction errors)

### Example Log Output
```
2026-04-01 10:30:45,123 - __main__ - INFO - MAPPO agent loaded from /app/trained_models/agent.th input=24 hidden=128 actions=4
2026-04-01 10:30:50,456 - __main__ - INFO - junction=300839359 agent_idx=1 action=0 confidence=0.923
2026-04-01 10:30:51,789 - __main__ - INFO - Hidden states reset for all junctions
```

## Development & Debugging

### Running Tests Locally
``` bash
pip install pytest pytest-asyncio httpx
pytest
```

### Debugging Model Predictions
``` bash
curl http://localhost:8000/model_info
```

### Resetting State Between Test Runs
``` bash
curl -X POST http://localhost:8000/reset_hidden
```

## Dependencies

### Core
- **fastapi** (0.110.0): Web framework
- **uvicorn** (0.28.0): ASGI server
- **torch** (2.2.1): Neural network inference
- **numpy** (1.26.4): Numerical operations

### Supporting
- **pydantic** (2.6.4): Request/response validation
- **python-dotenv** (1.0.1): Environment configuration
- **jinja2** (3.1.3): HTML templating
- **aiofiles** (24.1.0): Async file operations

## Quick Links

- **GitHub Repository**: <https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation>
- **API Swagger (Cloud)**: <https://traffic-inference-service.onrender.com/docs>
- **API Swagger (Local)**: <http://localhost:8000/docs>