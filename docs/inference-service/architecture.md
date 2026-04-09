# Architecture

## Technology Stack
- **Framework**: FastAPI 0.110.0 (async Python web framework)
- **Server**: Uvicorn 0.28.0 (ASGI server)
- **ML Framework**: PyTorch 2.2.1
- **Numerical Computing**: NumPy 1.26.4
- **Validation**: Pydantic 2.6.4
- **Templating**: Jinja2 3.1.3
- **Environment**: Python 3.9

## Deployment
- **Container**: Docker (Python 3.9-slim base)
- **Port**: 8000 (configurable via API_PORT)
- **Production URL**: https://traffic-inference-service.onrender.com
- **Local Development**: http://localhost:8000

## File Structure

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
