# 12. Performance Characteristics

### **Latency Breakdown** (typical)

```
Total Request Time: ~100-200ms

┌─────────────────────────────────────────────────────┐
│ Total: ~150ms                                       │
├─────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐             │
│ │ Java Gateway: ~20ms                 │             │
│ │ - Parse request: 2ms                │             │
│ │ - Validate data: 3ms                │             │
│ │ - HTTP call: 10ms                   │             │
│ │ - Response building: 5ms            │             │
│ └─────────────────────────────────────┘             │
│ ┌─────────────────────────────────────┐             │
│ │ Network: ~10-30ms                   │             │
│ │ - Request transmission: 5ms         │             │
│ │ - Response transmission: 5ms        │             │
│ │ - Latency: 0-20ms                   │             │
│ └─────────────────────────────────────┘             │
│ ┌─────────────────────────────────────┐             │
│ │ Python Service: ~80-120ms           │             │
│ │ - Request parsing: 5ms              │             │
│ │ - Model prediction: 70-100ms        │             │
│ │ - Response formatting: 5ms          │             │
│ └─────────────────────────────────────┘             │
└─────────────────────────────────────────────────────┘
```

### **Throughput** (requests per second)

- **Single instance:** 10-50 RPS (requests per second)
- **With horizontal scaling:** Linear increase with load balancing
- **Bottleneck:** Python model inference (70-100ms per prediction)

### **Resource Usage**

| Service | CPU | Memory | Disk |
|---------|-----|--------|------|
| Java Gateway | 0.1-0.2 cores | 512 MB | 100 MB |
| Python Service | 0.5-1.0 cores | 1-2 GB | 200 MB + model size |
| Model Storage | N/A | N/A | 50-500 MB per model |
