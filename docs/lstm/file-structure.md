# File Structure (LSTM Traffic Predictor)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
lstm-predictor-service/
├── app/
│   ├── main.py                 # FastAPI application & LSTM inference logic
│   ├── data/
│   │   ├── loader.py           # SUMO edgeData.xml parser
│   │   └── preprocessor.py     # Data normalization and windowing
│   ├── models/
│   │   └── lstm_model.pt       # Trained LSTM model weights (future)
│   ├── templates/
│   │   └── index.html          # Landing page
│   └── static/                 # Static assets (logo, favicon)
├── trained_models/
│   └── lstm_traffic_forecast.pt # Trained LSTM checkpoint (future)
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```