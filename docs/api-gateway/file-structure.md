# File Structure (Java API Gateway)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```text
java-api-gateway/
├── src/main/java/com/example/gateway/
│   ├── GatewayApplication.java
│   ├── controller/
│   │   ├── TrafficController.java
│   │   └── AuthController.java
│   ├── config/
│   │   ├── SecurityConfig.java
│   │   ├── OpenApiConfig.java
│   │   └── WebConfig.java
│   ├── security/
│   │   ├── JwtService.java
│   │   └── JwtAuthenticationFilter.java
│   ├── service/
│   │   └── RlInferenceClient.java
│   └── dto/
│       ├── LoginRequest.java
│       ├── LoginResponse.java
│       ├── TrafficActionResponse.java
│       ├── TrafficSignalState.java
│       └── ErrorResponse.java
├── src/main/resources/
│   ├── application.yml
│   └── application-prod.yml
├── pom.xml
├── Dockerfile
└── README.md
```
