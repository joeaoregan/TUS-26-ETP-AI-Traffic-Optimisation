"""
MAPPO inference API — 5-junction Irish town network.

Architecture (from training):
  - Shared RNNAgent: fc1(24→128) → GRUCell(128→128) → fc2(128→4)
  - Input per agent: obs_padded(19) + agent_id_onehot(5) = 24
  - Separate GRU hidden state maintained per junction between calls

Endpoints:
  POST /predict_action   — predict green phase for a junction
  POST /reset_hidden     — reset GRU hidden states (call at start of each sim run)
  GET  /health
  GET  /model_info
  GET  /                 — HTML landing page
"""

import logging
import os
from pathlib import Path
from typing import List, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ─── Junction config ───────────────────────────────────────────────────────────
TRAFFIC_LIGHTS = [
    "joinedS_265580996_300839357",
    "300839359",
    "265580972",
    "1270712555",
    "8541180897",
]

# Per-junction available actions (1=valid, 0=padded/invalid)
AVAIL_ACTIONS = {
    "joinedS_265580996_300839357": [1, 1, 1, 1],
    "300839359":                   [1, 1, 0, 0],
    "265580972":                   [1, 1, 0, 0],
    "1270712555":                  [1, 1, 0, 0],
    "8541180897":                  [1, 1, 0, 0],
}

AGENT_INDEX = {tl: i for i, tl in enumerate(TRAFFIC_LIGHTS)}

# Training hyperparams — must match mappo_sumo_v4.yaml
N_AGENTS   = 5
OBS_SHAPE  = 19   # max padded obs size (joinedS has 19)
N_ACTIONS  = 4    # max action size (joinedS has 4)
HIDDEN_DIM = 128


# ─── RNNAgent (matches EPyMARL rnn_agent.py exactly) ──────────────────────────
class RNNAgent(nn.Module):
    def __init__(self, input_shape: int, hidden_dim: int, n_actions: int):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.fc1 = nn.Linear(input_shape, hidden_dim)
        self.rnn = nn.GRUCell(hidden_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, n_actions)

    def init_hidden(self) -> torch.Tensor:
        return self.fc1.weight.new(1, self.hidden_dim).zero_()

    def forward(self, inputs: torch.Tensor, hidden_state: torch.Tensor):
        x = F.relu(self.fc1(inputs))
        h = self.rnn(x, hidden_state.reshape(-1, self.hidden_dim))
        logits = self.fc2(h)
        return logits, h


# ─── Pydantic schemas ──────────────────────────────────────────────────────────
class Observation(BaseModel):
    junction_id: str
    obs_data: List[float]


class PredictionResponse(BaseModel):
    junction_id: str
    action: int
    confidence: Optional[float] = None


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    status: str
    model_loaded: bool
    junctions: List[str]


# ─── Global state ──────────────────────────────────────────────────────────────
agent: Optional[RNNAgent] = None
hidden_states: dict = {}   # junction_id -> torch.Tensor [1, hidden_dim]


def _reset_all_hidden():
    """Reset GRU hidden states for all junctions (call at start of each sim run)."""
    global hidden_states
    if agent is None:
        return
    hidden_states = {tl: agent.init_hidden() for tl in TRAFFIC_LIGHTS}
    logger.info("Hidden states reset for all junctions")


def load_agent():
    global agent
    model_path = os.getenv("MAPPO_AGENT_PATH")
    if not model_path:
        raise RuntimeError("MAPPO_AGENT_PATH env var not set — point it to agent.th")
    if not Path(model_path).exists():
        raise RuntimeError(f"agent.th not found at {model_path}")

    input_shape = OBS_SHAPE + N_AGENTS  # 24

    agent = RNNAgent(input_shape=input_shape, hidden_dim=HIDDEN_DIM, n_actions=N_ACTIONS)
    state_dict = torch.load(model_path, map_location="cpu")
    agent.load_state_dict(state_dict)
    agent.eval()

    _reset_all_hidden()
    logger.info(
        "MAPPO agent loaded from %s  input=%d hidden=%d actions=%d",
        model_path, input_shape, HIDDEN_DIM, N_ACTIONS,
    )


# ─── FastAPI app ───────────────────────────────────────────────────────────────
tags_metadata = [
    {
        "name": "Traffic Inference",
        "description": "The core engine for RL-based traffic signal prediction.",
    },
    {
        "name": "System Health",
        "description": "Endpoints to monitor service status and model availability.",
    },
    {
        "name": "Navigation",
        "description": "Main landing pages and UI components.",
    },
]

app = FastAPI(
    title="RL Inference API — 5-Junction MAPPO",
    version="3.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Joe O'Regan, Edgars Peskaitis, Adam O Neill Mc Knight, David Claffey",
        "email": "A00258304@student.tus.ie",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Local development server"},
        {"url": "https://traffic-inference-service.onrender.com", "description": "Production Cloud server (Render)"},
    ],
    description="""<img src="static/logo.png" width="360" alt="AI Traffic Management System Logo" />
    <h2>Joe O'Regan, Edgars Peskaitis</h2>
    <h2>Adam O Neill Mc Knight, David Claffey</h2>
    <h3>Overview</h3>
    <p>REST API for traffic signal control using MAPPO (Multi-Agent PPO) with shared GRU actor.
    Controls 5 junctions in the Athlone town network.</p>
    <p>Call <code>POST /reset_hidden</code> at the start of each new simulation run to reset GRU state.</p>""",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    try:
        load_agent()
        logger.info("Application startup completed successfully")
    except Exception as e:
        logger.error("Application startup failed: %s", e)
        raise


@app.get("/health", response_model=HealthResponse, tags=["System Health"])
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if agent is not None else "no_model",
        model_loaded=agent is not None,
        junctions=TRAFFIC_LIGHTS,
    )


@app.post("/predict_action", response_model=PredictionResponse, tags=["Traffic Inference"])
async def predict_action(observation: Observation):
    """
    Predict the next green phase for a junction.

    Request body:
      junction_id  — one of the 5 known junction IDs
      obs_data     — local observation vector (float[]):
                       [phase_one_hot..., min_green_flag, lane_queue_0, ...]
                     Sizes: joinedS=19, others=~8-10
                     (smaller obs are zero-padded to 19 internally)

    Response:
      action  — green phase index (int)
                joinedS: 0-3,  others: 0-1
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    junction_id = observation.junction_id
    if junction_id not in AGENT_INDEX:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown junction '{junction_id}'. Known: {TRAFFIC_LIGHTS}",
        )

    agent_idx = AGENT_INDEX[junction_id]

    obs = np.array(observation.obs_data, dtype=np.float32)
    if obs.size > OBS_SHAPE:
        raise HTTPException(
            status_code=400,
            detail=f"obs_data has {obs.size} values, expected <= {OBS_SHAPE}",
        )
    if obs.size < OBS_SHAPE:
        obs = np.pad(obs, (0, OBS_SHAPE - obs.size))

    # Append agent_id one-hot
    agent_id_onehot = np.zeros(N_AGENTS, dtype=np.float32)
    agent_id_onehot[agent_idx] = 1.0
    agent_input = np.concatenate([obs, agent_id_onehot])

    x = torch.tensor(agent_input, dtype=torch.float32).unsqueeze(0)
    h = hidden_states[junction_id]

    with torch.no_grad():
        logits, h_new = agent(x, h)

    hidden_states[junction_id] = h_new

    avail = torch.tensor(AVAIL_ACTIONS[junction_id], dtype=torch.float32)
    logits = logits.squeeze(0)
    logits[avail == 0] = -1e10
    probs = F.softmax(logits, dim=-1)

    action = int(probs.argmax().item())
    confidence = float(probs[action].item())

    logger.info(
        "junction=%s agent_idx=%d action=%d confidence=%.3f",
        junction_id, agent_idx, action, confidence,
    )

    return PredictionResponse(
        junction_id=junction_id,
        action=action,
        confidence=confidence,
    )


@app.post("/reset_hidden", tags=["Traffic Inference"])
async def reset_hidden():
    """
    Reset GRU hidden states for all junctions.
    Call this at the start of each new simulation run.
    """
    _reset_all_hidden()
    return {"status": "ok", "message": "Hidden states reset for all junctions"}


@app.get("/model_info", tags=["Traffic Inference"])
async def get_model_info():
    """Get information about the loaded MAPPO model."""
    if agent is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {
        "architecture": "RNNAgent (GRU)",
        "input_shape": OBS_SHAPE + N_AGENTS,
        "hidden_dim": HIDDEN_DIM,
        "n_actions": N_ACTIONS,
        "n_agents": N_AGENTS,
        "obs_agent_id": True,
        "junctions": {
            tl: {
                "agent_index": AGENT_INDEX[tl],
                "avail_actions": AVAIL_ACTIONS[tl],
                "valid_actions": sum(AVAIL_ACTIONS[tl]),
            }
            for tl in TRAFFIC_LIGHTS
        },
    }


@app.get("/", response_class=HTMLResponse, tags=["Navigation"])
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("API_RELOAD", "false").lower() == "true",
    )
