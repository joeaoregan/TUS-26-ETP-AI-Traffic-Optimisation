# File Structure (SUMO Traffic Simulator)

[Overall Project Structure](../system-architecture/project-structure.md)

---

```
SUMO/
├── osm.net.xml.gz                           # Road network (OpenStreetMap → netconvert)
├── osm.sumocfg                              # Main simulation configuration file
├── town_routes.rou.xml                      # 7 routes with time-varying hourly flows (TII data)
├── tii_flows.xml                            # Vehicle type definitions (placeholder)
├── tii_hourly_traffic.csv                   # Source TII vehicle count data (E/W entry points)
├── osm.view.xml                             # GUI display settings (visual scheme, speed)
├── osm_bbox.osm.xml.gz                      # Raw OpenStreetMap export (reference, not used by SUMO)
├── osm.netccfg                              # netconvert configuration (left-hand traffic, TLS setup)
├── run.bat                                  # One-click launcher (sumo-gui with osm.sumocfg)
├── Simulations/
│   └── Base/                                # Baseline simulation scenario
│       └── [custom scenario configs]
├── Results/
│   ├── Base/
│   │   ├── edgeData.xml                     # Per-edge hourly statistics (main LSTM training data)
│   │   ├── tripinfos.xml                    # Per-vehicle trip statistics
│   │   ├── stats.xml                        # Overall simulation summary
│   │   └── sumo.log                         # Simulation execution log
│   └── MAPPO/
│       ├── edgeData.xml                     # Output from MAPPO RL training run (sample)
│       ├── tripinfos.xml
│       └── stats.xml
└── [other SUMO auxiliary files]
```

---

## Core Simulation Files

| File | Purpose |
|------|---------|
| `osm.net.xml.gz` | Road network topology (compressed). Source of truth for streets, junctions, traffic signals. |
| `osm.sumocfg` | Main config: input files, simulation duration (0–43200s = 12h), output formats, TLS settings. |
| `town_routes.rou.xml` | 7 predefined routes with 12 hourly flow slots each. Routes derived from TII vehicle counts. |
| `tii_flows.xml` | Vehicle type definitions (currently minimal). Could be extended for different vehicle classes. |
| `osm.view.xml` | GUI settings: visual scheme (real-world), simulation speed (20ms delay). |

---

## Network Generation

| File | Purpose |
|------|---------|
| `osm_bbox.osm.xml.gz` | Raw OpenStreetMap export for Athlone bounding box. Reference only; used to generate osm.net.xml.gz. |
| `osm.netccfg` | `netconvert` configuration: left-hand traffic, actuated TLS, street name output. |

Command to regenerate network:
```bash
netconvert --configuration osm.netccfg -o osm.net.xml.gz
```

---

## Simulation Output

Generated on each simulation run in `Results/Base/` (or `Results/MAPPO/` for RL training):

| File | Contents | Usage |
|------|----------|-------|
| `edgeData.xml` | Per-edge hourly statistics: volume, speed, occupancy, wait time | **LSTM training data** |
| `tripinfos.xml` | Per-vehicle trip metrics: departure, arrival, duration, route length | Validation, travel time analysis |
| `stats.xml` | Aggregate summary: total vehicles, network-wide congestion | Performance evaluation |
| `sumo.log` | Execution log with warnings/errors | Debugging |

---

## Sample Data Structure (edgeData.xml)

```xml
<meandata xmlns:xsi="...">
    <interval begin="0.00" end="3600.00" id="hourly_edges">
        <edge id="-1018300044#0" 
              sampledSeconds="12.58" 
              traveltime="0.66" 
              density="0.18" 
              occupancy="0.09" 
              waitingTime="0.00" 
              timeLoss="..." />
        <!-- Repeat for all edges in network -->
    </interval>
</meandata>
```

---

## Route Configuration

The `town_routes.rou.xml` defines 7 routes with traffic split:

**West Entry (Bali side) — 3 routes:**
- `bali-bali-goldenIsland`
- `bali-bali-long`
- `bali-shannon-short`

**East Entry (B&Q side) — 4 routes:**
- `bAndQ-shannon-orenge`
- `bAndQ-bAndq-orenge`
- `bAndQ-bAndQ-long`
- `bAndQ-shannon-long`

Each route contains 12 hourly flow slots (one per hour) derived from TII traffic counts.

---

## Integration Points

- **LSTM Service**: Consumes `Results/Base/edgeData.xml` for training data
- **RL Training**: Simulation runs managed by EPyMARL with `osm.sumocfg`
- **TraCI (Future)**: Traffic signals can be controlled live via Python TraCI API