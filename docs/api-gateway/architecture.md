# Architecture

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

For details JWT configuration and usage, see [Java API Gateway Authentication Guide](../security/java-api-gateway.md).

## Core Components

**REST Controller** (`TrafficController.java`)

- Handles all HTTP traffic prediction requests
- Manages error responses and validation
- Coordinates with the inference client

**Inference Client** (`RlInferenceClient.java`)

- HTTP client for RL inference service communication
- Handles timeouts (2s default), retries, and error mapping
- Provides health checks and state reset functionality

**Configuration**

- `OpenApiConfig`: Swagger/OpenAPI configuration
- `WebConfig`: Static resource routing (serves `index.html`)
- `GatewayApplication`: Spring Boot application entry point with RestTemplate bean
