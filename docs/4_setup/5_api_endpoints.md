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

## LSTM Predictor Service 

!!! note "GET /todo"
    Example of what GET would look like

!!! success "POST /todo"
    Example of what POST would look like

!!! warning "PUT /todo"
    Example of what PUT would look like

!!! danger "DELETE /todo"
    Example of what DELETE would look like
