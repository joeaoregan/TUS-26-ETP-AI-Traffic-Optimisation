# File Structure (SUMO Traffic Simulator)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
SUMO/
├── osm.net.xml.gz              # Road network (OpenStreetMap derived)
├── osm.sumocfg                 # Main simulation configuration
├── town_routes.rou.xml         # 7 predefined routes with hourly flows
├── tii_flows.xml               # Vehicle type definitions (placeholder)
├── osm.view.xml                # GUI display settings
├── tii_hourly_traffic.csv      # Source TII vehicle count data
├── osm_bbox.osm.xml.gz         # Raw OSM export (reference)
├── osm.netccfg                 # Network converter configuration
├── run.bat                     # One-click launcher
├── Simulations/
│   └── Base/                   # Baseline simulation scenario
└── results/
    └── Base/                   # Output files directory
```