# 11. Architecture Decision Rationale

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Java Gateway** | Spring Boot | Enterprise-grade framework, excellent REST support, easy testing |
| **Python Service** | FastAPI | High performance, automatic API documentation, great async support |
| **ML Library** | stable-baselines3 | Industry standard for PPO, well-tested, robust |
| **Containerization** | Docker | Consistent deployment, easy scaling, isolated environments |
| **Communication** | REST/JSON | Universal, stateless, easy to monitor, language-agnostic |
| **Data Format** | JSON | Human-readable, widely supported, easy serialization |
