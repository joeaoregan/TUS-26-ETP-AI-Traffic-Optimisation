# 🛡️ Exception Handling & Resilience

The system implements a centralised exception handling strategy to ensure service stability, especially during inter-service communication between the **Java API Gateway** and the **Python AI Services**.

## 🏗️ Architecture
The project uses Spring Boot's `@ControllerAdvice` to intercept exceptions globally. This prevents raw stack traces from being exposed to the end-user, which is a key security best practice.

### Key Components
* **`RlInferenceException`**: A custom runtime exception used specifically for failures during Reinforcement Learning inference requests.
* **`GlobalExceptionHandler`**: Intercepts all exceptions and maps them to standardised `ErrorResponse` DTOs.

## 🚦 Handling Inter-Service Failures
When the Gateway communicates with the `rl-inference-service` or `lstm-predictor-service`, several things can go wrong (timeouts, connection refused, or invalid model state).

| Exception | HTTP Status | Mitigation Strategy |
| :--- | :--- | :--- |
| `RlInferenceException` | 502 Bad Gateway | Logs the specific AI service error and returns a clean JSON response. |
| `MethodArgumentNotValidException` | 400 Bad Request | Validates input telemetry vectors before they reach the AI models. |
| `Exception` (General) | 500 Internal Error | Generic fallback to prevent internal logic leakage. |

## 📝 Standardised Error Response
All exceptions return a consistent JSON contract, allowing the frontend or simulation scripts to handle errors gracefully:

```json
{
  "message": "Error communicating with RL service",
  "details": "Connection timed out",
  "timestamp": "2026-04-27T10:00:00Z"
}
```