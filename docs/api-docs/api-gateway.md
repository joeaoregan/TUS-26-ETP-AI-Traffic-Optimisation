# Java API Gateway

## Live Documentation

**[API Gateway Swagger UI](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)** (Production)

**Local:** http://localhost:8080/swagger-ui/index.html

---

## Detailed Endpoint Documentation

See **[Endpoints](endpoints.md)** for comprehensive specifications of:

- `POST /api/auth/login` — JWT token issuance
- `GET /api/traffic/action` — Demo traffic prediction (requires authentication)
- `POST /api/traffic/action` — Custom observation prediction (requires authentication)
- `POST /api/traffic/reset` — Reset GRU hidden states (requires authentication)
- `GET /api/traffic/health` — Service health check (public)

---

## Authentication

All prediction and state management endpoints require JWT authentication.

See **[JWT Authentication Guide](../security/java-api-gateway.md)** for:

- Configuration and setup
- Token generation and usage
- Request/response examples
- Testing with Swagger UI

---

## Architecture & Features

- **[Architecture](architecture.md)** — Technology stack, configuration, core components
- **[Key Features](key-features.md)** — Security, prediction modes, signal state mapping, graceful degradation

---

## Swagger Auto-Generation

Documentation is automatically generated from Java annotations in the codebase:

- `@Operation` — Endpoint descriptions
- `@ApiResponse` — Response codes and examples
- `@Schema` — Model field documentation
- `@Tag` — Endpoint grouping

This ensures documentation stays in sync with implementation.