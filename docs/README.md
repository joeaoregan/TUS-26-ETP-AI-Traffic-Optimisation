# AI-Driven Predictive Traffic Flow Optimisation System

## Engineering Team Project | TUS Athlone

![TUS](https://img.shields.io/badge/TUS-2026-black?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iMTU3LjU1OTM2bW0iCiAgIGhlaWdodD0iMjA1LjE3MTE2bW0iCiAgIHZpZXdCb3g9IjAgMCAxNTcuNTU5MzYgMjA1LjE3MTE2IgogICB2ZXJzaW9uPSIxLjEiCiAgIGlkPSJzdmcxIgogICB4bWw6c3BhY2U9InByZXNlcnZlIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxzb2RpcG9kaTpuYW1lZHZpZXcKICAgICBpZD0ibmFtZWR2aWV3MSIKICAgICBwYWdlY29sb3I9IiNmZmZmZmYiCiAgICAgYm9yZGVyY29sb3I9IiMwMDAwMDAiCiAgICAgYm9yZGVyb3BhY2l0eT0iMC4yNSIKICAgICBpbmtzY2FwZTpzaG93cGFnZXNoYWRvdz0iMiIKICAgICBpbmtzY2FwZTpwYWdlb3BhY2l0eT0iMC4wIgogICAgIGlua3NjYXBlOnBhZ2VjaGVja2VyYm9hcmQ9IjAiCiAgICAgaW5rc2NhcGU6ZGVza2NvbG9yPSIjZDFkMWQxIgogICAgIGlua3NjYXBlOmRvY3VtZW50LXVuaXRzPSJtbSI+PGlua3NjYXBlOnBhZ2UKICAgICAgIHg9IjAiCiAgICAgICB5PSIwIgogICAgICAgd2lkdGg9IjE1Ny41NTkzNiIKICAgICAgIGhlaWdodD0iMjA1LjE3MTE2IgogICAgICAgaWQ9InBhZ2UyIgogICAgICAgbWFyZ2luPSIwIgogICAgICAgYmxlZWQ9IjAiIC8+PC9zb2RpcG9kaTpuYW1lZHZpZXc+PGRlZnMKICAgICBpZD0iZGVmczEiPjxzdHlsZQogICAgICAgaWQ9InN0eWxlMSI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48c3R5bGUKICAgICAgIGlkPSJzdHlsZTEtNCI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48L2RlZnM+PGcKICAgICBpbmtzY2FwZTpsYWJlbD0iTGF5ZXIgMSIKICAgICBpbmtzY2FwZTpncm91cG1vZGU9ImxheWVyIgogICAgIGlkPSJsYXllcjEiCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjA4LjE2MDkzLDQ4Ljg3NTE2MikiPjxnCiAgICAgICBpZD0iQXJ0d29yayIKICAgICAgIHRyYW5zZm9ybT0ibWF0cml4KDAuMjY0NTgzMzMsMCwwLDAuMjY0NTgzMzMsLTIwOC4xNjA5NCwtNDguODc1MTU4KSI+PHBhdGgKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICBkPSJNIDU5NS40OCwwIEggNDc2LjM4IFYgNTguNTIgSCAzNTcuMyBWIDAgSCAyMzguMiBWIDU4LjUyIEggMTE5LjEgViAwIEggMCB2IDM1Ny4yOSBoIDExOS4xIGEgMTc4LjY0LDE3OC42NCAwIDEgMSAzNTcuMjgsMCBoIDExOS4wNiB6IgogICAgICAgICBpZD0icGF0aDEiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSI0NzYuMzgiCiAgICAgICAgIHk9IjcxNS45MDAwMiIKICAgICAgICAgd2lkdGg9IjExOS4xIgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3QxIiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNzE1LjkwMDAyIgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDIiCiAgICAgICAgIHg9IjAiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB5PSI1OTYuNzk5OTkiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSI1OS41NDk5OTkiCiAgICAgICAgIGlkPSJyZWN0MyIKICAgICAgICAgeD0iMCIgLz48cmVjdAogICAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICAgIHg9IjQ3Ni4zOTk5OSIKICAgICAgICAgeT0iNTk2Ljc5OTk5IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDQiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSIxMTkuMSIKICAgICAgICAgeT0iNTM3LjI1IgogICAgICAgICB3aWR0aD0iMzU3LjI5OTk5IgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3Q1IiAvPjxwb2x5Z29uCiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgcG9pbnRzPSI0NzYuMzksNjU2LjM1IDExOS4xLDY1Ni4zNSAxMTkuMSw3MTUuOSAyMzguMiw3MTUuOSAyMzguMiw3NzUuNDUgMzU3LjI5LDc3NS40NSAzNTcuMjksNzE1LjkgNDc2LjM5LDcxNS45ICIKICAgICAgICAgaWQ9InBvbHlnb241IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeD0iNDc2LjM5OTk5IgogICAgICAgICB5PSI0MTguMTYiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSIxMTkuMSIKICAgICAgICAgaWQ9InJlY3Q2IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNDE4LjE2IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iMTE5LjEiCiAgICAgICAgIGlkPSJyZWN0NyIKICAgICAgICAgeD0iMCIgLz48L2c+PC9nPjwvc3ZnPgo=)
![Module](https://img.shields.io/badge/Module-Engineering%20Team%20Project-blue?style=flat-square)
![AI Traffic Optimisation](https://img.shields.io/badge/Topic-AI%20Traffic%20Optimisation-blue?style=flat-square)

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

### 🔗 Quick Links

#### 📚 Documentation
- **[System Architecture](SYSTEM_ARCHITECTURE.md)** — Detailed system design
- **[Quick Start Guide](QUICKSTART.md)** — Get up and running quickly
- **[Full Documentation](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/)** — Complete mkdocs site

<details>
  <summary>🛠️ API Setup</summary>

   [🧩 Components]()  
   [🚗 API Setup Guide](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/api-setup-guide/#option-1-using-docker-compose-recommended)  
   [📡 API Usage Examples](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/api-usage-examples/#get-traffic-action-demo-random-junction)  
   [🔐 Environment Variables](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/environment-variables/)  
   [🐳 Docker Compose Configuration](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/docker-compose-configuration/)  
   [📊 Monitoring and Logging](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/monitoring-and-logging/)  
   [🔄 Using Different Models](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/using-different-models/)  
   [⚡ Performance Tuning](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/performance-tuning/)  
   [🐛 Troubleshooting](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/troubleshooting/)  
   [🌍 Production Deployment](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-setup/production-deployment/)  

</details>

<details>
  <summary>💬 Support</summary>

- [👥 Contact](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/support/#contact)
- [🤝 Contributing](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/support/#contributing)
- [⚠️ Issues](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/support/#issues)
    
</details>
<details>
  <summary>📖 API Documentation</summary>

- [API Documentation](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-docs/)
- [Java API Gateway](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-docs/api-gateway/)
- [Python Inference Service](https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/api-docs/inference-service/)
    
</details>

#### 🌐 Live Services
- **[API Gateway](https://ai-traffic-control-api.onrender.com)** — REST API service
- **[Inference Service](https://traffic-inference-service.onrender.com)** — RL model inference

#### 📖 API Documentation (Swagger)
- **[API Gateway Swagger](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)** — Interactive API docs
- **[Inference Service Swagger](https://traffic-inference-service.onrender.com/docs)** — Interactive API docs

---

## 🏗️ System Architecture

This repository implements a **Cloud-Native Microservices Pipeline** designed for the Athlone "Orange Loop" case study. 

- **[Traffic Monitoring Gateway](java-api-gateway/README.md) (Java/Spring Boot):** Manages secure telemetry ingestion and orchestrates service communication.
  - **JWT authentication & role-based access control:** available in [A00163691-JWTAuth](../../tree/A00163691-JWTAuth) branch for production deployments.
- **[LSTM Predictor Service](lstm-predictor-service/README.md) (Python/FastAPI):** Forecasts vehicle flow 15 minutes ahead using historical traffic patterns, achieving MAE < 10% accuracy to provide high-fidelity state information for the RL agent.
- **[RL-Inference Service](rl-inference-service/README.md) (Python/FastAPI):** Hosts a trained **PPO (Proximal Policy Optimization)** model to predict optimal signal timings based on real-time traffic density.
- **[Simulation Layer](SUMO\Simulations\Base\README.md) (SUMO):** Integrated high-fidelity environment for testing adaptive signal logic against baseline fixed-time controllers.


This system is specifically modeled to address the saturation flow rates and signal-timing patterns of the Athlone 'Orange Loop' corridor, providing a scalable template for Smart City traffic management in regional Irish hubs.

---

# AI Traffic Control API Setup Guide

This project provides a complete REST API solution for traffic signal control using trained RL models.

## Project Structure

```
TUS-26-ETP2-Python-Data-Science-and-ML-Pipeline/
├── java-api-gateway/                       # Java Spring Boot gateway
│   ├── src/
│   │   ├── main/java/com/example/gateway/
│   │   │   ├── GatewayApplication.java     # Spring Boot app
│   │   │   ├── controller/
│   │   │   │   └── TrafficController.java  # REST endpoints
│   │   │   └── service/
│   │   │       └── RlInferenceClient.java  # RL service client
│   │   └── main/resources/
│   │       └── application.properties      # Spring config
│   ├── pom.xml                             # Maven configuration
│   └── Dockerfile                          # Java service Docker image
├── rl-inference-service/                   # Python FastAPI service
│   ├── app/
│   │   ├── main.py                         # FastAPI application
│   │   └── models/                         # Directory for trained models
│   ├── Dockerfile                          # Python service Docker image
│   ├── requirements.txt                    # Python dependencies
│   └── .env.example                        # Environment variables template
├── SUMO/                                   # 
│   ├── results/
│   │   ├── Base/
│   ├── Simulations/
│   │   ├── Base/
├── docker-compose.yml                      # Docker Compose orchestration
└── CHANGELOG.md                            # Change log
└── FILE_MAINFEST.md                        # 
└── QUICKSTART.md                           # Quick start guide
└── README.md                               # This file
└── SETUP_COMPLETE.md                       # 
└── SYSTEM_ARCHITECTURE.md                  # 
```

---

<div align="center">

2026 &bull; [Edgars Peskaitis](https://github.com/edgar183) &bull; [Joe O'Regan](https://github.com/joeaoregan) &bull; [David Claffey](https://github.com/dclaff) &bull; [Adam O Neill Mc Knight](https://github.com/AdamQ45)

</div>