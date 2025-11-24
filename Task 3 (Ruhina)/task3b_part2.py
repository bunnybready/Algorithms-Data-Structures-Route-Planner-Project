import os, sys, csv

# Add clrsPython
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, 'clrsPython')

# Add directory
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Chapter 20'))
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Chapter 10'))
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Utility functions'))

# Import bfs from clrsPython
from bfs import bfs

# Read CSV file
csv_file = os.path.join(PROJECT_ROOT, 'data', 'London_Underground_data.csv')

data = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        data.append(row)

# Build the graph
graph = {}
for row in data:
    if len(row) < 3 or not row[1].strip() or not row[2].strip():
        continue

    station_a = row[1].strip()
    station_b = row[2].strip()

    if station_a not in graph:
        graph[station_a] = set()
    if station_b not in graph:
        graph[station_b] = set()

    graph[station_a].add(station_b)
    graph[station_b].add(station_a)

graph = {station: list(neighbors) for station, neighbors in graph.items()}

# BFS function
def bfs_shortest_path(graph, start_station, end_station):
    visited = set()
    queue = [[start_station]]

    while queue:
        current_path = queue.pop(0)
        current_station = current_path[-1]

        if current_station == end_station:
            return current_path

        if current_station not in visited:
            visited.add(current_station)
            for neighbor in graph[current_station]:
                queue.append(current_path + [neighbor])

    return None

# Testing Journeys
journeys = [
    ("Oxford Circus", "Piccadilly Circus"),
    ("Upminster", "Ealing Broadway")
]
for start, end in journeys:
    path = bfs_shortest_path(graph, start, end)
    if path:
        print(f"Route from {start} to {end}:")
        print(" -> ".join(path))
        print("Total stops:", len(path) - 1)
    else:
        print(f"No route found from {start} to {end}")
    print()

# Artificial Tube Network Generation
def generate_random_tube(n, max_neighbors=4):
    graph = {f"S{i}": set() for i in range(n)}
    for station in graph:
        num_connections = 1
        for _ in range(num_connections):
            neighbor = f"S{(int(station[1:]) + 1) % n}"
            if neighbor != station:
                graph[station].add(neighbor)
                graph[neighbor].add(station)
    return {s: list(neigh) for s, neigh in graph.items()}

# Time Measurement For BFS
def average_bfs_operations(graph, num_trials=50):
    stations = list(graph.keys())
    for i in range(num_trials):
        start = stations[i % len(stations)]
        end = stations[(i + len(stations) // 2) % len(stations)]
        bfs_shortest_path(graph, start, end)
    return num_trials