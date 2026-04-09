### Python Service (RL Inference)

| Environment Variable | Description                        | Default                          |
|----------------------|------------------------------------|----------------------------------|
| `MAPPO_AGENT_PATH`   | Path to MAPPO agent checkpoint     | `/app/trained_models/agent.th`   |
| `API_HOST`           | API host address                   | `0.0.0.0`                        |
| `API_PORT`           | API port number                    | `8000`                           |
| `API_RELOAD`         | Enable auto-reload on code changes | `false`                          |

### Java Gateway

| Environment Variable           | Description                          | Default                                |
|--------------------------------|--------------------------------------|----------------------------------------|
| `RL_INFERENCE_SERVICE_URL`     | RL Inference Service URL             | `http://localhost:8000/predict_action` |
| `RL_INFERENCE_SERVICE_TIMEOUT` | Request timeout in ms                | `10000`                                |
| `JWT_SECRET`                   | Signing secret for access tokens     | (minimum 32 chars)                     |
| `JWT_ISSUER`                   | JWT issuer name                      | `traffic-api-gateway`                  |
| `JWT_EXPIRATION_MINUTES`       | Access token lifetime in minutes     | `60`                                   |
| `JWT_AUTH_USERNAME`            | Login username for `/api/auth/login` | `admin`                                |
| `JWT_AUTH_PASSWORD`            | Login password for `/api/auth/login` | `admin123`                             |