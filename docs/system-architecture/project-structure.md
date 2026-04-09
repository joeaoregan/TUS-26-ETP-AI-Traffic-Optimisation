# 🗂️ Project Structure

## Overall Structure

```
TUS-26-ETP-AI-Traffic-Optimisation/
├── java-api-gateway/                       # Java Spring Boot gateway (with JWT Auth)
│   ├── src/
│   │   ├── main/java/com/example/gateway/
│   │   │   ├── GatewayApplication.java     # Spring Boot app
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java      # JWT authentication endpoints
│   │   │   │   └── TrafficController.java   # REST traffic endpoints
│   │   │   ├── config/
│   │   │   │   └── SecurityConfig.java      # Spring Security configuration
│   │   │   ├── security/
│   │   │   │   ├── JwtService.java          # JWT token generation and validation
│   │   │   │   └── JwtAuthenticationFilter.java  # JWT request filter
│   │   │   ├── exception/
│   │   │   │   └── RlInferenceException.java # RL service communication errors
│   │   │   ├── dto/
│   │   │   │   ├── LoginRequest.java        # Login request DTO
│   │   │   │   ├── LoginResponse.java       # Login response DTO
│   │   │   │   ├── TrafficActionRequest.java # Traffic prediction request DTO
│   │   │   │   ├── TrafficActionResponse.java # Traffic prediction response DTO
│   │   │   │   ├── ErrorResponse.java       # Error response DTO
│   │   │   │   └── HealthResponse.java      # Health check response DTO
│   │   │   └── service/
│   │   │       └── RlInferenceClient.java   # RL service client (communicates with inference service)
│   │   └── main/resources/
│   │       ├── application.yml              # Spring config (local development)
│   │       └── application-prod.yml         # Production config (Render)
│   ├── pom.xml                             # Maven configuration
│   ├── Dockerfile                          # Multi-stage Java service Docker image
│   ├── README.md                           # Gateway setup and authentication guide
│   └── test_api.py                         # API test client with color output (local)
├── lstm-predictor-service/                 # Python LSTM forecasting service (framework stage)
│   ├── app/
│   │   ├── main.py                         # FastAPI application entry point
│   │   ├── data/
│   │   │   ├── loader.py                   # SUMO edgeData.xml parser
│   │   │   └── preprocessor.py             # Data normalization and windowing
│   │   ├── models/                         # Directory for trained LSTM models
│   │   ├── templates/
│   │   │   └── index.html                  # Landing page
│   │   └── static/                         # Static assets (logo, favicon)
│   ├── Dockerfile                          # Python service Docker image
│   ├── requirements.txt                    # Python dependencies (FastAPI, TensorFlow, pandas, etc.)
│   ├── .env.example                        # Environment variables template
│   └── README.md                           # LSTM service setup guide
├── rl-inference-service/                   # Python FastAPI RL inference service
│   ├── app/
│   │   ├── main.py                         # FastAPI application (MAPPO model)
│   │   ├── templates/
│   │   │   └── index.html                  # Landing page
│   │   └── static/                         # Static assets (logo, favicon)
│   ├── trained_models/
│   │   └── agent.th                        # Trained MAPPO model weights (PyTorch)
│   ├── Dockerfile                          # Python service Docker image
│   ├── requirements.txt                    # Python dependencies (FastAPI, PyTorch, etc.)
│   ├── .env.example                        # Environment variables template
│   └── README.md                           # Inference service setup guide
├── docs/                                   # MkDocs documentation (Material theme)
│   ├── index.md                            # Home page with quick links
│   ├── features.md                         # Feature matrix across all services
│   ├── CHANGELOG.md                        # Version history and updates
│   ├── support.md                          # Support and troubleshooting
│   ├── api-docs/
│   │   ├── index.md                        # API documentation hub
│   │   ├── api-gateway.md                  # API Gateway docs overview
│   │   ├── inference-service.md            # Inference Service docs overview
│   │   └── lstm.md                         # LSTM Service docs overview
│   ├── api-gateway/
│   │   ├── index.md                        # Gateway service overview
│   │   ├── architecture.md                 # Technology stack and components
│   │   ├── key-features.md                 # Security, prediction modes, etc.
│   │   └── endpoints.md                    # REST endpoint specifications
│   ├── inference-service/
│   │   ├── index.md                        # Inference service overview
│   │   ├── architecture.md                 # MAPPO model, GRU architecture
│   │   ├── key-features.md                 # Junctions, neural network details
│   │   └── endpoints.md                    # REST endpoint specifications
│   ├── lstm/
│   │   ├── index.md                        # LSTM service overview (placeholder)
│   │   ├── architecture.md                 # Technology stack, file structure
│   │   ├── key-features.md                 # Time-series forecasting capabilities
│   │   └── endpoints.md                    # REST endpoint specifications
│   ├── sumo/
│   │   ├── architecture.md                 # Network setup, simulation configuration
│   │   └── key-features.md                 # Traffic flows, output formats
│   ├── security/
│   │   └── java-api-gateway.md             # JWT authentication guide and configuration
│   ├── api-setup/
│   │   ├── api-setup-guide/
│   │   │   └── index.md
│   │   ├── api-usage-examples/
│   │   │   └── index.md
│   │   └── environment-variables/
│   │       └── index.md
│   ├── system-architecture/
│   │   └── index.md
│   ├── quickstart.md                       # 5-minute quick start
│   ├── mkdocs.yml                          # MkDocs configuration (Material theme)
│   └── images/
│       └── logo.png
├── SUMO/                                   # SUMO traffic simulation (Athlone network)
│   ├── osm.net.xml.gz                      # Road network (OpenStreetMap derived)
│   ├── osm.sumocfg                         # Main simulation configuration
│   ├── town_routes.rou.xml                 # 7 predefined routes with hourly flows
│   ├── tii_flows.xml                       # Vehicle type definitions
│   ├── tii_hourly_traffic.csv              # Source TII traffic data
│   ├── osm.view.xml                        # GUI display settings
│   ├── run.bat                             # One-click launcher
│   ├── Results/
│   │   ├── Base/
│   │   │   ├── edgeData.xml                # Per-edge hourly statistics
│   │   │   ├── tripinfos.xml               # Per-vehicle trip statistics
│   │   │   └── stats.xml                   # Overall simulation summary
│   │   └── MAPPO/
│   │       └── edgeData.xml                # Sample output from MAPPO training run
│   └── Simulations/
│       └── Base/
├── docker-compose.yml                      # Docker Compose orchestration (all services)
├── test_api.py                             # Python API test client (colorama, health checks)
├── CHANGELOG.md                            # Version history (v2.1.0 current)
├── README.md                               # Main project readme
└── SUPPORT.md                              # Support and contributing guidelines
```

## Individual Service Structure

- [Java API Gateway](../api-gateway/file-structure.md)
- [Python Inference Service](../inference-service/file-structure.md)
- [LSTM Traffic Predictor](../lstm/file-structure.md)
- [SUMO Traffic Simulator](../sumo/file-structure.md)
