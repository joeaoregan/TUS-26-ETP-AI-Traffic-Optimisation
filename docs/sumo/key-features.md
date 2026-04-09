# Key Features (SUMO Traffic Simulator)

[Feature List](../features.md#sumo-traffic-simulator-integration)

## Status

**Fully operational as a standalone simulator but not yet live-integrated with the RL control system.**

## Realistic Road Network

- **OpenStreetMap Integration**: Road network derived from actual OSM data for Athlone
- **Street-Level Detail**: All roads, junctions, and traffic signals from real geography
- **Left-Hand Traffic**: Configuration for Irish road standards

## Time-Varying Traffic Flows

- **Real-World Data**: Vehicle flows based on TII (Traffic Information Ireland) counts
- **Hourly Variation**: 12 hourly flow slots covering typical daily traffic patterns
- **7 Predefined Routes**: Captures major traffic movements through town (West Bali entry, East B&Q entry)

## Traffic Signal Management

- **Actuated Traffic Lights**: SUMO's built-in TLS engine for adaptive signal control
- **5 Major Junctions**: Full coverage of key intersections:
  - `joinedS_265580996_300839357` (complex multi-approach)
  - `300839359`, `265580972`, `1270712555`, `8541180897`
- **Future TraCI Integration**: Ready for live RL agent control

## Comprehensive Output Data

**edgeData.xml** — Per-edge hourly statistics:
- Vehicle volume (count)
- Average speed
- Occupancy rate
- Travel time

**tripinfos.xml** — Per-vehicle trip metrics:
- Departure and arrival times
- Trip duration
- Route length
- Waiting time

**stats.xml** — Aggregate simulation statistics:
- Total vehicles processed
- Network-wide congestion metrics
- Simulation performance

## Flexible Route Configuration

- Easily modifiable route definitions in XML
- Time-varying flows with hourly granularity
- Support for multi-leg journeys
- Vehicle type definitions for different classes

## GUI & Visualization

- **SUMO GUI**: Visual simulation monitoring in real-time
- **Customizable Display**: Real-world visual scheme, adjustable speed
- **One-Click Launch**: `run.bat` for easy simulation startup

## Data Foundation for ML

- Generates training data for LSTM forecasting model
- Provides ground truth for validation and testing
- Enables scenario testing (peak hours, incidents, etc.)
- Scalable to other traffic networks