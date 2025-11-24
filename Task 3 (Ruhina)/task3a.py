import os, sys

#
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, 'clrsPython')

#
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Chapter 20'))
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Chapter 10'))
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Utility functions'))

# Import bfs
from bfs import bfs

# Small example with 5 stations
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C'],
    'C': ['B', 'E'],
    'D': ['A', 'E'],
    'E': ['C', 'D']
}

# BFS Function to find shortest path in terms of stops
def bfs_shortest_path(graph, start, goal):
    visited = set()
    queue = ([[start]])

    while queue:
        path = queue.pop()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None

# Run BFS
start_node = 'A'
end_node = 'E'
path = bfs_shortest_path(graph, start_node, end_node)

# Output
if path:
    print("Path from", start_node, "to", end_node, ":")
    print(" -> ".join(path))
    print("Number of stops:", len(path) - 1)
else:
    print("No path found from", start_node, "to", end_node)