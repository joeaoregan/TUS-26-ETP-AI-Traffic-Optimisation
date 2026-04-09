# edge-analysis.py
# Analyse edgeData.xml to understand traffic conditions on edges, focusing on density, occupancy, and waiting times.

import xml.etree.ElementTree as ET
import pandas as pd

# Parse edgeData.xml
tree = ET.parse('SUMO/Results/MAPPO/edgeData.xml')
root = tree.getroot()

edges_data = []

for interval in root.findall('interval'):
    interval_begin = float(interval.get('begin'))
    interval_end = float(interval.get('end'))
    
    for edge in interval.findall('edge'):
        edge_id = edge.get('id')
        density = float(edge.get('density', 0))
        occupancy = float(edge.get('occupancy', 0))
        waitingTime = float(edge.get('waitingTime', 0))
        timeLoss = float(edge.get('timeLoss', 0))
        
        edges_data.append({
            'edge_id': edge_id,
            'interval_begin': interval_begin,
            'interval_end': interval_end,
            'density': density,
            'occupancy': occupancy,
            'waitingTime': waitingTime,
            'timeLoss': timeLoss
        })

df = pd.DataFrame(edges_data)

print("=== Edge Data Overview ===")
print(f"Total edge-interval records: {len(df)}")
print(f"Unique edges: {df['edge_id'].nunique()}")
print(f"Time intervals: {df['interval_begin'].nunique()}")
print(f"\nDensity stats:")
print(df['density'].describe())
print(f"\nOccupancy stats:")
print(df['occupancy'].describe())
print(f"\nWaiting time stats:")
print(df['waitingTime'].describe())
print(f"\nTop 10 edges by average density:")
print(df.groupby('edge_id')['density'].mean().nlargest(10))