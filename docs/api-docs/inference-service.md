# Python Inference Service

## Live Documentation

**[Inference Service Swagger UI](https://traffic-inference-service.onrender.com/docs)** (Production)

**Local:** http://localhost:8000/docs

---

## Detailed Endpoint Documentation

See **[Endpoints](../inference-service/endpoints.md)** for comprehensive specifications of:

- `POST /predict_action` — Predict optimal signal action for a junction
- `POST /reset_hidden` — Reset GRU hidden states (between simulation runs)
- `GET /health` — Service health check
- `GET /model_info` — Model architecture and junction metadata
- `GET /` — Landing page with navigation links
- `GET /docs` — Interactive Swagger UI

---

## Model Information

The inference service loads and manages a trained MAPPO (Multi-Agent Proximal Policy Optimization) model:

- **Architecture:** Shared RNNAgent with GRU recurrent layer
- **Input:** Observation vectors (up to 19 floats per junction)
- **Output:** Action logits for 2-4 possible signal phases per junction
- **Agents:** 5 agents (one per controlled junction)

See **[Key Features](../inference-service/key-features.md)** for neural network architecture details and supported junctions.

---

## Architecture & Features

- **[Architecture](../inference-service/architecture.md)** — Technology stack, deployment, file structure, integration points
- **[Key Features](../inference-service/key-features.md)** — Supported junctions, neural network architecture, observation format

---

## Swagger Auto-Generation

Documentation is automatically generated from Python type hints and docstrings:

- **FastAPI decorators** — `@app.get()`, `@app.post()`
- **Function docstrings** — Endpoint descriptions
- **Pydantic type hints** — Request/response schemas
- **Response models** — Expected HTTP structures
- **Tags** — Endpoint organization

This ensures documentation stays in sync with implementation.