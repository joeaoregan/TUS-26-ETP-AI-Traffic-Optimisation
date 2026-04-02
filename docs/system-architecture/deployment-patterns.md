# 16. Deployment Patterns

### **Development**
```
Local Machine
├── Java Gateway: localhost:8080
└── Python Service: localhost:8000
```

### **Testing**
```
Docker Compose (Single Host)
├── Java Gateway Container: 8080
└── Python Service Container: 8000
```

### **Production (Cloud)**
```
Kubernetes Cluster
├── Service Mesh (Istio)
├── Load Balancer
├── Java Gateway Pods (3+)
├── Python Service Pods (2+)
├── Model Persistent Volume
└── Monitoring Stack
```