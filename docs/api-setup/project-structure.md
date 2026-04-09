# 🗂️ Project Structure

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
│   │   │   ├── dto/
│   │   │   │   ├── LoginRequest.java        # Login request DTO
│   │   │   │   └── LoginResponse.java       # Login response DTO
│   │   │   └── service/
│   │   │       └── RlInferenceClient.java   # RL service client
│   │   └── main/resources/
│   │       ├── application.yml              # Spring config
│   │       └── application-prod.yml         # Production config
│   ├── pom.xml                             # Maven configuration
│   ├── Dockerfile                          # Java service Docker image
│   └── README.md                           # Gateway JWT Authentication guide
├── lstm-predictor-service/                 # Python LSTM forecasting service
│   ├── app/
│   │   ├── main.py                         # FastAPI application
│   │   └── models/                         # Directory for trained models
│   ├── Dockerfile                          # Python service Docker image
│   ├── requirements.txt                    # Python dependencies
│   └── .env.example                        # Environment variables template
├── rl-inference-service/                   # Python FastAPI RL service
│   ├── app/
│   │   ├── main.py                         # FastAPI application
│   │   └── models/                         # Directory for trained models
│   ├── Dockerfile                          # Python service Docker image
│   ├── requirements.txt                    # Python dependencies
│   └── .env.example                        # Environment variables template
├── docs/                                   # MkDocs documentation
│   ├── 1_home/                             # Quick reference guides
│   │   ├── INDEX.md
│   │   ├── 3_setup.md
│   │   ├── 4_api.md
│   │   └── ...
│   ├── 4_setup/                            # Detailed setup & configuration
│   │   ├── 1_created.md
│   │   ├── 2_quickstart.md
│   │   ├── 3_architecture.md
│   │   └── ...
│   ├── mkdocs.yml                          # MkDocs configuration
│   └── FEATURES.md                         # Feature matrix
├── SUMO/                                   # SUMO traffic simulation
│   ├── results/
│   │   └── Base/
│   └── Simulations/
│       └── Base/
├── docker-compose.yml                      # Docker Compose orchestration
├── test_api.py                             # API test client with color output
├── CHANGELOG.md                            # Change log
├── FILE_MANIFEST.md                        # File manifest
├── QUICKSTART.md                           # Quick start guide
├── README.md                               # Main readme
├── SYSTEM_ARCHITECTURE.md                  # Detailed architecture
└── SUPPORT.md                              # Support & contributing
```