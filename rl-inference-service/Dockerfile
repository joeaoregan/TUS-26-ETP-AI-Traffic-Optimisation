# Stage 1: build dependencies
FROM python:3.9-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc g++ build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    --target /app/packages -r requirements.txt

# Stage 2: runtime image
FROM python:3.9-slim

WORKDIR /app

# Only curl needed at runtime (healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /app/packages /app/packages
ENV PYTHONPATH=/app/packages

# Copy application code
COPY app/ .

EXPOSE 8000

ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV MAPPO_AGENT_PATH=/app/trained_models/agent.th

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
