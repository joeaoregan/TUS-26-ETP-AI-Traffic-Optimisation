# API Endpoints

## Traffic Inference

!!! success "POST `/predict_action`"
    Predict the next optimal green phase for a specific junction.

    **Request Body:**
    ``` json
    {
      "junction_id": "300839359",
      "obs_data": [0.0, 1.0, 1.0, 0.12, 0.33, 0.41, 0.22, 0.55]
    }
    ```

    **Response (200):**
    ``` json
    {
      "junction_id": "300839359",
      "action": 1,
      "confidence": 0.87
    }
    ```

    **Parameters:**  

    - `junction_id` (string, required): One of the 5 known junction IDs  
    - `obs_data` (array of floats, required): Local observation vector  
      - Smaller observations are automatically zero-padded to 19 floats  
      - Maximum size: 19 floats  

    **Errors:**  

    - `404`: Unknown junction ID  
    - `400`: Observation size exceeds 19 floats  
    - `503`: Model not loaded  

    **Hidden State Management:**  

    - Each call updates and persists the GRU hidden state for that junction  
    - Call `POST /reset_hidden` at the start of each new simulation run  

!!! success "POST `/reset_hidden`"
    Reset GRU hidden states for all junctions. **Call at the start of each new simulation run.**

    **Request Body:** (empty)

    **Response (200):**
    ``` json
    {
      "status": "ok",
      "message": "Hidden states reset for all junctions"
    }
    ```

## System Health & Information
!!! note "GET `/health`"
    Service health check.

    **Response (200):**    
    ``` json
    {
      "status": "healthy",
      "model_loaded": true,
      "junctions": [
        "joinedS_265580996_300839357",
        "300839359",
        "265580972",
        "1270712555",
        "8541180897"
      ]
    }
    ```

    **Status Values:**

    - `healthy`: Model loaded and ready  
    - `no_model`: Service running but model not loaded  
    - `unhealthy`: Service error  

!!! note "GET `/model_info`"
    Get detailed information about the loaded MAPPO model.

    **Response (200):**
    ``` json
    {
      "architecture": "RNNAgent (GRU)",
      "input_shape": 24,
      "hidden_dim": 128,
      "n_actions": 4,
      "n_agents": 5,
      "obs_agent_id": true,
      "junctions": {
        "joinedS_265580996_300839357": {
          "agent_index": 0,
          "avail_actions": [1, 1, 1, 1],
          "valid_actions": 4
        },
        "300839359": {
          "agent_index": 1,
          "avail_actions": [1, 1, 0, 0],
          "valid_actions": 2
        }
      }
    }
    ```

## Navigation

!!! note "GET `/`"
    HTML landing page with links to documentation, status checks, and the API Gateway.

    **Response**: HTML page with navigation links

!!! note "GET `/docs`"
    FastAPI Swagger UI (auto-generated from OpenAPI schema).

    **Response**: Interactive API documentation