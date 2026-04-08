# 13. Scalability Considerations

### **Horizontal Scaling**

```mermaid
graph TB
    LB["Load Balancer<br/>nginx/haproxy"]
    
    subgraph Gateway["Java Gateway Fleet"]
        JG1["Instance 1"]
        JG2["Instance 2"]
        JG3["Instance N"]
    end
    
    subgraph Python["Python Service Fleet"]
        PS1["Instance 1"]
        PS2["Instance 2"]
        PS3["Instance N"]
    end
    
    Cache["Model Cache<br/>Shared Volume"]
    
    LB -->|Round Robin| JG1
    LB -->|Round Robin| JG2
    LB -->|Round Robin| JG3
    
    JG1 -->|Load Balanced| PS1
    JG2 -->|Load Balanced| PS2
    JG3 -->|Load Balanced| PS3
    
    PS1 -->|Read| Cache
    PS2 -->|Read| Cache
    PS3 -->|Read| Cache
    
    style LB fill:#ffeb3b
    style Cache fill:#e8f5e9
```

### **Vertical Scaling**

- Increase container memory (Python: 1GB → 4GB)
- Increase CPU allocation (Java: 1 core → 4 cores)
- Use GPU acceleration for Python service (CUDA-enabled Docker)
