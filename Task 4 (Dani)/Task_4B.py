import os
import random
import time
import math
import matplotlib.pyplot as plt


# Disjoint Set (Union-Find) for Kruskal
class DisjointSetNode:
    def __init__(self, key):
        self.key = key
        self.parent = self
        self.rank = 0


def make_set(x):
    return DisjointSetNode(x)


def find_set(x):
    if x.parent != x:
        x.parent = find_set(x.parent)
    return x.parent


def union(x, y):
    x_root = find_set(x)
    y_root = find_set(y)
    if x_root == y_root:
        return
    if x_root.rank < y_root.rank:
        x_root.parent = y_root
    else:
        y_root.parent = x_root
        if x_root.rank == y_root.rank:
            x_root.rank += 1


# Graph Classes
class Edge:
    def __init__(self, v, weight):
        self.v = v
        self.weight = weight

    def get_v(self):
        return self.v

    def get_weight(self):
        return self.weight


class AdjacencyListGraph:
    def __init__(self, n, directed=False, weighted=True):
        self.V = n
        self.directed = directed
        self.weighted = weighted
        self.adj_list = [[] for _ in range(n)]

    def insert_edge(self, u, v, weight=1):
        self.adj_list[u].append(Edge(v, weight))
        if not self.directed:
            self.adj_list[v].append(Edge(u, weight))

    def get_card_V(self):
        return self.V

    def get_adj_list(self, u):
        return self.adj_list[u]


# Kruskal's Algorithm
def kruskal(graph):
    V = graph.get_card_V()
    edges = []
    for u in range(V):
        for edge in graph.get_adj_list(u):
            v = edge.get_v()
            if u < v:  # avoid duplicates in undirected graph
                edges.append((u, v, edge.get_weight()))

    edges_sorted = sorted(edges, key=lambda x: x[2])
    forest = [make_set(v) for v in range(V)]
    mst_edges = []

    for u, v, w in edges_sorted:
        if find_set(forest[u]) != find_set(forest[v]):
            mst_edges.append((u, v, w))
            union(forest[u], forest[v])
        if len(mst_edges) == V - 1:
            break

    # Build MST graph
    mst_graph = AdjacencyListGraph(V, directed=False, weighted=True)
    for u, v, w in mst_edges:
        mst_graph.insert_edge(u, v, w)

    return mst_graph


# Dijkstra's Algorithm
def dijkstra(graph, source):
    V = graph.get_card_V()
    dist = [math.inf] * V
    parent = [None] * V
    visited = [False] * V

    dist[source] = 0

    for _ in range(V):
        # Find minimum distance unvisited vertex
        min_dist = math.inf
        u = -1
        for v in range(V):
            if not visited[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        if u == -1:
            break

        visited[u] = True

        # Update distances to neighbors
        for edge in graph.get_adj_list(u):
            v = edge.get_v()
            w = edge.get_weight()
            if not visited[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    return dist, parent


# Utility Functions
def generate_weighted_graph(n, density=0.15, min_w=1, max_w=20):
    G = AdjacencyListGraph(n, directed=False, weighted=True)
    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < density:
                w = random.randint(min_w, max_w)
                G.insert_edge(u, v, w)
    return G


def measure_mst_time_once(n, density=0.15):
    G = generate_weighted_graph(n, density=density)
    start = time.time()
    _ = kruskal(G)
    end = time.time()
    return end - start


def measure_runtime(sizes, trials=3, density=0.15):
    results = []
    for n in sizes:
        times = []
        print(f"Measuring MST time for n={n} (density={density})")
        for t in range(trials):
            dt = measure_mst_time_once(n, density=density)
            times.append(dt)
            print(f"  trial {t + 1}: {dt:.4f} s")
        avg = sum(times) / len(times)
        results.append(avg)
        print(f" -> avg {avg:.4f} s\n")
    return results


def plot_and_save(sizes, times, outpath):
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, marker='o', linewidth=2, markersize=8)
    plt.xlabel("Number of stations (n)", fontsize=12)
    plt.ylabel("Average MST time (s)", fontsize=12)
    plt.title("Task 4(b): Average Time to Compute MST (Kruskal's Algorithm)", fontsize=14)
    plt.grid(True, alpha=0.3)
    os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
    plt.savefig(outpath, dpi=300, bbox_inches='tight')
    print(f"Plot saved to: {outpath}")
    plt.show()


# London Underground Data Loader
def load_london_excel(path):
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("pandas not installed. Please install: pip install pandas openpyxl")

    if not os.path.exists(path):
        raise FileNotFoundError(f"London data file not found at {path}. Place the XLSX file there.")

    df = pd.read_excel(path)
    cols = list(df.columns)
    lowcols = [c.lower() for c in cols]

    # Find station and time columns
    try:
        s1_col = cols[lowcols.index('station1')]
        s2_col = cols[lowcols.index('station2')]
        time_col = cols[lowcols.index('time')]
    except ValueError:
        raise ValueError(f"Could not find expected columns 'Station1', 'Station2', 'Time'. Found: {cols}")

    # Build unique station list
    stations = sorted(set(df[s1_col].astype(str)).union(set(df[s2_col].astype(str))))
    idx = {s: i for i, s in enumerate(stations)}
    G = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    # Keep minimum time if multiple edges between same pair
    seen = {}
    for _, row in df.iterrows():
        a = str(row[s1_col])
        b = str(row[s2_col])
        try:
            t = float(row[time_col])
        except Exception:
            continue
        u = idx[a]
        v = idx[b]
        key = tuple(sorted((u, v)))
        if key not in seen or t < seen[key]:
            seen[key] = t

    for (u, v), w in seen.items():
        G.insert_edge(u, v, w)

    return G, stations, idx


def compute_backbone_from_graph(G, stations):
    mst_graph = kruskal(G)

    # Extract MST edges and total weight
    total = 0
    mst_edges = []
    for u in range(mst_graph.get_card_V()):
        for e in mst_graph.get_adj_list(u):
            v = e.get_v()
            if u < v:
                w = e.get_weight()
                total += w
                mst_edges.append((u, v, w))

    # Build set of all original edges
    all_edges = set()
    for u in range(G.get_card_V()):
        for e in G.get_adj_list(u):
            v = e.get_v()
            if u < v:
                all_edges.add((u, v, e.get_weight()))

    mst_set_keys = {(min(u, v), max(u, v)) for u, v, w in mst_edges}
    redundant = [(u, v, w) for (u, v, w) in all_edges if (min(u, v), max(u, v)) not in mst_set_keys]

    return total, mst_edges, redundant


def reconstruct_path(parent, source, target, stations):
    path = []
    x = target
    while x is not None:
        path.append(stations[x])
        x = parent[x]
    path.reverse()
    return path


def impact_analysis(original_graph, stations, idx, mst_edges, source_name, target_name):
    if source_name not in idx or target_name not in idx:
        print(f"Source or target not in station list: {source_name}, {target_name}")
        return

    source = idx[source_name]
    target = idx[target_name]

    # Original shortest path
    dist_full, parent_full = dijkstra(original_graph, source)
    if math.isinf(dist_full[target]):
        print("No path in original graph between the given stations.")
        return
    path_full = reconstruct_path(parent_full, source, target, stations)

    # Backbone-only graph using MST edges
    G2 = AdjacencyListGraph(len(stations), directed=False, weighted=True)
    for u, v, w in mst_edges:
        G2.insert_edge(u, v, w)

    dist_back, parent_back = dijkstra(G2, source)
    if math.isinf(dist_back[target]):
        print("No path in backbone-only graph between the given stations.")
        return
    path_back = reconstruct_path(parent_back, source, target, stations)

    print("\n" + "=" * 70)
    print("IMPACT ANALYSIS")
    print("=" * 70)
    print(f"From: {source_name} → To: {target_name}")
    print("\nOriginal Network:")
    print("  Path:", " → ".join(path_full))
    print(f"  Total time: {dist_full[target]:.2f} minutes")
    print("\nBackbone-Only Network:")
    print("  Path:", " → ".join(path_back))
    print(f"  Total time: {dist_back[target]:.2f} minutes")
    print(f"\nTime Increase: {dist_back[target] - dist_full[target]:.2f} minutes")
    print(f"Percentage Increase: {((dist_back[target] / dist_full[target]) - 1) * 100:.2f}%")


# Main Function
def run_task4b():
    print("=" * 70)
    print("TASK 4(b): Empirical MST Runtime Measurement")
    print("=" * 70)
    print()

    # Part 1: Runtime measurement
    sizes = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    times = measure_runtime(sizes, trials=3, density=0.12)

    outplot = os.path.join("outputs", "graphs", "task4b_runtime_plot.png")
    plot_and_save(sizes, times, outplot)

    print("\n" + "=" * 70)
    print("TASK 4(b): Compute Backbone for London Underground")
    print("=" * 70)
    print()

    # Part 2: Real London Underground backbone
    excel_path = os.path.join("data.London Underground Data.xlsx")

    try:
        G, stations, idx = load_london_excel(excel_path)
    except Exception as e:
        print(f"Error loading London data: {e}")
        print("\nNote: Place 'London Underground Data.xlsx' in a 'data' folder and re-run.")
        print("The file should have columns: 'Station1', 'Station2', 'Time'")
        return

    total, mst_edges, redundant = compute_backbone_from_graph(G, stations)

    print(f"\nTotal weight of backbone (sum of MST edges): {total:.2f} minutes")
    print(f"Number of stations: {len(stations)}")
    print(f"Number of backbone edges: {len(mst_edges)}")
    print(f"Number of redundant (closable) edges: {len(redundant)}")

    print("\n" + "-" * 70)
    print("First 10 redundant (closable) connections:")
    print("-" * 70)
    for i, (u, v, w) in enumerate(redundant[:10], 1):
        print(f"  {i:2d}. {stations[u]} - {stations[v]} (time: {w:.2f} min)")

    # Save redundant edges to file
    outdir = os.path.join("outputs", "results")
    os.makedirs(outdir, exist_ok=True)
    outfile = os.path.join(outdir, "task4b_redundant_edges.txt")
    with open(outfile, "w", encoding="utf-8") as fh:
        fh.write("Redundant Edges (can be closed while preserving connectivity)\n")
        fh.write("=" * 70 + "\n\n")
        for u, v, w in redundant:
            fh.write(f"{stations[u]} - {stations[v]}, time={w:.2f} minutes\n")
    print(f"\nAll redundant edges saved to: {outfile}")

    # Part 3: Impact analysis example
    example_source = "Wimbledon"
    example_target = "Stratford"

    print(f"\n{'=' * 70}")
    print(f"Performing impact analysis: {example_source} → {example_target}")
    print('=' * 70)

    impact_analysis(G, stations, idx, mst_edges, example_source, example_target)


if __name__ == "__main__":
    run_task4b()


