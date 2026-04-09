# RL Inference Service

## Overview

The **RL Inference Service** is a FastAPI-based Python microservice that hosts a trained MAPPO (Multi-Agent Proximal Policy Optimization) neural network model for traffic signal prediction. It serves as the "AI brain" of the traffic optimization system, making real-time predictions about optimal traffic signal states for 5 junctions in the Athlone town network.

## Purpose

This service provides:
- **Real-time Traffic Signal Prediction**: Uses a trained MAPPO RL model to predict the next optimal green phase for any junction
- **Stateful Inference**: Maintains separate GRU hidden states per junction across multiple prediction calls
- **Multi-junction Support**: Handles 5 different junctions with varying numbers of valid actions (2-4 per junction)
- **Model Management**: Exposes endpoints to reset GRU hidden states between simulation runs
- **Health Monitoring**: Provides service health checks and model information endpoints
- **Auto-documented API**: Built with FastAPI for automatic OpenAPI/Swagger documentation

## Key Features

### Supported Junctions

The service manages these 5 junctions with the following action spaces:

1. **joinedS_265580996_300839357** - 4 valid phases (0, 1, 2, 3)
2. **300839359** - 2 valid phases (0, 1)
3. **265580972** - 2 valid phases (0, 1)
4. **1270712555** - 2 valid phases (0, 1)
5. **8541180897** - 2 valid phases (0, 1)

### Neural Network Architecture

The model uses a shared RNNAgent with the following structure:

- **Input Layer**: Concatenates observations + agent ID one-hot encoding
  - Observation vector: up to 19 floats (zero-padded to this size)
  - Agent ID one-hot: 5 floats (one per junction)
  - Total input: 24 floats

- **Hidden Layer**: GRUCell
  - Dimension: 128
  - Maintains stateful hidden state per junction across calls

- **Output Layer**: Fully connected
  - Outputs logits for all possible actions (4 max)
  - Masked by junction-specific action availability

- **Activation**: ReLU on first layer, softmax on output

### Observation Format

Each observation contains traffic state information including:
- Phase encoding (one-hot representation of current signal phase)
- Minimum green flag (whether minimum green time has elapsed)
- Lane queue lengths for approach lanes
- Vehicle wait times
- Gap detection values

Example observation sizes:
- joinedS junction: 19 floats (full-featured)
- Other junctions: ~8-10 floats (zero-padded to 19 internally)

## Architecture

### Technology Stack
- **Framework**: FastAPI 0.110.0 (async Python web framework)
- **Server**: Uvicorn 0.28.0 (ASGI server)
- **ML Framework**: PyTorch 2.2.1
- **Numerical Computing**: NumPy 1.26.4
- **Validation**: Pydantic 2.6.4
- **Templating**: Jinja2 3.1.3
- **Environment**: Python 3.9

### Deployment
- **Container**: Docker (Python 3.9-slim base)
- **Port**: 8000 (configurable via API_PORT)
- **Production URL**: https://traffic-inference-service.onrender.com
- **Local Development**: http://localhost:8000

### File Structure

```
rl-inference-service/
├── app/
│   ├── main.py                 # FastAPI application & inference logic
│   ├── templates/
│   │   └── index.html          # Landing page
│   └── static/                 # Static assets (logo, favicon)
├── trained_models/
│   └── agent.th                # Trained MAPPO model weights
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## API Endpoints

### Traffic Inference

!!! success "POST `/predict_action`"
    Predict the next optimal green phase for a specific junction.

    **Request Body:**
    ``` json
    {
      "junction_id": "300839359",
      "obs_data": [0.0, 1.0, 1.0, 0.12, 0.33, 0.41, 0.22, 0.55]
    }
    ```

    **Response (200):**
    ``` json
    {
      "junction_id": "300839359",
      "action": 1,
      "confidence": 0.87
    }
    ```

    **Parameters:**  

    - `junction_id` (string, required): One of the 5 known junction IDs  
    - `obs_data` (array of floats, required): Local observation vector  
      - Smaller observations are automatically zero-padded to 19 floats  
      - Maximum size: 19 floats  

    **Errors:**  

    - `404`: Unknown junction ID  
    - `400`: Observation size exceeds 19 floats  
    - `503`: Model not loaded  

    **Hidden State Management:**  

    - Each call updates and persists the GRU hidden state for that junction  
    - Call `POST /reset_hidden` at the start of each new simulation run  

!!! success "POST `/reset_hidden`"
    Reset GRU hidden states for all junctions. **Call at the start of each new simulation run.**

    **Request Body:** (empty)

    **Response (200):**
    ``` json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

### System Health & Information
!!! note "GET `/health`"
    Service health check.

    **Response (200):**    
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

    **Status Values:**

    - `healthy`: Model loaded and ready  
    - `no_model`: Service running but model not loaded  
    - `unhealthy`: Service error  

!!! note "GET `/model_info`"
    Get detailed information about the loaded MAPPO model.

    **Response (200):**
    ``` json
    {
      "architecture": "RNNAgent (GRU)",
      "input_shape": 24,
      "hidden_dim": 128,
      "n_actions": 4,
      "n_agents": 5,
      "obs_agent_id": true,
      "junctions": {
        "joinedS_265580996_300839357": {
          "agent_index": 0,
          "avail_actions": [1, 1, 1, 1],
          "valid_actions": 4
        },
        "300839359": {
          "agent_index": 1,
          "avail_actions": [1, 1, 0, 0],
          "valid_actions": 2
        }
      }
    }
    ```

### Navigation

!!! note "GET `/`"
    HTML landing page with links to documentation, status checks, and the API Gateway.

    **Response**: HTML page with navigation links

!!! note "GET `/docs`"
  FastAPI Swagger UI (auto-generated from OpenAPI schema).

  **Response**: Interactive API documentation

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
- Swagger UI: http://localhost:8000/docs
- Landing page: http://localhost:8000/
- Health check: http://localhost:8000/health

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

The API Gateway (Java Spring Boot) communicates with this service via REST:

**From Gateway Request:**
``` json
{
  "junction_id": "joinedS_265580996_300839357",
  "obs_data": [0.0, 1.0, 0.0, ...]
}
```

**To Gateway Response:**
``` json
{
  "junctionId": "joinedS_265580996_300839357",
  "predictedAction": 2,
  "signalState": "GREEN",
  "timestamp": 1710000000000,
  "status": "success"
}
```

**Gateway Timeout**: 2 seconds (local) / 20 seconds (cloud)

### With SUMO Simulator

Training and simulation use the SUMO (Simulation of Urban Mobility) traffic simulator:
- Provides real-world traffic scenarios
- Calculates observations from vehicle positions and lane queues
- Applies predicted actions as signal phase changes
- Measures reward signals for RL training

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

- **GitHub Repository**: https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation
- **API Swagger (Cloud)**: https://traffic-inference-service.onrender.com/docs
- **API Swagger (Local)**: http://localhost:8000/docs