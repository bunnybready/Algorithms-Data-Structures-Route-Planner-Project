# Dataset (embedded)
stations = [
    "King's Cross", "Liverpool Street", "Paddington", "Victoria",
    "Waterloo", "Euston", "Stratford", "Canary Wharf"
]

station_to_index = {name: i for i, name in enumerate(stations)}
index_to_station = {i: name for i, name in enumerate(stations)}


# Graph structure: adjacency list representation
class Edge:
    def __init__(self, v, weight):
        self.v = v
        self.weight = weight

    def get_v(self):
        return self.v

    def get_weight(self):
        return self.weight


class Graph:
    def __init__(self, V):
        self.V = V
        self.adj_list = [[] for _ in range(V)]

    def add_edge(self, u, v, weight):
        self.adj_list[u].append(Edge(v, weight))
        self.adj_list[v].append(Edge(u, weight))

    def get_card_V(self):
        return self.V

    def get_adj_list(self, u):
        return self.adj_list[u]


# Create graph with sample edges
graph = Graph(len(stations))
# Add edges (u, v, weight) - adjust these to match your actual dataset
edges_data = [
    (0, 1, 5),  # King's Cross - Liverpool Street
    (0, 2, 8),  # King's Cross - Paddington
    (0, 5, 3),  # King's Cross - Euston
    (1, 3, 7),  # Liverpool Street - Victoria
    (1, 6, 4),  # Liverpool Street - Stratford
    (2, 3, 6),  # Paddington - Victoria
    (2, 4, 9),  # Paddington - Waterloo
    (3, 4, 5),  # Victoria - Waterloo
    (4, 5, 10),  # Waterloo - Euston
    (6, 7, 3),  # Stratford - Canary Wharf
    (1, 7, 6),  # Liverpool Street - Canary Wharf
]

for u, v, w in edges_data:
    graph.add_edge(u, v, w)


# Disjoint Set (Union-Find)
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


# Kruskal's algorithm
def kruskal(graph):
    V = graph.get_card_V()
    edges = []
    for u in range(V):
        for edge in graph.get_adj_list(u):
            v = edge.get_v()
            if u < v:  # avoid duplicates
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

    # Build a new graph representing MST
    class MSTGraph:
        def __init__(self, V, edges):
            self.V = V
            self.adj_list = [[] for _ in range(V)]
            for u, v, w in edges:
                self.adj_list[u].append((v, w))
                self.adj_list[v].append((u, w))

        def get_card_V(self):
            return self.V

        def get_adj_list(self, u):
            return [Edge(v, w) for v, w in self.adj_list[u]]

    return MSTGraph(V, mst_edges)


# ------------------------
# Utility functions
# ------------------------
def extract_edges_from_graph(G):
    edges = []
    V = G.get_card_V()
    for u in range(V):
        for edge in G.get_adj_list(u):
            v = edge.get_v()
            if u < v:
                edges.append((u, v, edge.get_weight()))
    return edges


def manual_kruskal_trace(edges, V):
    print("Manual Kruskal trace (edges in nondecreasing weight order):")
    print("-" * 70)
    edges_sorted = sorted(edges, key=lambda x: x[2])
    forest = [make_set(v) for v in range(V)]
    selected = []

    for u, v, w in edges_sorted:
        if find_set(forest[u]) != find_set(forest[v]):
            print(f"✓ Edge {index_to_station[u]} - {index_to_station[v]} (weight={w}) => SELECTED")
            selected.append((u, v, w))
            union(forest[u], forest[v])
        else:
            print(f"✗ Edge {index_to_station[u]} - {index_to_station[v]} (weight={w}) => SKIPPED (creates cycle)")
        if len(selected) == V - 1:
            break

    print("\n" + "=" * 70)
    print("Manual MST edges:")
    print("=" * 70)
    total_weight = 0
    for u, v, w in selected:
        print(f"  {index_to_station[u]} - {index_to_station[v]} (weight={w})")
        total_weight += w
    print(f"\nTotal MST weight: {total_weight}")
    return selected


def mst_edges_to_set(mst_edges):
    return {(min(u, v), max(u, v)) for u, v, w in mst_edges}


# ------------------------
# Main function
# ------------------------
def run_task4a():
    print("=" * 70)
    print("TASK 4(a): Manual Trace + Kruskal Verification")
    print("=" * 70)
    print()

    edges = extract_edges_from_graph(graph)
    V = graph.get_card_V()

    manual_mst = manual_kruskal_trace(edges, V)

    print("\n" + "=" * 70)
    print("Running library Kruskal (verification)...")
    print("=" * 70)
    lib_mst_graph = kruskal(graph)
    lib_edges = extract_edges_from_graph(lib_mst_graph)

    print("\nLibrary MST edges:")
    total_weight = 0
    for u, v, w in lib_edges:
        print(f"  {index_to_station[u]} - {index_to_station[v]} (weight={w})")
        total_weight += w
    print(f"\nTotal MST weight: {total_weight}")

    # Verification
    manual_set = mst_edges_to_set(manual_mst)
    lib_set = mst_edges_to_set(lib_edges)

    print("\n" + "=" * 70)
    print("VERIFICATION RESULTS:")
    print("=" * 70)
    print(f"Manual MST == Library MST? -> {manual_set == lib_set}")

    if manual_set == lib_set:
        print("✓ SUCCESS: Both methods produce identical MST!")
    else:
        print("✗ MISMATCH: Results differ (check implementation)")

    # Closable edges
    all_edge_set = {(min(u, v), max(u, v)) for u, v, w in edges}
    closable = all_edge_set - lib_set

    print("\n" + "=" * 70)
    print("Edges that can be CLOSED while preserving connectivity:")
    print("=" * 70)
    if closable:
        for a, b in sorted(closable):
            original_weight = next(w for u, v, w in edges if (min(u, v), max(u, v)) == (a, b))
            print(f"  {index_to_station[a]} - {index_to_station[b]} (weight={original_weight})")
        print(f"\nTotal closable edges: {len(closable)}")
    else:
        print("  No edges can be closed (all edges are in MST)")


if __name__ == "__main__":
    run_task4a()