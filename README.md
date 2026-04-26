# AI-Driven Predictive Traffic Flow Optimisation System

## Engineering Team Project | TUS Athlone

![TUS](https://img.shields.io/badge/TUS-2026-black?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iMTU3LjU1OTM2bW0iCiAgIGhlaWdodD0iMjA1LjE3MTE2bW0iCiAgIHZpZXdCb3g9IjAgMCAxNTcuNTU5MzYgMjA1LjE3MTE2IgogICB2ZXJzaW9uPSIxLjEiCiAgIGlkPSJzdmcxIgogICB4bWw6c3BhY2U9InByZXNlcnZlIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxzb2RpcG9kaTpuYW1lZHZpZXcKICAgICBpZD0ibmFtZWR2aWV3MSIKICAgICBwYWdlY29sb3I9IiNmZmZmZmYiCiAgICAgYm9yZGVyY29sb3I9IiMwMDAwMDAiCiAgICAgYm9yZGVyb3BhY2l0eT0iMC4yNSIKICAgICBpbmtzY2FwZTpzaG93cGFnZXNoYWRvdz0iMiIKICAgICBpbmtzY2FwZTpwYWdlb3BhY2l0eT0iMC4wIgogICAgIGlua3NjYXBlOnBhZ2VjaGVja2VyYm9hcmQ9IjAiCiAgICAgaW5rc2NhcGU6ZGVza2NvbG9yPSIjZDFkMWQxIgogICAgIGlua3NjYXBlOmRvY3VtZW50LXVuaXRzPSJtbSI+PGlua3NjYXBlOnBhZ2UKICAgICAgIHg9IjAiCiAgICAgICB5PSIwIgogICAgICAgd2lkdGg9IjE1Ny41NTkzNiIKICAgICAgIGhlaWdodD0iMjA1LjE3MTE2IgogICAgICAgaWQ9InBhZ2UyIgogICAgICAgbWFyZ2luPSIwIgogICAgICAgYmxlZWQ9IjAiIC8+PC9zb2RpcG9kaTpuYW1lZHZpZXc+PGRlZnMKICAgICBpZD0iZGVmczEiPjxzdHlsZQogICAgICAgaWQ9InN0eWxlMSI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48c3R5bGUKICAgICAgIGlkPSJzdHlsZTEtNCI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48L2RlZnM+PGcKICAgICBpbmtzY2FwZTpsYWJlbD0iTGF5ZXIgMSIKICAgICBpbmtzY2FwZTpncm91cG1vZGU9ImxheWVyIgogICAgIGlkPSJsYXllcjEiCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjA4LjE2MDkzLDQ4Ljg3NTE2MikiPjxnCiAgICAgICBpZD0iQXJ0d29yayIKICAgICAgIHRyYW5zZm9ybT0ibWF0cml4KDAuMjY0NTgzMzMsMCwwLDAuMjY0NTgzMzMsLTIwOC4xNjA5NCwtNDguODc1MTU4KSI+PHBhdGgKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICBkPSJNIDU5NS40OCwwIEggNDc2LjM4IFYgNTguNTIgSCAzNTcuMyBWIDAgSCAyMzguMiBWIDU4LjUyIEggMTE5LjEgViAwIEggMCB2IDM1Ny4yOSBoIDExOS4xIGEgMTc4LjY0LDE3OC42NCAwIDEgMSAzNTcuMjgsMCBoIDExOS4wNiB6IgogICAgICAgICBpZD0icGF0aDEiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSI0NzYuMzgiCiAgICAgICAgIHk9IjcxNS45MDAwMiIKICAgICAgICAgd2lkdGg9IjExOS4xIgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3QxIiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNzE1LjkwMDAyIgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDIiCiAgICAgICAgIHg9IjAiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB5PSI1OTYuNzk5OTkiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSI1OS41NDk5OTkiCiAgICAgICAgIGlkPSJyZWN0MyIKICAgICAgICAgeD0iMCIgLz48cmVjdAogICAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICAgIHg9IjQ3Ni4zOTk5OSIKICAgICAgICAgeT0iNTk2Ljc5OTk5IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDQiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSIxMTkuMSIKICAgICAgICAgeT0iNTM3LjI1IgogICAgICAgICB3aWR0aD0iMzU3LjI5OTk5IgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3Q1IiAvPjxwb2x5Z29uCiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgcG9pbnRzPSI0NzYuMzksNjU2LjM1IDExOS4xLDY1Ni4zNSAxMTkuMSw3MTUuOSAyMzguMiw3MTUuOSAyMzguMiw3NzUuNDUgMzU3LjI5LDc3NS40NSAzNTcuMjksNzE1LjkgNDc2LjM5LDcxNS45ICIKICAgICAgICAgaWQ9InBvbHlnb241IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeD0iNDc2LjM5OTk5IgogICAgICAgICB5PSI0MTguMTYiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSIxMTkuMSIKICAgICAgICAgaWQ9InJlY3Q2IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNDE4LjE2IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iMTE5LjEiCiAgICAgICAgIGlkPSJyZWN0NyIKICAgICAgICAgeD0iMCIgLz48L2c+PC9nPjwvc3ZnPgo=)
![Module](https://img.shields.io/badge/Module-Engineering%20Team%20Project-blue?style=flat-square)
![Topic](https://img.shields.io/badge/Topic-AI%20Traffic%20Optimisation-yellow?style=flat-square)

![Java 17](https://img.shields.io/badge/Java-17-blue)
![Python 3.9](https://img.shields.io/badge/Python-3.9-green)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.2.3-6DB33F?logo=spring-boot&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active_Research-success)

![GitHub repo size](https://img.shields.io/github/repo-size/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?color=blue)
![GitHub top language](https://img.shields.io/github/languages/top/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation)
![Stars](https://img.shields.io/github/stars/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation?style=social)

> **Project Goal:** Target 15-20% reduction in urban traffic congestion for the Athlone "Orange Loop" using Reinforcement Learning, measured by:
> - **Average Travel Time (ATT):** -15%
> - **Mean Queue Length (MQL):** -20%
> - **Data Integrity:** TLS 1.3 secured telemetry pipeline

---

## 🔗 Quick Links

### 🌐 Live Services
- [**API Gateway**](https://ai-traffic-control-api.onrender.com) — REST API service on Render
- [**Inference Service**](https://traffic-inference-service.onrender.com) — RL model inference on Render
- [**LSTM Predictor Service**](https://lstm-predictor-service.onrender.com/) - LSTM Predictor Service on Render

### 📖 API Documentation (Swagger)
- **[API Gateway Swagger](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)** — Interactive API docs
- **[Inference Service Swagger](https://traffic-inference-service.onrender.com/docs)** — Interactive API docs

### 📚 Documentation
- **[System Architecture](docs/system-architecture/index.md)** — Detailed system design
- **[API Endpoints](docs/api/endpoints.md)** — Quick reference and full API specifications
- **[Quick Start Guide](docs/quickstart.md)** — Get up and running quickly
- **[Full Documentation](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/)** — Complete mkdocs site
- **[Gateway JWT Authentication Guide](docs/security/java-api-gateway.md)** — JWT configuration and usage

<details>
  <summary>🚀Running the System</summary>

You can start all three microservices (API Gateway, RL Inference, and LSTM Predictor) using the provided startup scripts:

#### Windows:

```bash
start.bat
```

#### Linux/macOS:

```bash
./start.sh
```

</details>
<details>
  <summary>🛠️ API Setup — Docker, Environment Variables, Components, Examples, Monitoring</summary>

- [🐳 Docker Compose Configuration](docs/api/setup/docker-compose-configuration.md)
- [🔐 Environment Variables](docs/api/setup/environment-variables.md)
- [🚗 Local Development Setup](docs/api/setup/local-dev.md)
- [🌍 Production Deployment](docs/api/setup/production-deployment.md)
- [🧩 Components Overview](docs/api/guides/components.md)
- [📡 API Usage Examples](docs/api/guides/usage-examples.md)
- [📊 Monitoring and Logging](docs/api/guides/monitoring-and-logging.md)
- [⚡ Performance Tuning](docs/api/guides/performance-tuning.md)
- [🔄 Using Different Models](docs/api/setup/using-different-models.md)
- [🐛 Troubleshooting](docs/api/setup/troubleshooting.md)

</details>

<details>
  <summary>📖 API Reference — Quick Reference & Detailed Specifications</summary>

- [📡 API Endpoints (Quick Reference)](docs/api/endpoints.md)
- [Java API Gateway Endpoints](docs/api-gateway/endpoints.md)
- [🤖 Python Inference Service Endpoints](docs/inference-service/endpoints.md)
- [🧠 LSTM Predictor Endpoints](docs/lstm/endpoints.md)
    
</details>
<details>
  <summary>💬 Support — Contact, Contributing, Issues</summary>

- [👥 Contact](docs/support.md#contact)
- [🤝 Contributing](docs/support.md#contributing)
- [⚠️ Issues](docs/support.md#issues)

</details>

---

## 🏗️ System Architecture

```text
           ┌─────────────────────────────────┐
           │          CLIENT LAYER           │
           │   Web • Mobile • External API   │
           └────────────────┬────────────────┘
                            │
                            │ HTTPS (TLS 1.3)
                            │
         ┌──────────────────▼──────────────────┐
         │   JAVA API GATEWAY (Port 8080)      │
         │        Spring Boot 3.2.3            │
         ├─────────────────────────────────────┤
         │  • JWT Authentication (HS256)       │
         │  • Request Validation               │
         │  • Fallback Logic (RED signal)      │
         │  • Circuit Breaker Pattern          │
         └──────────────────┬──────────────────┘
                            │
                ┌───────────┴─────────────┐
                │                         │
    ┌───────────▼────────┐   ┌────────────▼──────────┐
    │  HEALTH CHECK      │   │  PREDICTION REQUESTS  │
    │  /health           │   │  /traffic/action      │
    └────────────────────┘   └┬──────────────────────┘
                              │
                  ┌───────────▼───────────┐
                  │ INFERENCE SERVICE     │
                  │  (Port 8000)          │
                  │  Python/FastAPI       │
                  ├───────────────────────┤
                  │ • MAPPO RL Model      │
                  │ • 5-Junction Support  │
                  │ • GRU State Mgmt      │
                  │ • Action Masking      │
                  └───────────┬───────────┘
                              │
                ┌─────────────┴───────────┐
                │                         │
    ┌───────────▼─────────┐   ┌───────────▼───────────┐
    │  LSTM PREDICTOR     │   │  ACTION SELECTION     │
    │  (Port 8001)        │   │  (MAPPO Output)       │
    │  Python/FastAPI     │   │                       │
    ├─────────────────────┤   │ Actions:              │
    │ • Time-series LSTM  │   │ 0: RED                │
    │ • 15-min Forecast   │   │ 1: YELLOW             │
    │ • MAE < 10%         │   │ 2: GREEN              │
    │ • Data Pipeline     │   │ 3: GREEN_EXTENDED     │
    └─────────────────────┘   └───────────┬───────────┘
                                          │
                                          │ Signal State
                                          │
                              ┌───────────▼───────────┐
                              │  RESPONSE TO CLIENT   │
                              │ {                     │
                              │   action: 0-3,        │
                              │   signalState: "RED", │
                              │   confidence: 0.87    │
                              │ }                     │
                              └───────────────────────┘
```

This repository implements a **Cloud-Native Microservices Pipeline** designed for the Athlone "Orange Loop" case study.

- **[Traffic Monitoring Gateway](java-api-gateway/README.md) (Java/Spring Boot):** Manages secure telemetry ingestion and orchestrates service communication.
  - **JWT authentication:** Stateless token-based security with HS256 signing
  - **Exception handling:** Dedicated exception package for RL service communication errors
  - See [Java API Gateway README](java-api-gateway/README.md) for configuration and usage examples

- **[RL Inference Service](rl-inference-service/README.md) (Python/FastAPI):** Hosts a trained **MAPPO (Multi-Agent Proximal Policy Optimization)** model to predict optimal signal timings based on real-time traffic observations from 5 junctions

- **[LSTM Predictor Service](lstm-predictor-service/README.md) (Python/FastAPI):** Forecasts vehicle flow 15 minutes ahead using historical traffic patterns from SUMO simulations, targeting MAE < 10% accuracy

- **[Simulation Layer](SUMO/README.md) (SUMO):** Integrated high-fidelity traffic simulation environment for testing adaptive signal logic against baseline fixed-time controllers

This system is specifically modeled to address the saturation flow rates and signal-timing patterns of the Athlone 'Orange Loop' corridor, providing a scalable template for Smart City traffic management in regional Irish hubs.

Two FastAPI microservices:

**RL Inference Service** (Port 8000)
- MAPPO agent for signal prediction
- [Full docs](./rl-inference-service/README.md)

**LSTM Predictor Service** (Port 8001)
- LSTM for traffic density forecasting
- [Full docs](./lstm-predictor-service/README.md)

## 🚀 Quick Start

Start both services in separate terminals:

```bash
cd rl-inference-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

```bash
cd lstm-predictor-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Test integration:

```bash
python lstm-predictor-service/test_rl_integration.py
```

---

## 🗂️ Project Structure

```
TUS-26-ETP-AI-Traffic-Optimisation/
├── java-api-gateway/          # Spring Boot Edge Service (JWT Auth, LSTM/RL Orchestration)
├── rl-inference-service/      # Python FastAPI (MAPPO Multi-Agent RL Inference)
├── lstm-predictor-service/    # Python FastAPI (Time-Series Traffic Density Forecasting)
├── SUMO/                      # Traffic Simulation (Athlone 'Orange Loop' Network & Results)
├── docs/                      # Central Documentation (MkDocs source & guides)
├── docker-compose.yml         # Container orchestration for all services
├── start.bat / start.sh       # Multi-platform quickstart scripts
└── README.md                  # This file
```

For a detailed breakdown of every file, please refer to our detailed [Project Structure](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/system-architecture/project-structure/) documentation.

---

<div align="center">

2026 • [Edgars Peskaitis](https://github.com/edgar183) • [Joe O'Regan](https://github.com/joeaoregan) • [David Claffey](https://github.com/dclaff) • [Adam O Neill Mc Knight](https://github.com/AdamQ45)

</div>