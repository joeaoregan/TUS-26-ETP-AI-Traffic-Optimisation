# System Architecture

## Architecture Diagram

```code title="System Architecture"
           ┌──────────────────────────────────┐
           │         CLIENT LAYER          │
           │  Web • Mobile • External API  │
           └─────────────────┬────────────────┘
                           │
                           │ HTTPS (TLS 1.3)
                           │
         ┌───────────────────▼──────────────────┐
         │  JAVA API GATEWAY (Port 8080)     │
         │       Spring Boot 3.2.3           │
         ├──────────────────────────────────────┤
         │  • JWT Authentication (HS256)     │
         │  • Request Validation             │
         │  • Fallback Logic (RED signal)    │
         │  • Circuit Breaker Pattern        │
         └───────────────────┬──────────────────┘
                           │
                ┌───────────┴─────────────┐
                │                       │
    ┌────────────▼────────┐   ┌────────────▼────────────┐
    │  HEALTH CHECK     │   │  PREDICTION REQUESTS  │
    │  /health          │   │  /traffic/action      │
    └─────────────────────┘   └─┬───────────────────────┘
                              │
                  ┌────────────▼────────────┐
                  │ INFERENCE SERVICE     │
                  │  (Port 8000)          │
                  │  Python/FastAPI       │
                  ├─────────────────────────┤
                  │ • MAPPO RL Model      │
                  │ • 5-Junction Support  │
                  │ • GRU State Mgmt      │
                  │ • Action Masking      │
                  └────────────┬────────────┘
                              │
                ┌──────────────┴────────────┐
                │                         │
    ┌────────────▼──────────┐   ┌────────────▼────────────┐
    │  LSTM PREDICTOR     │   │  ACTION SELECTION     │
    │  (Port 8001)        │   │  (MAPPO Output)       │
    │  Python/FastAPI     │   │                       │
    ├───────────────────────┤   │ Actions:              │
    │ • Time-series LSTM  │   │ 0: RED                │
    │ • 15-min Forecast   │   │ 1: YELLOW             │
    │ • MAE < 10%         │   │ 2: GREEN              │
    │ • Data Pipeline     │   │ 3: GREEN_EXTENDED     │
    └───────────────────────┘   └────────────┬────────────┘
                                          │
                                          │ Signal State
                                          │
                              ┌────────────▼────────────┐
                              │  RESPONSE TO CLIENT   │
                              │ {                     │
                              │   action: 0-3,        │
                              │   signalState: "RED", │
                              │   confidence: 0.87    │
                              │ }                     │
                              └─────────────────────────┘
```

## Overview

The AI Traffic Control API is a distributed, microservices-based system designed to provide real-time traffic signal control recommendations using trained Reinforcement Learning (RL) models.

---

## 🗂️ Project Structure

Start here to understand the codebase organization:
- **[Project Structure](project-structure.md)** — Complete directory layout and file descriptions

---

## 📚 Conceptual Understanding

Build foundational knowledge about the system design:

1. **[High-Level Overview](high-level.md)** — Bird's-eye view of the architecture
2. **[System Components](system-components.md)** — Key services and their responsibilities
3. **[Request-Response Flow](request-response-flow.md)** — How requests move through the system

---

## 🔄 Data & Processing

Understand how data flows and is processed:

4. **[Data Flow Through System](data-flow-through-system.md)** — Complete data journey from input to output
5. **[Detailed Internal Flow - Action Prediction](detailed-internal-flow.md)** — Deep dive into prediction logic
6. **[Model Loading & Caching Strategy](model-loading-and-caching-strategy.md)** — How models are initialized and cached

---

## 🔗 Workflows & Protocols

Learn about complete workflows and inter-service communication:

7. **[Complete End-to-End Workflow](complete-end-to-end-workflow.md)** — Full lifecycle from client request to response
8. **[Inter-Service Communication Protocol](inter-service-communication-protocol.md)** — How services talk to each other
9. **[Error Handling Flow](error-handling-flow.md)** — Exception handling and fallback mechanisms

---

## 🚀 Operations & Deployment

Learn how the system runs in production:

10. **[Deployment Architecture](deployment-architecture.md)** — Cloud deployment setup and infrastructure
11. **[Deployment Patterns](deployment-patterns.md)** — Deployment strategies and best practices
12. **[Monitoring & Observability Points](monitoring-and-observability-points.md)** — Logging, metrics, and health checks

---

## 🎯 Design & Optimization

Understand design decisions and optimization considerations:

13. **[Architecture Decision Rationale](architecture-decision-rationale.md)** — Why key decisions were made
14. **[Security Architecture](security-architecture.md)** — Security mechanisms and JWT implementation
15. **[Performance Characteristics](performance-characteristics.md)** — Latency, throughput, and performance metrics
16. **[Scalability Considerations](scalability-considerations.md)** — How the system scales and handles load

---

## Quick Navigation

**For different audiences:**

- **👤 New to the project?** Start with [High-Level Overview](high-level.md) → [System Components](system-components.md)
- **🛠️ Setting up locally?** See [Deployment Architecture](deployment-architecture.md) + Setup guides in the nav
- **🔍 Debugging an issue?** Check [Error Handling Flow](error-handling-flow.md) → [Monitoring & Observability Points](monitoring-and-observability-points.md)
- **📈 Optimizing performance?** Read [Performance Characteristics](performance-characteristics.md) → [Scalability Considerations](scalability-considerations.md)
- **🔐 Security review?** Start with [Security Architecture](security-architecture.md)