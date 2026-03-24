## 🐛 Troubleshooting

### Services won't start
- [x] Check Docker is installed: `docker --version`
- [x] Verify ports 8000, 8080 are available
- [x] Check logs: `docker-compose logs`

### Model loading fails
- [x] Ensure model file exists: `rl-inference-service/app/trained_models/model.zip`
- [x] Rerun selector: `python select_model.py`
- [x] Check Python logs: `docker-compose logs rl-inference`

### Predictions return errors
- [x] Verify service health: `curl http://localhost:8080/api/traffic/health`
- [x] Check observation dimensions (should be 10 floats)
- [x] View logs: `docker-compose logs`

---

## 📞 Issues

For issues:

- [x] Check service logs: `docker-compose logs service_name`
- [x] Verify services are running: `docker-compose ps`
- [x] Test individual services: `curl http://localhost:8000/health`
- [x] Review [INDEX.md](../1_home/INDEX.md) (README.md) for detailed troubleshooting

---

## 📝 Notes

- Models are in `C:\Users\gemer\Sumo\my-network\Results\sweeps*`
- Default observation dimension: 10 features
- Actions are mapped to traffic signal states (RED, YELLOW, GREEN, GREEN_EXTENDED)
- Services communicate via Docker network (when containerized)
- All data is JSON-based for easy integration

---

**Created:** March 2026  

**Technology Stack:** 

- Python 3.9+
- FastAPI
- Java 17+
- Spring Boot 3.2
- Docker
- Docker Compose  

**Status:** Ready to use! ✓