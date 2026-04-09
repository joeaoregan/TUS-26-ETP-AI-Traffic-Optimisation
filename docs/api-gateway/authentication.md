# Authentication (JWT)

The API Gateway now includes JWT (JSON Web Token) authentication for securing traffic prediction endpoints.

## Overview

- **Stateless authentication**: No server-side sessions
- **HS256 signing**: Industry-standard HMAC-SHA256
- **Configurable credentials**: Username/password via environment variables
- **Token expiration**: 60 minutes default (configurable)

## Protected Endpoints

- `GET /api/traffic/action` — Requires Bearer token
- `POST /api/traffic/action` — Requires Bearer token

## Public Endpoints

- `POST /api/auth/login` — Issue tokens (no auth required)
- `GET /api/traffic/health` — Health check (no auth required)
- `GET /swagger-ui/**` — API documentation (no auth required)

## Authentication Flow

1) **POST /api/auth/login** with credentials:

```json
  {
    "username": "admin",
    "password": "admin123"
  }
```

2) Receive Bearer token:

```json
  {
    "tokenType": "Bearer",
    "accessToken": "eyJhbGciOiJIUzI1NiJ9...",
    "expiresIn": 3600,
    "timestamp": 1710000000000
  }
```

3) Use token on protected endpoints:

```yaml
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...
```
