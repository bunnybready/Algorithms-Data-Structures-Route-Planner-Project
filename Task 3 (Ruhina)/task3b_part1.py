import os, sys, random, time
import matplotlib.pyplot as plt

#
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CLRS_ROOT = os.path.join(PROJECT_ROOT, 'clrsPython')

#
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Chapter 20'))
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Chapter 10'))
sys.path.insert(0, os.path.join(CLRS_ROOT, 'Utility functions'))

# Import bfs
from clrsPython.Chapter_20.bfs import bfs

class Edge:
    def __init__(self, v):
        self.v = v
    def get_v(self):
        return self.v

class SimpleGraph:
    def __init__(self, g):
        self.g = g

    def get_card_V(self):
        return len(self.g)

    def get_adj_list(self, u):
        # return list of Edge objects
        return [Edge(v) for v in self.g[u]]

# Generate random tube-like graph
def generate_random_tube(n):
    graph = {i: [] for i in range(n)}

    for i in range(n - 1):
        graph[i].append(i + 1)
        graph[i + 1].append(i)

    for _ in range(n // 2):
        a, b = random.sample(range(n), 2)
        if b not in graph[a]:
            graph[a].append(b)
            graph[b].append(a)

    return graph

# Time BFS
def average_bfs_time(graph, runs=5):
    total = 0
    for _ in range(runs):
        start = random.randrange(len(graph))

        G = SimpleGraph(graph)

        t0 = time.time()
        bfs(G, start)
        total += time.time() - t0

    return total / runs

sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
avg_times = []

for n in sizes:
    graph = generate_random_tube(n)
    avg_time = average_bfs_time(graph)
    avg_times.append(avg_time)
    print(f"Network size {n}: average BFS time = {avg_time:.6f} seconds")

plt.plot(sizes, avg_times, marker='o')
plt.xlabel("Network size (n stations)")
plt.ylabel("Average BFS time (seconds)")
plt.title("Empirical BFS Performance")
plt.grid(True)
plt.savefig("task3b_performance_graph.png")