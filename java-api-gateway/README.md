# Java API Gateway Authentication

![TUS](https://img.shields.io/badge/TUS-2026-black?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iMTU3LjU1OTM2bW0iCiAgIGhlaWdodD0iMjA1LjE3MTE2bW0iCiAgIHZpZXdCb3g9IjAgMCAxNTcuNTU5MzYgMjA1LjE3MTE2IgogICB2ZXJzaW9uPSIxLjEiCiAgIGlkPSJzdmcxIgogICB4bWw6c3BhY2U9InByZXNlcnZlIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxzb2RpcG9kaTpuYW1lZHZpZXcKICAgICBpZD0ibmFtZWR2aWV3MSIKICAgICBwYWdlY29sb3I9IiNmZmZmZmYiCiAgICAgYm9yZGVyY29sb3I9IiMwMDAwMDAiCiAgICAgYm9yZGVyb3BhY2l0eT0iMC4yNSIKICAgICBpbmtzY2FwZTpzaG93cGFnZXNoYWRvdz0iMiIKICAgICBpbmtzY2FwZTpwYWdlb3BhY2l0eT0iMC4wIgogICAgIGlua3NjYXBlOnBhZ2VjaGVja2VyYm9hcmQ9IjAiCiAgICAgaW5rc2NhcGU6ZGVza2NvbG9yPSIjZDFkMWQxIgogICAgIGlua3NjYXBlOmRvY3VtZW50LXVuaXRzPSJtbSI+PGlua3NjYXBlOnBhZ2UKICAgICAgIHg9IjAiCiAgICAgICB5PSIwIgogICAgICAgd2lkdGg9IjE1Ny41NTkzNiIKICAgICAgIGhlaWdodD0iMjA1LjE3MTE2IgogICAgICAgaWQ9InBhZ2UyIgogICAgICAgbWFyZ2luPSIwIgogICAgICAgYmxlZWQ9IjAiIC8+PC9zb2RpcG9kaTpuYW1lZHZpZXc+PGRlZnMKICAgICBpZD0iZGVmczEiPjxzdHlsZQogICAgICAgaWQ9InN0eWxlMSI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48c3R5bGUKICAgICAgIGlkPSJzdHlsZTEtNCI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48L2RlZnM+PGcKICAgICBpbmtzY2FwZTpsYWJlbD0iTGF5ZXIgMSIKICAgICBpbmtzY2FwZTpncm91cG1vZGU9ImxheWVyIgogICAgIGlkPSJsYXllcjEiCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjA4LjE2MDkzLDQ4Ljg3NTE2MikiPjxnCiAgICAgICBpZD0iQXJ0d29yayIKICAgICAgIHRyYW5zZm9ybT0ibWF0cml4KDAuMjY0NTgzMzMsMCwwLDAuMjY0NTgzMzMsLTIwOC4xNjA5NCwtNDguODc1MTU4KSI+PHBhdGgKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICBkPSJNIDU5NS40OCwwIEggNDc2LjM4IFYgNTguNTIgSCAzNTcuMyBWIDAgSCAyMzguMiBWIDU4LjUyIEggMTE5LjEgViAwIEggMCB2IDM1Ny4yOSBoIDExOS4xIGEgMTc4LjY0LDE3OC42NCAwIDEgMSAzNTcuMjgsMCBoIDExOS4wNiB6IgogICAgICAgICBpZD0icGF0aDEiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSI0NzYuMzgiCiAgICAgICAgIHk9IjcxNS45MDAwMiIKICAgICAgICAgd2lkdGg9IjExOS4xIgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3QxIiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNzE1LjkwMDAyIgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDIiCiAgICAgICAgIHg9IjAiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB5PSI1OTYuNzk5OTkiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSI1OS41NDk5OTkiCiAgICAgICAgIGlkPSJyZWN0MyIKICAgICAgICAgeD0iMCIgLz48cmVjdAogICAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICAgIHg9IjQ3Ni4zOTk5OSIKICAgICAgICAgeT0iNTk2Ljc5OTk5IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDQiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSIxMTkuMSIKICAgICAgICAgeT0iNTM3LjI1IgogICAgICAgICB3aWR0aD0iMzU3LjI5OTk5IgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3Q1IiAvPjxwb2x5Z29uCiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgcG9pbnRzPSI0NzYuMzksNjU2LjM1IDExOS4xLDY1Ni4zNSAxMTkuMSw3MTUuOSAyMzguMiw3MTUuOSAyMzguMiw3NzUuNDUgMzU3LjI5LDc3NS40NSAzNTcuMjksNzE1LjkgNDc2LjM5LDcxNS45ICIKICAgICAgICAgaWQ9InBvbHlnb241IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeD0iNDc2LjM5OTk5IgogICAgICAgICB5PSI0MTguMTYiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSIxMTkuMSIKICAgICAgICAgaWQ9InJlY3Q2IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNDE4LjE2IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iMTE5LjEiCiAgICAgICAgIGlkPSJyZWN0NyIKICAgICAgICAgeD0iMCIgLz48L2c+PC9nPjwvc3ZnPgo=)
![Module](https://img.shields.io/badge/Module-Engineering%20Team%20Project-blue?style=flat-square)
![Topic](https://img.shields.io/badge/Topic-AI%20Traffic%20Optimisation-blue?style=flat-square)

## Overview

This document describes the JWT authentication that has been added to the Spring Boot API gateway.

Authentication is handled at the gateway layer using JSON Web Tokens (JWT).

The flow is intentionally simple:

1. A client sends a username and password to `POST /api/auth/login`.
2. The gateway validates those credentials against configured values.
3. If the credentials are valid, the gateway returns a signed bearer token.
4. The client sends that token in the `Authorization` header when calling protected endpoints.

This implementation uses stateless authentication. No server-side session is created.

## What Is Protected

### Public endpoints

- `POST /api/auth/login`
- `GET /api/traffic/health`
- `GET /swagger-ui/**`
- `GET /v3/api-docs/**`
- Static resources such as `/`, `/index.html`, `/app.js`, `/styles.css`, and `/images/**`

### Protected endpoints

- `GET /api/traffic/action`
- `POST /api/traffic/action`

Requests to protected endpoints must include a bearer token.

## Configuration

Authentication and JWT settings are configured in `application.yml` and can be overridden with environment variables.

| Property                          | Environment variable     | Default                                              | Notes |
|-----------------------------------|--------------------------|------------------------------------------------------|-------|
| `security.jwt.issuer`             | `JWT_ISSUER`             | `traffic-api-gateway`                                | Used as the JWT issuer claim        |
| `security.jwt.secret`             | `JWT_SECRET`             | `change-this-secret-key-to-a-very-long-random-value` | Must be at least 32 bytes for HS256 |
| `security.jwt.expiration-minutes` | `JWT_EXPIRATION_MINUTES` | `60`                                                 | Token lifetime |
| `security.auth.username`          | `JWT_AUTH_USERNAME`      | `admin`                                              | Login username |
| `security.auth.password`          | `JWT_AUTH_PASSWORD`      | `admin123`                                           | Login password |

## Security Notes

- The default username, password, and secret are for local development only.
- Replace `JWT_SECRET` before deploying anywhere outside a local environment.
- This implementation currently uses a single configured username and password.
- There is no refresh-token flow yet.
- Invalid or expired tokens are treated as unauthenticated requests.

## How It Works Internally

### `AuthController`

`POST /api/auth/login` accepts a JSON payload:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

If the credentials match the configured values, the controller returns:

```json
{
  "tokenType": "Bearer",
  "accessToken": "<jwt>",
  "expiresIn": 3600,
  "timestamp": 1710000000000
}
```

### `JwtService`

The JWT service:

- Validates the configured signing secret at startup
- Signs tokens using HS256
- Stores the username in the `sub` claim
- Adds `iss`, `iat`, and `exp` claims
- Parses and validates incoming tokens

### `JwtAuthenticationFilter`

The request filter:

- Reads the `Authorization` header
- Expects the format `Bearer <token>`
- Validates the token
- Extracts the username from the token subject
- Adds an authenticated principal to the Spring Security context

### `SecurityConfig`

Spring Security is configured to:

- Disable CSRF for this stateless API
- Disable HTTP Basic authentication
- Use stateless session management
- Allow public access to login, health, Swagger, and static assets
- Require authentication for traffic action endpoints

## Running Locally

### Option 1: Docker Compose

The `docker-compose.yml` file includes these JWT-related environment variables for the gateway:

```yaml
JWT_SECRET: change-this-secret-key-to-a-very-long-random-value
JWT_AUTH_USERNAME: admin
JWT_AUTH_PASSWORD: admin123
JWT_EXPIRATION_MINUTES: "60"
```

Start the services:

```bash
docker-compose up --build
```

### Option 2: Maven

From the `java-api-gateway` directory:

```bash
mvn spring-boot:run
```

If you want to override the defaults, set environment variables first.

Example PowerShell:

```powershell
$env:JWT_SECRET="replace-with-a-long-random-secret-of-at-least-32-characters"
$env:JWT_AUTH_USERNAME="admin"
$env:JWT_AUTH_PASSWORD="admin123"
$env:JWT_EXPIRATION_MINUTES="60"
mvn spring-boot:run
```

## Usage Examples

### PowerShell

Authenticate:

```powershell
$loginBody = @{
    username = "admin"
    password = "admin123"
} | ConvertTo-Json

$tokenResponse = Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/auth/login" -ContentType "application/json" -Body $loginBody
$token = $tokenResponse.accessToken
```

Call a protected endpoint:

```powershell
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Method Get -Uri "http://localhost:8080/api/traffic/action" -Headers $headers
```

Call the prediction endpoint with custom observations:

```powershell
$headers = @{ Authorization = "Bearer $token" }
$body = @{
    observations = @(0.12, 0.33, 0.41, 0.55, 0.62, 0.70, 0.81, 0.90, 0.95)
    metadata = "morning-peak"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8080/api/traffic/action" -Headers $headers -ContentType "application/json" -Body $body
```

### curl

Authenticate and capture the token:

```bash
TOKEN=$(curl -s -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq -r '.accessToken')
```

Call a protected endpoint:

```bash
curl -X GET http://localhost:8080/api/traffic/action \
  -H "Authorization: Bearer $TOKEN"
```

Call the prediction endpoint with custom observations:

```bash
curl -X POST http://localhost:8080/api/traffic/action \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "observations": [0.12, 0.33, 0.41, 0.55, 0.62, 0.70, 0.81, 0.90, 0.95],
    "metadata": "morning-peak"
  }'
```

## Swagger Usage

Swagger UI is still publicly reachable.

Open:

```text
http://localhost:8080/swagger-ui/index.html
```

You can authenticate by first calling `POST /api/auth/login`, copying the returned `accessToken`, and then using the Swagger `Authorize` button with:

```text
Bearer <your-token>
```

---

## Testing

The root-level `test_api.py` script has been updated to:

- Authenticate first using JWT credentials
- Cache the returned access token
- Send the token on protected requests
- Display color-coded output for better readability
- Track test results (e.g., "All tests passed! 4/4")
- Return boolean status for each test function

Run it from the repository root:

```bash
python test_api.py
```

Test output includes:

✅ Green checkmarks for successful operations
❌ Red X marks for failures
🔵 Blue headers for test sections
🔄 Test counter showing passed/total tests

### Requirements

To use the enhanced test script with color output, install colorama:

```bash
pip install colorama
```

## Relevant Files

- `src/main/java/com/example/gateway/controller/AuthController.java`
- `src/main/java/com/example/gateway/config/SecurityConfig.java`
- `src/main/java/com/example/gateway/security/JwtService.java`
- `src/main/java/com/example/gateway/security/JwtAuthenticationFilter.java`
- `src/main/resources/application.yml`
- `src/main/resources/application-prod.yml`
- `src/main/java/com/example/gateway/dto/LoginRequest.java`
- `src/main/java/com/example/gateway/dto/LoginResponse.java`
- `src/main/java/com/example/gateway/dto/ErrorResponse.java`
- `test_api.py`

## Current Limitations

- Single configured user only
- No user database integration
- No role-based authorization
- No refresh tokens
- No logout endpoint because the system is stateless

If the project needs stronger access control later, the next logical step is to replace configured credentials with a persistent user store and add roles.
