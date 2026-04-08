
# Quick Reference

## Starting Fresh

1. `python select_model.py` - Select and copy model
2. `start.bat` (Windows) or `./start.sh` (Linux) - Start services
3. `python test_api.py` - Run tests
4. `curl http://localhost:8080/api/traffic/action` - Make predictions

## Stopping Services

```bash
docker-compose down
```

## Viewing Logs

```bash
docker-compose logs rl-inference    # Python service
docker-compose logs java-gateway    # Java service
docker-compose logs -f              # All services, follow mode
```

## Restarting with New Model

```bash
docker-compose down
python select_model.py              # Choose new model
docker-compose up --build
```
