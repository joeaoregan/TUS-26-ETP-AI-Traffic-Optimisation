# AI Traffic Optimisation System

![Logo](images/logo.png)

AI-Driven Predictive Traffic Flow Optimisation System

- [Features](features.md)
- [System Architecture](system-architecture/index.md)
- [Quick Start](quickstart.md)
- [Setup Complete](setup-complete/index.md)
- [File Manifest](file-manifest/index.md)
- [API Docs](api/index.md)
- [API Endpoints](api/endpoints.md)
- [Changelog](CHANGELOG.md)
- [Support](support.md)

--- 

### 👥 Research Team

- [Joe O'Regan](https://github.com/joeaoregan)
- [Adam O Neill Mc Knight](https://github.com/AdamQ45)
- [David Claffey](https://github.com/dclaff)
- [Edgars Peskaitis](https://github.com/edgar183)

---

## 📈 Performance Targets

> **Project Goal:** Target 15-20% reduction in urban traffic congestion for the Athlone "Orange Loop" using Reinforcement Learning.

> - **Average Travel Time (ATT):** Target -15%
> - **Mean Queue Length (MQL):** Target -20%
> - **Data Integrity:** TLS 1.3 secured telemetry pipeline

---

## 🔗 Quick Links

| 🌐 API Gateway                                                                 | 🤖 Inference Service                                              | 🧠 LSTM Predictor |
|---|---|---|
| [App](https://ai-traffic-control-api.onrender.com/)                             | [App](https://traffic-inference-service.onrender.com)             | [App](https://lstm-predictor-service.onrender.com)     |
| [Swagger UI Docs](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html) | [Fast API Docs](https://traffic-inference-service.onrender.com/docs) | [Fast API Docs](https://lstm-predictor-service.onrender.com/docs) |
| Local: `8080` | Local: `8000` | Local: `8001` |

---

## 🏗️ System Architecture

This repository implements a **Cloud-Native Microservices Pipeline** designed for the Athlone "Orange Loop" case study.

- **Traffic Monitoring Gateway (Java/Spring Boot):** Manages secure telemetry ingestion and orchestrates service communication with JWT authentication.
- **RL-Inference Service (Python/FastAPI):** Hosts a trained **PPO (Proximal Policy Optimization)** model to predict optimal signal timings based on real-time traffic density.
- **LSTM Traffic Predictor (Python/FastAPI):** Forecasts vehicle flow 15 minutes ahead using historical SUMO data for context-aware decision making.
- **Simulation Layer (SUMO):** Integrated high-fidelity environment for testing adaptive signal logic against baseline fixed-time controllers.

This system is specifically modeled to address the saturation flow rates and signal-timing patterns of the Athlone 'Orange Loop' corridor, providing a scalable template for Smart City traffic management.

*For more details see [System Architecture](system-architecture/index.md) page.*

---

## 📚 Service Documentation

- **[Java API Gateway](api-gateway/index.md)** — JWT authentication, traffic prediction endpoints, circuit breaker resilience
- **[Python Inference Service](inference-service/index.md)** — PPO model inference, GRU hidden state management
- **[LSTM Traffic Predictor](lstm/index.md)** — Time-series forecasting, SUMO data integration
- **[SUMO Simulator](sumo/architecture.md)** — Road network, traffic flows, output data generation

---

## 🔐 Security

JWT authentication is integrated into the API Gateway. See [Java API Gateway Authentication Guide](security/java-api-gateway.md) for configuration and usage.