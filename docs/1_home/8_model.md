To use a different trained MAPPO model:

1. **Locate your checkpoint:**

   ```
   Results/mappo_sumo_v4/seed_<n>/models/<run_name>/<steps>/agent.th

   Example:
   - Results/mappo_sumo_v4/seed_42/models/.../2828160/agent.th
   ```

2. **Copy to trained_models directory:**

   ```bash
   cp "<source_path>/agent.th" "rl-inference-service/app/trained_models/agent.th"
   ```

3. **Rebuild and restart:**

   ```bash
   docker build -t rl-inference-service:2.0.0 ./rl-inference-service
   docker compose up -d
   ```

> **Note:** The model is an EPyMARL RNNAgent checkpoint (PyTorch `.th` file), not a Stable-Baselines3 `.zip`. Architecture: `fc1(24→128) → GRUCell(128→128) → fc2(128→4)`. Input shape = 24 (19 obs + 5 agent-id one-hot).
