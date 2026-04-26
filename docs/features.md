# 🔧 Key Features

**Updated**: 26/04/2026

## Key

- [x] Have
- [ ] In progress / Future / Nice to have

## Python RL Inference Service

**Status**: Fully operational.

Loads trained MAPPO models and serves real-time signal predictions via REST API with stateful GRU hidden state management.

- [x] Loads trained MAPPO agent (GRU-based)
- [x] RESTful action prediction (`POST /predict_action`)
- [x] Stateful hidden state per junction
- [x] Health monitoring (`GET /health`)
- [x] Model info endpoint (`GET /model_info`)
- [x] Comprehensive error handling
- [x] Interactive API documentation (Swagger UI)
- [x] Configurable via environment variables
- [x] Support for 5 junctions with variable action spaces
- [x] Hidden state reset (`POST /reset_hidden`)
- [ ] Request/response caching for identical observations
- [ ] Model versioning and switching at runtime
- [ ] Metrics collection (request counts, latency)

## Python LSTM Predictor Service

**Status**: Fully operational.

Forecasts traffic density using LSTM neural networks with batch prediction support for RL lookahead planning.

- [x] Loads trained LSTM model (64 units, dropout 0.2)
- [x] Single prediction (`POST /predict`)
- [x] Batch prediction (`POST /predict-batch`) — RL integration
- [x] Health monitoring (`GET /health`)
- [x] Model info endpoint (`GET /model-info`)
- [x] Performance metrics (`GET /metrics`)
- [x] Comprehensive error handling
- [x] Interactive API documentation (Swagger UI)
- [x] Configurable via environment variables
- [x] Data normalization (MinMaxScaler)
- [x] Multi-step ahead forecasting (up to 100 sequences)
- [x] Data analysis scripts (edge-analysis.py, trip-analysis.py)
- [x] Docker containerization (multi-stage build)
- [x] Model trained (MAE 0.2084 on normalized data)
- [x] Stationarity enhancements via differencing and scaling
- [x] Comprehensive unit testing (Pytest suite with coloured diagnostice output)
- [x] Achieve MAE < 10% on raw traffic values
- [ ] Bidirectional LSTM for enhanced accuracy
- [ ] Attention mechanism for temporal weighting
- [ ] Real-time model retraining capability
- [ ] Weather data integration
- [ ] KNN imputation for missing sensor data

## Java API Gateway

**Status**: Fully operational.

Orchestrates requests between RL and LSTM services with JWT authentication and circuit breaker pattern.

- [x] REST API endpoints for traffic control
- [x] Communicates with Python services (RL + LSTM)
- [x] Health checks and monitoring
- [x] Robust error handling
- [x] Service dependency management
- [x] Circuit breaker pattern (Resilience4j)
- [x] JWT authentication (HS256)
- [x] Stateless token-based security
- [x] Load testing capabilities
- [x] API request rate limiting (`RateLimitFilter`)
- [x] Custom exception management (`RlInferenceException`)
- [x] OpenAPI/Swagger UI integration (Refined documentation)
- [ ] Request/response logging and audit trail
- [ ] Metrics export (Micrometer/Prometheus)
- [ ] Request validation and sanitization
- [ ] Role-based access control (RBAC)

## RL + LSTM Integration

**Status**: Operational.

Services communicate and exchange predictions for coordinated traffic optimization.

- [x] RL service calls LSTM for lookahead planning
- [x] LSTM batch endpoint supports multi-hour forecasts
- [x] Health checks verify both services running
- [x] API Gateway orchestrates requests
- [x] Error handling and fallback mechanisms
- [x] Integration test suite (`test_rl_integration.py`)
- [ ] Feedback loop from traffic state to model retraining
- [ ] Distributed tracing between services
- [ ] Unified metrics dashboard

## SUMO Traffic Simulator Integration

**Status**: Fully operational as standalone simulator.

- [x] SUMO network configuration
- [x] Vehicle simulation and tracking
- [x] Traffic light control via SUMO
- [x] Simulation metrics and reporting
- [x] Vehicle data collection and logging
- [x] edgeData.xml export for LSTM training
- [ ] Real-time traffic state feedback to API Gateway
- [ ] Live integration with RL control system
- [ ] TraCI (Traffic Control Interface) bidirectional communication

## Docker Integration

**Status**: Fully operational.

Multi-stage builds, Docker Compose orchestration with all 3 services, health checks, and persistent volumes.

- [x] Multi-stage builds for optimization (RL + LSTM)
- [x] Service orchestration with Docker Compose (all 3 services)
- [x] Health checks and automatic restart
- [x] Persistent volumes for trained models
- [x] Network isolation (traffic-network bridge)
- [x] Logging configuration (json-file driver)
- [x] Environment-based configuration
- [ ] Kubernetes deployment manifests
- [ ] Helm charts for production deployments
- [ ] Resource limits and requests configuration
- [ ] Container registry (Docker Hub/ECR)

## Security & Authentication

**Status**: JWT authentication implemented and merged to main.

Stateless token-based security with HS256 signing on API Gateway. Python services use internal network communication.

- [x] JWT token generation and validation (Gateway)
- [x] Bearer token authentication for API endpoints
- [x] HS256 signing
- [x] Token expiration and configuration
- [x] Stateless (no server sessions)
- [x] Service-to-service internal communication (no auth required)
- [x] Mutual TLS between microservices via self-signed CA
- [x] TLS 1.3 implementation for inter-service communication
- [x] Rate limiting per authenticated user
- [ ] Token refresh mechanism
- [ ] Role-based access control (RBAC)
- [ ] API key management
- [ ] Token revocation/blacklist
- [ ] Audit logging for authentication events

## Deployment

**Status**: Cloud deployment on Render operational.

Local Docker Compose development environment fully functional.

- [x] Cloud deployment on Render (RL + LSTM services)
- [x] Local Docker Compose environment (all 3 services)
- [x] Environment-based configuration (local/production)
- [x] Graceful service fallback and degradation
- [x] Model hot-loading without service restart
- [ ] Rollback mechanism for failed deployments
- [ ] Automated scaling based on load
- [ ] Secrets management (environment variables/vaults)
- [ ] Performance monitoring and alerting

## Monitoring & Observability

**Status**: Basic health checks and metrics endpoints implemented.

- [x] Health check endpoints (`GET /health`) — all 3 services
- [x] Model info endpoints (`GET /model_info`) — RL + LSTM
- [x] Performance metrics endpoint (`GET /metrics`) — LSTM
- [x] Colored terminal logging (startup, predictions, errors)
- [x] Inference latency tracking
- [x] Colored terminal logging
- [ ] Prometheus metrics export
- [ ] Grafana dashboards for visualization
- [ ] Distributed tracing (Jaeger/Zipkin)
- [ ] Centralized logging (ELK Stack/Loki)
- [ ] Alert rules and notifications
- [ ] SLA/SLO tracking
- [ ] Custom business metrics

## Documentation

**Status**: Comprehensive and up-to-date.

MkDocs with Material theme, auto-generated API docs, setup guides, and architecture documentation.

- [x] Root README with architecture and quick start
- [x] RL Service README (endpoints, config, architecture)
- [x] LSTM Service README (endpoints, config, training)
- [x] Integration guide (`docs/INTEGRATION.md`)
- [x] Features documentation (this file)
- [x] Auto-generated API documentation (Swagger/OpenAPI)
- [x] Setup and troubleshooting guides
- [x] Architecture and design documentation
- [x] Docker Compose configuration documented
- [x] GitHub Pages hosting
- [ ] Versioned documentation (multiple versions)
- [ ] Search functionality
- [ ] Custom domain setup (optional)

## GitHub Pages Site

**Status**: Published.

- [x] MkDocs Material theme
- [x] Auto-generated from main branch docs
- [x] Published at: https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/
- [ ] Search functionality
- [ ] Versioned documentation (multiple versions)
- [ ] Custom domain setup (optional)