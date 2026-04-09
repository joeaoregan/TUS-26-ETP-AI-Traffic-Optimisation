# File Structure (Python Inference Service)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
rl-inference-service/
├── app/
│   ├── main.py                 # FastAPI application & inference logic
│   ├── templates/
│   │   └── index.html          # Landing page
│   └── static/                 # Static assets (logo, favicon)
├── trained_models/
│   └── agent.th                # Trained MAPPO model weights
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```
