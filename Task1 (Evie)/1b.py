import sys, os, time, random, string
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from clrsPython.Chapter_11.chained_hashtable import ChainedHashTable


def load_station_names():
    here = os.path.dirname(__file__)
    excel_path = os.path.join(here, "..", "data", "London Underground data.xlsx")

    df = pd.read_excel(excel_path)

    # station name columns are 2nd and 3rd
    col1 = df.columns[1]
    col2 = df.columns[2]

    s1 = df[col1].dropna().astype(str)
    s2 = df[col2].dropna().astype(str)

    stations = sorted(set(s1) | set(s2))
    return stations


ALL_STATIONS = load_station_names()
print(f"Loaded {len(ALL_STATIONS)} unique London Underground stations.")


def generate_station_sample(n):
    if n >= len(ALL_STATIONS):
        return ALL_STATIONS[:]
    return random.sample(ALL_STATIONS, n)


def measure_times(n, runs=3):
    insert_total = search_total = delete_total = 0.0

    for _ in range(runs):
        sample = generate_station_sample(n)
        table = ChainedHashTable(n)

        # insert
        start = time.perf_counter()
        for name in sample:
            table.insert(name)      # same behaviour as your 1a
        insert_total += time.perf_counter() - start

        # search
        start = time.perf_counter()
        for name in sample:
            table.search(name)
        search_total += time.perf_counter() - start

        # delete
        start = time.perf_counter()
        for name in sample:
            node = table.search(name)
            if node:
                table.delete(node)  # delete using node reference (just like 1a)
        delete_total += time.perf_counter() - start

    # Average time per operation
    return (
        insert_total / (runs * n),
        search_total / (runs * n),
        delete_total / (runs * n),
    )


if __name__ == "__main__":
    max_n = len(ALL_STATIONS)

    sizes = [20, 50, 100, 150, max_n]

    insert_t = []
    search_t = []
    delete_t = []

    # RUN EXPERIMENT
    for n in sizes:
        ins, sea, dele = measure_times(n)
        insert_t.append(ins)
        search_t.append(sea)
        delete_t.append(dele)
        print(f"n={n}: insert={ins:.4e}, search={sea:.4e}, delete={dele:.4e}")

    US = 1e6

    plt.figure(figsize=(8, 5))

    plt.plot(sizes, [t * US for t in insert_t],
             marker="o", label="Insert")
    plt.plot(sizes, [t * US for t in search_t],
             marker="s", label="Search")
    plt.plot(sizes, [t * US for t in delete_t],
             marker="^", label="Delete")

    plt.xlabel("Number of stations (n)")
    plt.ylabel("Average time per operation (µs)")  # now labelled properly
    plt.title("Task 1(b): Hash Table Performance (Microseconds)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("task1b_performance_plot_microseconds.png")
    plt.show()
