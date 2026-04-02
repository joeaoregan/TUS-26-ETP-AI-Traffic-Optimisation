# Python FastAPI Service

📁 `rl-inference-service/`

## Core Application

🐍 `app/main.py` 

- [x] FastAPI application
- [x] Loads trained PPO models
- [x] POST `/predict_action` endpoint
- [x] GET `/health` and `/model_info` endpoints
- [x] Error handling and logging

## Configuration

📄 `requirements.txt` - Python dependencies

```python
fastapi==0.110.0
uvicorn==0.28.0
stable-baselines3==2.2.1
torch==2.2.1
numpy==1.26.4
pydantic==2.6.4
python-dotenv==1.0.1
shimmy==0.2.1
jinja2==3.1.3
aiofiles==24.1.0
```

## Deployment

📄 `Dockerfile` 

- [x] Python 3.9-slim container
- [x] Builds dependencies
- [x] Exposes port 8000
- [x] Runs with uvicorn

## Configuration Templates

📄 `.env.example` 

- [x] Environment variable template

## Data Directory

📁 `app/models/` 

- [x] Directory for trained models
- [x] (Models copied here by select_model.py)
- [x] `model.zip` - Trained PPO model