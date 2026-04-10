# File Structure (Python Inference Service)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
rl-inference-service/
├── app/
│   ├── main.py                              # FastAPI application (MAPPO model inference)
│   ├── templates/
│   │   └── index.html                       # Landing page with navigation links
│   └── static/
│       ├── logo.png                         # Project logo
│       └── favicon.ico                      # Browser tab icon
├── trained_models/
│   └── agent.th                             # Trained MAPPO model weights (PyTorch state_dict)
├── Dockerfile                               # Python 3.9-slim base, Uvicorn server
├── requirements.txt                         # FastAPI, Uvicorn, PyTorch, Numpy, Pydantic, Jinja2
├── .env.example                             # Template: MAPPO_AGENT_PATH, API_HOST, API_PORT
├── .gitignore
├── README.md                                # Setup and deployment guide
└── docker-compose.override.yml              # Local development overrides (optional)
```

---

## app/ Directory Structure

```
app/
├── main.py                                  # FastAPI instance, route handlers
│   ├── startup events (load model, initialize GRU states)
│   ├── POST /predict_action (junction_id, obs_data → action, confidence)
│   ├── POST /reset_hidden (reset all GRU hidden states)
│   ├── GET /health (service status, model_loaded)
│   ├── GET /model_info (model architecture, junctions, action masks)
│   ├── GET / (landing page)
│   └── GET /docs (Swagger UI)
├── templates/
│   └── index.html (static HTML with links)
└── static/
    └── assets (logo, favicon, etc.)
```

---

## Key Files

- **main.py** — All application logic in one file:
  - FastAPI app initialization
  - MAPPO RNNAgent loading from `MAPPO_AGENT_PATH`
  - Per-junction GRU hidden state management
  - 5 route handlers
  - Pydantic request/response models

- **trained_models/agent.th** — PyTorch model file (~1-2 MB)
  - Loaded at startup via `torch.load()`
  - Contains RNNAgent weights for all 5 junctions

- **Dockerfile** — Production image build
  - Base: `python:3.9-slim`
  - Installs requirements
  - Runs: `uvicorn main:app --host 0.0.0.0 --port $API_PORT`

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `MAPPO_AGENT_PATH` | `/app/trained_models/agent.th` | Path to model weights |
| `API_HOST` | `0.0.0.0` | Bind address |
| `API_PORT` | `8000` | Service port |
| `API_RELOAD` | `false` | Auto-reload on code changes |