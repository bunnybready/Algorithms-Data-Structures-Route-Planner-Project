
import time
import random
import matplotlib.pyplot as plt
import pandas as pd

from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra


def generate_artificial_graph(n, edge_probability=0.05, max_weight=20):
    graph = AdjacencyListGraph(n, directed=False, weighted=True)

    for u in range(n):
        for v in range(u + 1, n):
            if random.random() < edge_probability:
                weight = random.randint(1, max_weight)
                try:
                    graph.insert_edge(u, v, weight)
                except RuntimeError:
                    pass

    return graph


def measure_runtime(n, trials=20):
    graph = generate_artificial_graph(n)
    total = 0

    for _ in range(trials):
        s = random.randint(0, n - 1)
        start = time.time()
        d, pi = dijkstra(graph, s)
        end = time.time()
        total += (end - start)

    return total / trials



def run_empirical_test():
    sizes = list(range(100, 1100, 100))
    times = []

    print("Running empirical timing test...\n")
    for n in sizes:
        avg_time = measure_runtime(n)
        times.append(avg_time)
        print(f"n = {n}, average time = {avg_time:.6f} sec")

    plt.figure(figsize=(9, 6))
    plt.plot(sizes, times, marker='o')
    plt.xlabel("Network Size (n stations)")
    plt.ylabel("Average Dijkstra Runtime (seconds)")
    plt.title("Empirical Performance of Dijkstra on Artificial Tube Networks")
    plt.grid(True)
    plt.savefig("task2b_runtime_plot.png")
    plt.show()


def load_real_network(filepath):

    df = pd.read_excel(filepath)
    print(df.columns)


    # Remove rows missing data
    df = df.dropna(subset=["Station 1", "Station 2", "Time"])

    # Convert stations to strings
    df["Station 1"] = df["Station 1"].astype(str).str.strip()
    df["Station 2"] = df["Station 2"].astype(str).str.strip()

    # Remove "nan" station names
    df = df[
        (df["Station 1"].str.lower() != "nan") &
        (df["Station 2"].str.lower() != "nan")
    ]

    # Remove self-loops
    df = df[df["Station 1"] != df["Station 2"]]


    stations = sorted(set(df["Station 1"]).union(df["Station 2"]))
    station_to_index = {name: i for i, name in enumerate(stations)}
    index_to_station = {i: name for name, i in station_to_index.items()}

    graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

    # Handle duplicates: keep minimum time
    edge_map = {}

    for _, row in df.iterrows():
        u = station_to_index[row["Station 1"]]
        v = station_to_index[row["Station 2"]]
        t = row["Time"]

        key = tuple(sorted((u, v)))

        if key not in edge_map or t < edge_map[key]:
            edge_map[key] = t

    # Insert edges safely
    for (u, v), weight in edge_map.items():
        try:
            graph.insert_edge(u, v, weight)
        except RuntimeError:
            continue

    return graph, station_to_index, index_to_station



# run shortest path on real network
def run_real_shortest_path(graph, station_to_index, index_to_station, start, end):
    s = station_to_index[start]
    t = station_to_index[end]

    d, pi = dijkstra(graph, s)

    # Reconstruct path
    path = []
    current = t
    while current is not None:
        path.insert(0, index_to_station[current])
        current = pi[current]

    return path, d[t]


# main execution
if __name__ == "__main__":

    print("\n==============================")
    print("   TASK 2B – EMPIRICAL TEST")
    print("==============================\n")

    run_empirical_test()

    print("\n======================================")
    print("   LOADING REAL LONDON NETWORK DATA")
    print("======================================\n")

    graph, station_to_index, index_to_station = load_real_network("London Underground data.xlsx")

    print("Network loaded successfully!\n")
    print(f"Total stations: {graph.get_card_V()}")
    print(f"Total unique edges: {graph.get_card_E()}\n")

    # Short journey
    print("=== Short route: Piccadilly Circus → Oxford Circus ===")
    short_path, short_time = run_real_shortest_path(
        graph, station_to_index, index_to_station,
        "Piccadilly Circus", "Oxford Circus"
    )
    print("Path:", " → ".join(short_path))
    print("Total time:", short_time, "minutes\n")

    # Long journey
    print("=== Long route: Ealing Broadway → Upminster ===")
    long_path, long_time = run_real_shortest_path(
        graph, station_to_index, index_to_station,
        "Ealing Broadway", "Upminster"
    )
    print("Path:", " → ".join(long_path))
    print("Total time:", long_time, "minutes\n")
