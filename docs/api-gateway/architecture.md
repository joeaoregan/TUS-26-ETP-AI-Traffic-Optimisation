# Architecture (Java API Gateway)

## Technology Stack

- **Framework**: Spring Boot 3.2.3
- **Language**: Java 17
- **Build**: Maven
- **Deployment**: Docker (Render cloud platform)
- **API Documentation**: SpringDoc OpenAPI (Swagger UI)

## Configuration

- **Local Development**: Port `8080`
- **Production URL**: `https://ai-traffic-control-api.onrender.com`
- **Inference Service**: Communicates via REST to RL backend (default: `http://localhost:8000`)

| Environment Variables | Default | Purpose |
|---|---|---|
| `JWT_SECRET`  | `change-this-secret-key-to-a-very-long-random-value`  | HMAC signing key (min 32 bytes) |
| `JWT_AUTH_USERNAME` | `admin` | Login username  |
| `JWT_AUTH_PASSWORD` | `admin123` | Login password |
| `JWT_EXPIRATION_MINUTES` | `60`  | Token lifetime in minutes |
| `JWT_ISSUER`  | `traffic-api-gateway` | Token issuer claim |
| `RL_INFERENCE_URL` | `http://localhost:8000/predict_action` | RL inference service endpoint |

For details JWT configuration and usage, see [Java API Gateway Authentication Guide](../security/java-api-gateway.md).

## Core Components

**AuthController** (`controller/AuthController.java`)

- Handles JWT token generation
- Validates username/password credentials
- Issues signed bearer tokens

**TrafficController** (`controller/TrafficController.java`)

- Handles all HTTP traffic prediction requests
- Manages error responses and validation
- Coordinates with the inference client
- Supports demo and custom observation modes

**JwtService** (`security/JwtService.java`)

- Validates configured signing secret at startup
- Signs tokens using HS256
- Parses and validates incoming tokens
- Extracts username from token subject

**JwtAuthenticationFilter** (`security/JwtAuthenticationFilter.java`)

- Reads the Authorization header
- Validates Bearer token format
- Adds authenticated principal to Spring Security context

**SecurityConfig** (`config/SecurityConfig.java`)

- Disables CSRF for stateless API
- Configures stateless session management
- Allows public access to login, health, and Swagger endpoints
- Requires authentication for traffic action endpoints

**RlInferenceClient** (`service/RlInferenceClient.java`)

- HTTP client for RL inference service communication
- Handles timeouts (2s default), retries, and error mapping
- Provides health checks and state reset functionality

**OpenApiConfig** (`config/OpenApiConfig.java`)

- Swagger/OpenAPI configuration
- Auto-generates interactive API documentation

**WebConfig** (`config/WebConfig.java`)

- Static resource routing
- Serves `index.html` and frontend assets