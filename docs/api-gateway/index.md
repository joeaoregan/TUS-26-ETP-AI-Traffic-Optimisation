# AI Traffic Control API Gateway

## Overview

The [Traffic Control API Gateway](https://ai-traffic-control-api.onrender.com/) is a Spring Boot REST API that serves as the orchestration layer for an AI-driven traffic optimization system. It interfaces with a Reinforcement Learning (RL) inference service to predict optimal traffic signal states and manage traffic flow in real-time.

## Purpose

This microservice provides:

- **Traffic Signal Prediction**: Uses a MAPPO (Multi-Agent PPO) RL model to predict optimal traffic signal actions
- **Inference Orchestration**: Acts as a bridge between traffic control applications and the RL inference backend
- **Resilience & Fallback**: Implements circuit-breaker patterns with graceful fallback when the inference service is unavailable
- **Health Monitoring**: Exposes health check endpoints to verify inference service availability
- **API Documentation**: Auto-generated OpenAPI (Swagger) documentation for all endpoints

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

!!! success "POST `/predict_action`"
    Accepts

    ``` json
    {
      "junction_id": "...", 
      "obs_data": [...]
    }
    ```
    returns
       
    ``` json
    {
      "action": 0-3, 
      "confidence": 0.0-1.0
    }
    ```

!!! note "GET `/health`"
    Returns
    
    ``` json
    {
      "status": "healthy", 
      "modelLoaded": true, 
      "junctions": [...]
    }
    ```

!!! success "POST `/reset_hidden`"
    Resets GRU hidden states

## Quick Links

- **GitHub Repository**: <https://github.com/joeaoregan/TUS-26-ETP-AI-Traffic-Optimisation>
- **Live Swagger UI (Cloud)**: <https://ai-traffic-control-api.onrender.com/swagger-ui/index.html>
- **Inference Service Docs**: <https://traffic-inference-service.onrender.com/docs>
- **Full Project Documentation**: <https://joeaoregan.github.io/TUS-26-ETP-AI-Traffic-Optimisation/>

---