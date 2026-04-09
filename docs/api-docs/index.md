# API Documentation

## 🔗 Live Interactive Documentation

Swagger UI provides interactive, real-time API documentation with live testing capabilities.

### Production

- **[API Gateway Swagger UI](https://ai-traffic-control-api.onrender.com/swagger-ui/index.html)** — Traffic prediction and state management
- **[Inference Service Swagger UI](https://traffic-inference-service.onrender.com/docs)** — RL model inference
- **[LSTM Predictor Swagger UI](https://lstm-predictor-service.onrender.com/docs)** — Traffic forecasting (planned)

### Local Development

- **API Gateway:** http://localhost:8080/swagger-ui/index.html
- **Inference Service:** http://localhost:8000/docs
- **LSTM Predictor:** http://localhost:8001/docs

---

## 📚 Detailed Endpoint Documentation

For comprehensive endpoint specifications, request/response examples, and usage guides, see the service documentation:

- **[Java API Gateway](../api-gateway/endpoints.md)** — Authentication, traffic prediction, state reset
- **[Python Inference Service](../inference-service/endpoints.md)** — Model inference, health checks, model information
- **[LSTM Traffic Predictor](../lstm/endpoints.md)** — Traffic forecasting, model metadata

---

## 🔐 Authentication

**JWT Bearer Token Required** for protected endpoints in the API Gateway.

1. Authenticate via `POST /api/auth/login` to receive a token
2. Include token in `Authorization: Bearer <token>` header on protected requests

See [JWT Authentication Guide](../security/java-api-gateway.md) for detailed configuration and examples.

---

## How Auto-Generated Documentation Works

### Java API Gateway (springdoc-openapi)

Swagger documentation is automatically generated from annotations:

- `@Operation` — Endpoint summary and description
- `@ApiResponse` — Documented response codes and examples
- `@Schema` — Request/response model documentation
- `@Tag` — Groups related endpoints in the UI

### Python Services (FastAPI)

Swagger documentation is automatically generated from type hints and docstrings:

- `@app.get() / @app.post()` decorators — Endpoint definitions
- **Function docstrings** — Summaries and descriptions
- **Pydantic type hints** — Request/response schemas
- **Response models** — Define expected HTTP structures
- **Tags** — Organize endpoints into groups
- **Status codes** — Document error responses

This keeps documentation in sync with code without extra maintenance overhead.

---

## Testing with Swagger

1. Navigate to the Swagger UI link (production or local)
2. For protected endpoints: Click **"Authorize"** and paste your JWT token
3. Expand endpoint to see parameters and response schema
4. Click **"Try it out"** to send a test request
5. View response body, headers, and status code

---

## API Setup & Usage Guides

For step-by-step setup instructions, environment configuration, and usage examples, see:

- **[API Setup Guide](../api-setup/api-setup-guide.md)** — Docker Compose, local development, environment variables
- **[API Usage Examples](../api-setup/api-usage-examples.md)** — PowerShell, curl, Python examples
- **[Environment Variables](../api-setup/environment-variables.md)** — Configuration reference