# Architecture (SUMO Traffic Simulator)

## Technology Stack

- **Simulator**: Eclipse SUMO v1.26.0 (Simulation of Urban Mobility)
- **Network Source**: OpenStreetMap (OSM) data
- **Network Converter**: SUMO netconvert utility
- **Simulation Duration**: 12 hours (0–43200 seconds)
- **Traffic Data Source**: TII (Traffic Information Ireland) vehicle counts
- **Output Format**: XML (edgeData.xml, tripinfos.xml, stats.xml)

## Network Architecture

**Road Network** (`osm.net.xml.gz`)

- Generated from OpenStreetMap bounding box data for Athlone
- Contains all streets, junctions, and traffic signal timings
- Compressed format for storage efficiency
- Left-hand traffic configuration (Ireland)

**Traffic Signals**

- Actuated traffic light control via SUMO's built-in TLS engine
- 5 major junctions with adaptive signal timing
- Junction IDs: `joinedS_265580996_300839357`, `300839359`, `265580972`, `1270712555`, `8541180897`

## File Structure

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

## Traffic Flow Configuration

**Route Definition** (`town_routes.rou.xml`)

- Defines 7 fixed routes through the Athlone network
- Each route contains 12 hourly flow slots (one per hour of simulation)
- Time-varying flows based on real TII traffic counts

**Route Split**:

- **West Entry (Bali side)**: 3 routes
  - `bali-bali-goldenIsland`
  - `bali-bali-long`
  - `bali-shannon-short`

- **East Entry (B&Q side)**: 4 routes
  - `bAndQ-shannon-orenge`
  - `bAndQ-bAndq-orenge`
  - `bAndQ-bAndQ-long`
  - `bAndQ-shannon-long`

## Simulation Configuration

**File**: `osm.sumocfg`

Key settings:

- **Network**: `osm.net.xml.gz`
- **Routes**: `tii_flows.xml`, `town_routes.rou.xml`
- **Simulation Time**: 0 to 43200 seconds (12 hours)
- **Timestep**: 1 second
- **Output Files**: 
  - `edgeData.xml` — Hourly statistics per edge
  - `tripinfos.xml` — Per-vehicle trip data
  - `stats.xml` — Overall simulation summary

**GUI Settings** (`osm.view.xml`):

- Visual scheme: "Real World"
- Simulation delay: 20ms
- Enables visual monitoring during runs

## Data Flow

```
OpenStreetMap Data
    ↓
osm_bbox.osm.xml.gz (raw OSM export)
    ↓
netconvert (with osm.netccfg)
    ↓
osm.net.xml.gz (SUMO network)
    ↓
SUMO Simulation Engine
    ↓
town_routes.rou.xml (7 routes × 12 hourly flows)
    ↓
Vehicles spawn and traverse network
    ↓
Output Files Generated
├── edgeData.xml (per-edge statistics)
├── tripinfos.xml (per-vehicle statistics)
└── stats.xml (simulation summary)
```

## Integration with Other Systems

**LSTM Traffic Predictor**

- Consumes `edgeData.xml` output
- Uses historical vehicle counts, speeds, and occupancy
- Trains LSTM model for 15-minute forecasting

**RL Inference Service**

- Receives live junction observations from SUMO (via TraCI future integration)
- Predicts optimal signal timings
- Feeds decisions back to SUMO for adaptive control

**API Gateway**

- Provides HTTP interface to retrieve SUMO data
- Orchestrates requests from simulation to inference services