# Java API Gateway Authentication

This document describes the JWT authentication that has been added to the Spring Boot API gateway.

## Overview

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
