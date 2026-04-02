# 📡 API Endpoints

## Python Service (Port 8000)

!!! note "GET /health"
    Service health status (lists controlled junctions)
!!! success "GET /predict_action"
    Predict action for a junction (requires junction_id + obs_data)
!!! success "GET /reset_hidden"
    Reset GRU hidden states (call at start of each simulation run)
!!! note "GET /model_info"
    MAPPO model details (architecture, junctions, action masks)
!!! note "GET /docs"
    Swagger UI documentation

## Java Gateway (Port 8080)

!!! note "GET /api/traffic/health"
    Service health status
!!! note "GET /api/traffic/action"
    Demo prediction (random junction, auto-generated observations)
!!! success "POST /api/traffic/action"
    Predict action (requires junctionId + observations)
!!! success "POST /api/traffic/reset"
    Reset MAPPO GRU hidden states

## LSTM Predictor Service (Port 8001)

!!! note "GET /health"
    Check if service is running  
    Response:  
    ```json
    {
        "status": "ok", 
        "model_loaded": true
    }
    ```

!!! success "POST /forecast"
    Predict traffic flow 15 minutes into future  
    
    Request:  
    ```json
    {
        "junction_id": "joinedS_265580996_300839357",
        "vehicle_counts": [45, 52, 48, 51, 49, ...],  # last 60 minutes
        "timestamp": 1234567890
    }
    ```    
    Response:  
    ```json
    {
        "junction_id": "joinedS_265580996_300839357",
        "forecast_15min": [55, 58, 62, 60],  # next 15 minutes
        "mae": 0.087,  # model's error estimate
        "timestamp": 1234567890
    }
    ```

!!! note "GET /model_info"
    Get details about loaded LSTM model  
    Response:  
    ```json
    {
        "architecture": "LSTM",
        "input_size": 60,
        "hidden_size": 64,
        "output_size": 15,
        "trained_on": "SUMO simulation data",
        "mae_target": 0.10
    }
    ```

## Examples

!!! note "GET /todo"
    Example of what GET would look like

!!! success "POST /todo"
    Example of what POST would look like

!!! warning "PUT /todo"
    Example of what PUT would look like

!!! danger "DELETE /todo"
    Example of what DELETE would look like
