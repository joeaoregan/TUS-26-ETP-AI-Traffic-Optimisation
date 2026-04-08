# AI Traffic Control API Gateway

## Overview

The **Traffic Control API Gateway** is a Spring Boot REST API that serves as the orchestration layer for an AI-driven traffic optimization system. It interfaces with a Reinforcement Learning (RL) inference service to predict optimal traffic signal states and manage traffic flow in real-time.

## Purpose

This microservice provides:

- **Traffic Signal Prediction**: Uses a MAPPO (Multi-Agent PPO) RL model to predict optimal traffic signal actions
- **Inference Orchestration**: Acts as a bridge between traffic control applications and the RL inference backend
- **Resilience & Fallback**: Implements circuit-breaker patterns with graceful fallback when the inference service is unavailable
- **Health Monitoring**: Exposes health check endpoints to verify inference service availability
- **API Documentation**: Auto-generated OpenAPI (Swagger) documentation for all endpoints

## Key Features

- **Dual Prediction Modes**:
  - **Demo Mode** (`GET /api/traffic/action`): Generates random observations for quick testing
  - **Custom Mode** (`POST /api/traffic/action`): Accepts real or experimental observation vectors

- **Flexible Observations**: Supports variable-length observation vectors (up to 19 floats per junction)

- **Multiple Junction Support**: Preconfigured for 5 known traffic junctions:
  - `joinedS_265580996_300839357`
  - `300839359`
  - `265580972`
  - `1270712555`
  - `8541180897`

- **Signal State Mapping**: Translates RL model outputs (0-3) to human-readable states:
  - `0` → RED
  - `1` → YELLOW
  - `2` → GREEN
  - `3` → GREEN_EXTENDED
  - `default` → UNKNOWN

- **Graceful Degradation**: Falls back to RED signal when inference service is unavailable

- **Stateful Inference**: Includes endpoints to reset GRU hidden states for multi-step simulations

## Architecture

### Technology Stack

- **Framework**: Spring Boot 3.2.3
- **Language**: Java 17
- **Build**: Maven
- **Deployment**: Docker (Render cloud platform)
- **API Documentation**: SpringDoc OpenAPI (Swagger UI)

### Configuration

- **Local Development**: Port `8080`
- **Production URL**: `https://ai-traffic-control-api.onrender.com`
- **Inference Service**: Communicates via REST to RL backend (default: `http://localhost:8000`)

### Core Components

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

## API Endpoints

### Traffic Prediction

#### GET `/api/traffic/action`
**Demo endpoint** - Picks a random junction and generates dummy observations.

**Response (200)**:
``` json
{
  "junctionId": "300839359",
  "predictedAction": 1,
  "signalState": "YELLOW",
  "timestamp": 1710000000000,
  "status": "success"
}
```

**Response (Fallback - Inference Down)**:
``` json
{
  "junctionId": "300839359",
  "predictedAction": 0,
  "signalState": "RED",
  "timestamp": 1710000000000,
  "status": "fallback_mode (inference service down)"
}
```

#### POST `/api/traffic/action`
**Production endpoint** - Accepts junction ID and custom observation vector.

**Request**:
``` json
{
  "junctionId": "joinedS_265580996_300839357",
  "observations": [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.12, 0.08, 0.33, 0.41, 0.22, 0.55, 0.18, 0.62, 0.70, 0.81, 0.50],
  "metadata": "morning-peak"
}
```

**Response (200)**: Same structure as demo endpoint

**Errors**:

- `400`: Missing or invalid `junctionId` / `observations`
- `400`: Observations exceed maximum size (19)
- `500`: Unexpected internal error

### State Management

#### POST `/api/traffic/reset`
**Reset GRU hidden states** for all junctions (call at start of simulation run).

**Response (200)**:

``` json
{
  "status": "ok",
  "message": "Hidden states reset for all junctions"
}
```

### Health & Monitoring

#### GET `/api/traffic/health`

**Service health check** - Verifies inference service availability.

**Response (200 - Healthy)**:
``` json
{
  "status": "healthy",
  "inferenceService": "up",
  "timestamp": 1710000000000
}
```

**Response (503 - Degraded)**:
``` json
{
  "status": "degraded",
  "inferenceService": "down",
  "timestamp": 1710000000000
}
```

## Configuration Files

### `application.yml` (Local Development)

- Inference URL: `http://localhost:8000/predict_action`
- Read/connect timeouts: 2s
- Observation dimension: 19 floats
- Logging level: DEBUG

### `application-prod.yml` (Production)

- Inference URL: Loaded from `RL_INFERENCE_URL` environment variable
- Read/connect timeouts: 20s (longer for cloud)
- Logging level: WARN (production-optimized)

## Deployment

### Docker Build

``` bash
docker build -t traffic-gateway:latest .
```

The Dockerfile uses a multi-stage build:

1. **Builder Stage**: Compiles Maven project with Java 17
2. **Runtime Stage**: Minimal JRE container (~200MB)

### Running Locally

``` bash
mvn clean install
mvn spring-boot:run
```

Then visit:

- **Swagger UI**: `http://localhost:8080/swagger-ui/index.html`
- **OpenAPI JSON**: `http://localhost:8080/v3/api-docs`

## Error Handling

| Error | Status | Handling |
|-------|--------|----------|
| Invalid junction ID           | 400            | Validation error with message |
| Observations too large        | 400            | Validation error with size info |
| Inference service unreachable | 200 (Fallback) | Returns RED signal state with fallback status |
| Unexpected exception          | 500            | Generic error response |

## Dependencies

**Core**:

- `spring-boot-starter-web`: REST API framework
- `spring-boot-starter-webflux`: Async support
- `springdoc-openapi-starter-webmvc-ui` (v2.5.0): Swagger documentation
- `jackson-databind`: JSON serialization

**Development**:

- `lombok`: Reduce boilerplate (@Data, @Slf4j, @RequiredArgsConstructor)

## Integration with AI Inference Service

This gateway expects a Python FastAPI backend at the configured `RL_INFERENCE_URL` with endpoints:

- `POST /predict_action`: Accepts `{"junction_id": "...", "obs_data": [...]}`, returns `{"action": 0-3, "confidence": 0.0-1.0}`
- `GET /health`: Returns `{"status": "healthy", "modelLoaded": true, "junctions": [...]}`
- `POST /reset_hidden`: Resets GRU hidden states

## Quick Links

- **GitHub Repository**: https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation
- **Live Swagger UI (Cloud)**: https://ai-traffic-control-api.onrender.com/swagger-ui/index.html
- **Inference Service Docs**: https://traffic-inference-service.onrender.com/docs
- **Full Project Documentation**: https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/

---