# SUMO Traffic Simulation — Athlone Network

![TUS](https://img.shields.io/badge/TUS-2026-black?style=flat-square&logo=data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iMTU3LjU1OTM2bW0iCiAgIGhlaWdodD0iMjA1LjE3MTE2bW0iCiAgIHZpZXdCb3g9IjAgMCAxNTcuNTU5MzYgMjA1LjE3MTE2IgogICB2ZXJzaW9uPSIxLjEiCiAgIGlkPSJzdmcxIgogICB4bWw6c3BhY2U9InByZXNlcnZlIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxzb2RpcG9kaTpuYW1lZHZpZXcKICAgICBpZD0ibmFtZWR2aWV3MSIKICAgICBwYWdlY29sb3I9IiNmZmZmZmYiCiAgICAgYm9yZGVyY29sb3I9IiMwMDAwMDAiCiAgICAgYm9yZGVyb3BhY2l0eT0iMC4yNSIKICAgICBpbmtzY2FwZTpzaG93cGFnZXNoYWRvdz0iMiIKICAgICBpbmtzY2FwZTpwYWdlb3BhY2l0eT0iMC4wIgogICAgIGlua3NjYXBlOnBhZ2VjaGVja2VyYm9hcmQ9IjAiCiAgICAgaW5rc2NhcGU6ZGVza2NvbG9yPSIjZDFkMWQxIgogICAgIGlua3NjYXBlOmRvY3VtZW50LXVuaXRzPSJtbSI+PGlua3NjYXBlOnBhZ2UKICAgICAgIHg9IjAiCiAgICAgICB5PSIwIgogICAgICAgd2lkdGg9IjE1Ny41NTkzNiIKICAgICAgIGhlaWdodD0iMjA1LjE3MTE2IgogICAgICAgaWQ9InBhZ2UyIgogICAgICAgbWFyZ2luPSIwIgogICAgICAgYmxlZWQ9IjAiIC8+PC9zb2RpcG9kaTpuYW1lZHZpZXc+PGRlZnMKICAgICBpZD0iZGVmczEiPjxzdHlsZQogICAgICAgaWQ9InN0eWxlMSI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48c3R5bGUKICAgICAgIGlkPSJzdHlsZTEtNCI+LmNscy0xe2ZpbGw6I2EzOTQ2MTt9PC9zdHlsZT48L2RlZnM+PGcKICAgICBpbmtzY2FwZTpsYWJlbD0iTGF5ZXIgMSIKICAgICBpbmtzY2FwZTpncm91cG1vZGU9ImxheWVyIgogICAgIGlkPSJsYXllcjEiCiAgICAgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMjA4LjE2MDkzLDQ4Ljg3NTE2MikiPjxnCiAgICAgICBpZD0iQXJ0d29yayIKICAgICAgIHRyYW5zZm9ybT0ibWF0cml4KDAuMjY0NTgzMzMsMCwwLDAuMjY0NTgzMzMsLTIwOC4xNjA5NCwtNDguODc1MTU4KSI+PHBhdGgKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICBkPSJNIDU5NS40OCwwIEggNDc2LjM4IFYgNTguNTIgSCAzNTcuMyBWIDAgSCAyMzguMiBWIDU4LjUyIEggMTE5LjEgViAwIEggMCB2IDM1Ny4yOSBoIDExOS4xIGEgMTc4LjY0LDE3OC42NCAwIDEgMSAzNTcuMjgsMCBoIDExOS4wNiB6IgogICAgICAgICBpZD0icGF0aDEiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSI0NzYuMzgiCiAgICAgICAgIHk9IjcxNS45MDAwMiIKICAgICAgICAgd2lkdGg9IjExOS4xIgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3QxIiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNzE1LjkwMDAyIgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDIiCiAgICAgICAgIHg9IjAiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB5PSI1OTYuNzk5OTkiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSI1OS41NDk5OTkiCiAgICAgICAgIGlkPSJyZWN0MyIKICAgICAgICAgeD0iMCIgLz48cmVjdAogICAgICAgICBjbGFzcz0iY2xzLTEiCiAgICAgICAgIHg9IjQ3Ni4zOTk5OSIKICAgICAgICAgeT0iNTk2Ljc5OTk5IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iNTkuNTQ5OTk5IgogICAgICAgICBpZD0icmVjdDQiIC8+PHJlY3QKICAgICAgICAgY2xhc3M9ImNscy0xIgogICAgICAgICB4PSIxMTkuMSIKICAgICAgICAgeT0iNTM3LjI1IgogICAgICAgICB3aWR0aD0iMzU3LjI5OTk5IgogICAgICAgICBoZWlnaHQ9IjU5LjU0OTk5OSIKICAgICAgICAgaWQ9InJlY3Q1IiAvPjxwb2x5Z29uCiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgcG9pbnRzPSI0NzYuMzksNjU2LjM1IDExOS4xLDY1Ni4zNSAxMTkuMSw3MTUuOSAyMzguMiw3MTUuOSAyMzguMiw3NzUuNDUgMzU3LjI5LDc3NS40NSAzNTcuMjksNzE1LjkgNDc2LjM5LDcxNS45ICIKICAgICAgICAgaWQ9InBvbHlnb241IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeD0iNDc2LjM5OTk5IgogICAgICAgICB5PSI0MTguMTYiCiAgICAgICAgIHdpZHRoPSIxMTkuMSIKICAgICAgICAgaGVpZ2h0PSIxMTkuMSIKICAgICAgICAgaWQ9InJlY3Q2IiAvPjxyZWN0CiAgICAgICAgIGNsYXNzPSJjbHMtMSIKICAgICAgICAgeT0iNDE4LjE2IgogICAgICAgICB3aWR0aD0iMTE5LjEiCiAgICAgICAgIGhlaWdodD0iMTE5LjEiCiAgICAgICAgIGlkPSJyZWN0NyIKICAgICAgICAgeD0iMCIgLz48L2c+PC9nPjwvc3ZnPgo=)
![Module](https://img.shields.io/badge/Module-Engineering%20Team%20Project-blue?style=flat-square)
![Topic](https://img.shields.io/badge/Topic-AI%20Traffic%20Optimisation-blue?style=flat-square)

## Overview

A traffic simulation of a local road network built using [Eclipse SUMO](https://sumo.dlr.de/) v1.26.0. The simulation runs 7 predefined routes through the town network for a 12-hour period using real-world OSM map data.

---

## Requirements

- [Eclipse SUMO](https://sumo.dlr.de/docs/Downloads.php) v1.26.0 or later
- Python 3.x
- `SUMO_HOME` environment variable set (e.g. `C:\Program Files (x86)\Eclipse\Sumo`)
- Python packages: `pandas`, `beautifulsoup4` (only needed for data extraction scripts)

---

## Running the Simulation

```bat
run.bat
```

This launches `sumo-gui` with the main configuration file `osm.sumocfg`.

---

## How the Simulation Works

The active route configuration in `osm.sumocfg` is:

```xml
<route-files value="tii_flows.xml,town_routes.rou.xml"/>
```

- `town_routes.rou.xml` is the single active source of traffic. It defines 7 fixed routes with time-varying hourly flows derived from TII counts. Each route contains 12 hourly flow slots covering 07:00–19:00.
- Route split (new):
	- West entry (Bali side) is split across 3 routes:
		- bali-bali-goldenIsland
		- bali-bali-long
		- bali-shannon-short
	- East entry (B&Q side) is split across 4 routes:
		- bAndQ-shannon-orenge
		- bAndQ-bAndq-orenge
		- bAndQ-bAndQ-long
		- bAndQ-shannon-long
- `tii_flows.xml` is loaded but currently contains only a vehicle type definition and contributes no vehicles. All traffic originates from `town_routes.rou.xml`.

---

## Core Files (required to run the simulation)

| File | Purpose |
|------|---------|
| `osm.net.xml.gz` | The road network generated from OpenStreetMap data. The main network file used by SUMO. |
| `osm.sumocfg` | The main SUMO simulation configuration. Defines input files, simulation time (0–43200 s), output files, routing and TLS settings. |
| `town_routes.rou.xml` | Defines the 7 predefined routes with hourly time-varying flows derived from TII traffic counts. West counts are distributed across the 3 Bali routes; East counts are distributed across the 4 B&Q routes. 12 flow slots per route (one per hour, 07:00–19:00). |
| `tii_flows.xml` | Currently a placeholder. Contains only a `car` vehicle type definition. No flows are active. Loaded by SUMO but contributes vehicles to the simulation. |
| `tii_hourly_traffic.csv` | Source of the hourly East/West vehicle counts used to generate the flow rates in `town_routes.rou.xml`. Not read directly by SUMO — data was used to populate the flow values. |
| `osm.view.xml` | GUI display settings for `sumo-gui`. Sets the visual scheme to "real world" and a 20 ms simulation delay. |
| `run.bat` | One-click launcher. Runs `sumo-gui -c osm.sumocfg`. |

---

## Source & Reference Data

| File | Purpose |
|------|---------|
| `osm_bbox.osm.xml.gz` | Raw OpenStreetMap export for the bounding box area. Source input used by `netconvert` to build `osm.net.xml.gz`. |
| `osm.netccfg` | `netconvert` configuration used to convert the OSM data into the SUMO network. Enables left-hand traffic, actuated traffic lights, and street name output. |

---

## Simulation Output Files (generated on run)

| File | Purpose |
|------|---------|
| `edgeData.xml` | Per-edge traffic statistics (volume, speed, occupancy) collected every hour during simulation. |
| `tripinfos.xml` | Per-vehicle trip statistics (departure time, arrival time, duration, route length). |
| `stats.xml` | Overall simulation statistics summary. |

---
