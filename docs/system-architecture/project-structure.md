# 🗂️ Project Structure

## Overall Structure

```
TUS-26-ETP-AI-Traffic-Optimisation/
├── java-api-gateway/                       # Spring Boot Edge & Orchestration Service
│   ├── src/main/java/com/example/gateway/
│   │   ├── GatewayApplication.java         # Main entry point for the Java Gateway
│   │   ├── config/
│   │   │   ├── OpenApiConfig.java          # Swagger UI / OpenAPI documentation config
│   │   │   ├── RateLimitFilter.java        # Individual contribution: API traffic throttling
│   │   │   ├── SecurityConfig.java         # Spring Security & JWT Filter chain config
│   │   │   └── WebConfig.java              # CORS and MVC configuration
│   │   ├── controller/
│   │   │   ├── AuthController.java         # David's work: Login and token endpoints
│   │   │   └── TrafficController.java      # Orchestration: Enhanced prediction & RL logic
│   │   ├── dto/                            # Data Transfer Objects (JSON Contracts)
│   │   │   ├── ErrorResponse.java          # Standardised error payload
│   │   │   ├── HealthResponse.java         # Service health status payload
│   │   │   ├── LoginRequest.java           # Authentication input
│   │   │   ├── LoginResponse.java          # JWT token delivery
│   │   │   ├── TrafficActionRequest.java   # Observation vector input for RL
│   │   │   ├── TrafficActionResponse.java  # Basic reactive action output
│   │   │   ├── EnhancedTrafficActionResponse.java # Merged LSTM/RL proactive output
│   │   │   ├── TrafficForecastResponse.java# Direct forecasting output
│   │   │   └── TrafficSignalState.java     # Model for current signal phase data
│   │   ├── exception/
│   │   │   ├── GlobalExceptionHandler.java # Centralised @ControllerAdvice
│   │   │   └── RlInferenceException.java    # Refactored: Custom exception for service errors
│   │   ├── security/
│   │   │   ├── JwtAuthenticationFilter.java# Custom stateless security filter
│   │   │   └── JwtService.java             # David's work: Token logic & validation
│   │   └── service/
│   │       ├── LstmPredictorClient.java    # Feign/Rest client for forecasting
│   │       └── RlInferenceClient.java      # Feign/Rest client for MAPPO inference
│   ├── src/main/resources/
│   │   ├── application.yml                 # Default development configuration
│   │   ├── application-prod.yml            # Deployment: Cloud-specific config (Render)
│   │   └── static/index.html               # Observability Dashboard (HTML/JS)
│   ├── src/test/java/com/example/gateway/  # JUnit & Mockito test suite
│   ├── Dockerfile                          # Multi-stage production container build
│   └── pom.xml                             # Maven dependency management
│
├── lstm-predictor-service/                 # Python FastAPI Forecasting Service
│   ├── app/
│   │   ├── main.py                         # FastAPI entry, health & metrics endpoints
│   │   ├── models/
│   │   │   ├── lstm_model.py               # Core Keras/TensorFlow model architecture
│   │   │   ├── lstm_train.py               # Model training and validation logic
│   │   │   └── preprocessor.py             # Refactored: Min-Max Scaling & Windowing
│   │   └── utils/
│   │       ├── feature_engineering.py      # Spatial-temporal lag feature logic
│   │       ├── metrics.py                  # MAE/RMSE calculation utilities
│   │       └── stationarity.py             # Research implementation: Stationarity enhancements
│   ├── trained_models/
│   │   ├── lstm_model.keras                # Persisted production model file
│   │   ├── scaler.pkl                      # Serialised Normalisation parameters
│   │   └── lstm_model_tf/                  # SavedModel format for alternate deployments
│   ├── tests/
│   │   └── test_api.py                     # Refactored: Pytest suite with coloured output
│   ├── Dockerfile                          # Lightweight Python deployment container
│   ├── requirements.txt                    # Python dependency manifest
│   └── runtime.txt                         # Platform-specific runtime versioning
│
├── rl-inference-service/                   # Python FastAPI RL Inference Service
│   ├── app/
│   │   ├── main.py                         # MAPPO logic & GRU hidden state management
│   │   ├── templates/index.html            # Service landing page
│   │   └── static/                         # Assets for service UI
│   ├── trained_models/
│   │   └── agent.th                        # Multi-Agent RL model weights (PyTorch)
│   ├── tests/
│   │   └── test_api.py                     # RL service validation suite
│   ├── Dockerfile                          # Container definition for RL component
│   └── requirements.txt                    # RL stack (PyTorch, numpy, FastAPI)
│
├── SUMO/                                   # Microscopic Traffic Simulation Layer
│   ├── Simulations/Base/
│   │   ├── osm.net.xml                     # Athlone 'Orange Loop' road network
│   │   ├── tii_hourly_traffic.csv          # TII real-world traffic count data
│   │   ├── town_routes.rou.xml             # Simulation demand & route definitions
│   │   └── osm.sumocfg                     # Simulation master configuration
│   └── Results/
│       ├── Base/                           # Metrics for Fixed-Time control
│       ├── MAPPO/                          # Metrics for Multi-Agent RL control
│       ├── matplotlib_stats_sumo.py        # Visualisation script for result comparison
│       └── report/                         # Comparative charts (74% improvement data)
│
├── docs/                                   # MkDocs documentation (Material theme)
|
├── tls/                                    # Security infrastructure
│   └── generate-certs.sh                   # Adam's work: TLS 1.3 certificate generation
├── docker-compose.yml                      # Main container orchestration
├── docker-compose.tls.yml                  # Overlay for secured communication
├── start.bat                               # Windows: Orchestrated startup script
├── start.sh                                # Linux/macOS: Orchestrated startup script
├── test_api.py                             # Root-level health & integration testing
└── README.md                               # Main project entry point
```

## Individual Service Structure

- [Java API Gateway](../api-gateway/file-structure.md)
- [Python Inference Service](../inference-service/file-structure.md)
- [LSTM Traffic Predictor](../lstm/file-structure.md)
- [SUMO Traffic Simulator](../sumo/file-structure.md)
