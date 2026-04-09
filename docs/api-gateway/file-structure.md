# File Structure (Java API Gateway)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
java-api-gateway/
├── src/
│   ├── main/
│   │   ├── java/com/example/gateway/
│   │   │   ├── GatewayApplication.java              # Spring Boot application entry point
│   │   │   ├── controller/
│   │   │   │   ├── AuthController.java              # JWT login/token endpoints
│   │   │   │   └── TrafficController.java           # Traffic prediction and health endpoints
│   │   │   ├── config/
│   │   │   │   ├── SecurityConfig.java              # Spring Security and JWT configuration
│   │   │   │   ├── OpenApiConfig.java               # Swagger/OpenAPI documentation config
│   │   │   │   └── WebConfig.java                   # Static resource routing
│   │   │   ├── security/
│   │   │   │   ├── JwtService.java                  # JWT token generation and validation
│   │   │   │   └── JwtAuthenticationFilter.java     # Intercepts requests, validates JWT
│   │   │   ├── exception/
│   │   │   │   └── RlInferenceException.java        # Custom exception for RL service errors
│   │   │   ├── service/
│   │   │   │   └── RlInferenceClient.java           # HTTP client for inference service (predict, health, reset)
│   │   │   └── dto/
│   │   │       ├── LoginRequest.java                # { username, password }
│   │   │       ├── LoginResponse.java               # { tokenType, accessToken, expiresIn }
│   │   │       ├── TrafficActionRequest.java        # { junctionId, observations[], metadata }
│   │   │       ├── TrafficActionResponse.java       # { junctionId, predictedAction, signalState, timestamp, status }
│   │   │       ├── TrafficSignalState.java          # Enum: RED, YELLOW, GREEN, GREEN_EXTENDED, UNKNOWN
│   │   │       ├── ErrorResponse.java               # { status, message, timestamp }
│   │   │       └── HealthResponse.java              # { status, inferenceService, timestamp }
│   │   └── resources/
│   │       ├── application.yml                      # Local development config (port 8080, localhost:8000)
│   │       └── application-prod.yml                 # Production config (Render, env variables)
│   ├── test/
│   │   └── java/com/example/gateway/
│   │       └── [test classes]
│   └── pom.xml                                      # Maven dependencies and build config
├── Dockerfile                                       # Multi-stage Java image (builder + runtime)
├── README.md                                        # JWT authentication guide and setup
└── .gitignore
```

---

## Package Organization

| Package | Purpose |
|---------|---------|
| `controller/` | REST endpoint handlers (HTTP requests/responses) |
| `config/` | Spring Boot configuration (security, API docs, web) |
| `security/` | JWT token generation, validation, and request filtering |
| `service/` | Business logic layer (inference client, traffic processing) |
| `exception/` | Custom application exceptions |
| `dto/` | Data Transfer Objects (request/response models) |

---

## Key Files

- **GatewayApplication.java** — Spring Boot entry point, RestTemplate bean
- **TrafficController.java** — 4 REST endpoints (login, predict, reset, health)
- **RlInferenceClient.java** — HTTP client for `http://localhost:8000` inference service
- **JwtService.java** — Token generation (HS256), expiration handling
- **SecurityConfig.java** — Spring Security filters, endpoint protection rules