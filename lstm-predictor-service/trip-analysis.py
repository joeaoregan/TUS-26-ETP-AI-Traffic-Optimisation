# trip-analysis.py
# Analyse tripinfo.xml to understand trip durations, waiting times, and departure delays.

import xml.etree.ElementTree as ET
import pandas as pd

# Parse tripinfo.xml
tree = ET.parse('../SUMO/Results/MAPPO/tripinfo.xml')
root = tree.getroot()

trips = []
for trip in root.findall('tripinfo'):
    trips.append({
        'id': trip.get('id'),
        'depart': float(trip.get('depart')),
        'arrival': float(trip.get('arrival')),
        'departDelay': float(trip.get('departDelay')),
        'waitingTime': float(trip.get('waitingTime', 0)),
        'arrivalSpeed': float(trip.get('arrivalSpeed', 0)),
        'duration': float(trip.get('duration', 0))
    })

df = pd.DataFrame(trips)

print("=== Dataset Overview ===")
print(f"Total trips: {len(df)}")
print(f"Time range: {df['depart'].min():.0f}s to {df['arrival'].max():.0f}s")
print(f"\nWaiting time stats:")
print(df['waitingTime'].describe())
print(f"\nTrip duration stats:")
print(df['duration'].describe())
print(f"\nDeparture delay stats:")
print(df['departDelay'].describe())