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

## 🔗 Quick Links

### 🌐 Live Services
- **[API Gateway](https://ai-traffic-control-api.onrender.com)** — REST API service
- **[Inference Service](https://traffic-inference-service.onrender.com)** — RL model inference

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
  <summary>🛠️ API Setup — Docker, Environment Variables, Components, Examples, Monitoring</summary>

- [🐳 Docker Compose Configuration](docs/api/setup/docker-compose.md)
- [🔐 Environment Variables](docs/api/setup/environment-variables.md)
- [🚗 Local Development Setup](docs/api/setup/local-development.md)
- [🌍 Production Deployment](docs/api/setup/production-deployment.md)
- [🧩 Components Overview](docs/api/guides/components.md)
- [📡 API Usage Examples](docs/api/guides/usage-examples.md)
- [📊 Monitoring and Logging](docs/api/guides/monitoring-logging.md)
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

This repository implements a **Cloud-Native Microservices Pipeline** designed for the Athlone "Orange Loop" case study.

- **[Traffic Monitoring Gateway](java-api-gateway/README.md) (Java/Spring Boot):** Manages secure telemetry ingestion and orchestrates service communication.
  - **JWT authentication:** Stateless token-based security with HS256 signing
  - **Exception handling:** Dedicated exception package for RL service communication errors
  - See [Java API Gateway README](java-api-gateway/README.md) for configuration and usage examples

- **[RL Inference Service](rl-inference-service/README.md) (Python/FastAPI):** Hosts a trained **MAPPO (Multi-Agent Proximal Policy Optimization)** model to predict optimal signal timings based on real-time traffic observations from 5 junctions

- **[LSTM Predictor Service](lstm-predictor-service/README.md) (Python/FastAPI):** Forecasts vehicle flow 15 minutes ahead using historical traffic patterns from SUMO simulations, targeting MAE < 10% accuracy

- **[Simulation Layer](SUMO/README.md) (SUMO):** Integrated high-fidelity traffic simulation environment for testing adaptive signal logic against baseline fixed-time controllers

This system is specifically modeled to address the saturation flow rates and signal-timing patterns of the Athlone 'Orange Loop' corridor, providing a scalable template for Smart City traffic management in regional Irish hubs.

---

# 🗂️ Project Structure

```
TUS-26-ETP-AI-Traffic-Optimisation/
├── java-api-gateway/                       # Java Spring Boot gateway (JWT Auth)
│   ├── src/
│   │   ├── main/java/com/example/gateway/
│   │   │   ├── GatewayApplication.java
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java
│   │   │   │   └── TrafficController.java
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java
│   │   │   │   ├── OpenApiConfig.java
│   │   │   │   └── WebConfig.java
│   │   │   ├── security/
│   │   │   │   ├── JwtService.java
│   │   │   │   └── JwtAuthenticationFilter.java
│   │   │   ├── exception/
│   │   │   │   └── RlInferenceException.java
│   │   │   ├── service/
│   │   │   │   └── RlInferenceClient.java
│   │   │   └── dto/
│   │   │       ├── LoginRequest.java
│   │   │       ├── LoginResponse.java
│   │   │       ├── TrafficActionRequest.java
│   │   │       ├── TrafficActionResponse.java
│   │   │       ├── TrafficSignalState.java
│   │   │       ├── ErrorResponse.java
│   │   │       └── HealthResponse.java
│   │   └── main/resources/
│   │       ├── application.yml
│   │       └── application-prod.yml
│   ├── pom.xml
│   ├── Dockerfile
│   └── README.md
├── rl-inference-service/                   # Python FastAPI RL inference service
│   ├── app/
│   │   ├── main.py
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── static/
│   ├── trained_models/
│   │   └── agent.th
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── lstm-predictor-service/                 # Python FastAPI LSTM forecasting service
│   ├── app/
│   │   ├── main.py
│   │   ├── data/
│   │   │   ├── loader.py
│   │   │   └── preprocessor.py
│   │   ├── models/
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── static/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
├── docs/                                   # MkDocs documentation (Material theme)
│   ├── index.md
│   ├── features.md
│   ├── CHANGELOG.md
│   ├── support.md
│   ├── quickstart.md
│   ├── api/                                # API documentation & setup
│   │   ├── index.md
│   │   ├── endpoints.md
│   │   ├── setup/
│   │   │   ├── index.md
│   │   │   ├── docker-compose.md
│   │   │   ├── environment-variables.md
│   │   │   ├── local-development.md
│   │   │   ├── production-deployment.md
│   │   │   ├── troubleshooting.md
│   │   │   └── using-different-models.md
│   │   └── guides/
│   │       ├── index.md
│   │       ├── usage-examples.md
│   │       ├── components.md
│   │       ├── monitoring-logging.md
│   │       └── performance-tuning.md
│   ├── api-gateway/
│   │   ├── index.md
│   │   ├── architecture.md
│   │   ├── key-features.md
│   │   ├── endpoints.md
│   │   └── file-structure.md
│   ├── inference-service/
│   │   ├── index.md
│   │   ├── architecture.md
│   │   ├── key-features.md
│   │   ├── endpoints.md
│   │   └── file-structure.md
│   ├── lstm/
│   │   ├── index.md
│   │   ├── architecture.md
│   │   ├── key-features.md
│   │   ├── endpoints.md
│   │   └── file-structure.md
│   ├── sumo/
│   │   ├── index.md
│   │   ├── architecture.md
│   │   ├── key-features.md
│   │   └── file-structure.md
│   ├── security/
│   │   └── java-api-gateway.md
│   ├── system-architecture/
│   │   ├── index.md
│   │   └── project-structure.md
│   ├── mkdocs.yml
│   └── images/
│       └── logo.png
├── SUMO/                                   # SUMO traffic simulation (Athlone network)
│   ├── osm.net.xml.gz
│   ├── osm.sumocfg
│   ├── town_routes.rou.xml
│   ├── tii_flows.xml
│   ├── tii_hourly_traffic.csv
│   ├── osm.view.xml
│   ├── osm_bbox.osm.xml.gz
│   ├── osm.netccfg
│   ├── run.bat
│   ├── Results/
│   │   ├── Base/
│   │   │   ├── edgeData.xml
│   │   │   ├── tripinfos.xml
│   │   │   └── stats.xml
│   │   └── MAPPO/
│   │       └── edgeData.xml
│   ├── Simulations/
│   │   └── Base/
│   └── README.md
├── docker-compose.yml
├── test_api.py
├── CHANGELOG.md
├── README.md
└── SUPPORT.md
```

---

<div align="center">

2026 • [Edgars Peskaitis](https://github.com/edgar183) • [Joe O'Regan](https://github.com/joeaoregan) • [David Claffey](https://github.com/dclaff) • [Adam O Neill Mc Knight](...)

</div>