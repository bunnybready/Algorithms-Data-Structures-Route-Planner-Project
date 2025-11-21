import sys, os, time, random, string
import matplotlib.pyplot as plt

# Make sure Python can see the clrsPython package from your project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from clrsPython.Chapter_11.chained_hashtable import ChainedHashTable
from clrsPython.Chapter_11.hash_functions import cryptographic_hash


# ============================
# Station wrapper (same idea as Task 1a)
# ============================
class Station:
    def __init__(self, name, key):
        self.name = name
        self.key = key

    @staticmethod
    def get_key(obj):
        return obj.key

    def __str__(self):
        return self.name


# ============================
# Data generation
# ============================
def generate_stations(n):
    """
    Generate n artificial station names: Station_XXXXX.
    Uses random letters so keys are not trivial.
    """
    stations = []
    for i in range(n):
        suffix = ''.join(random.choices(string.ascii_uppercase, k=5))
        stations.append(f"Station_{suffix}")
    return stations


# ============================
# Timing one size n
# ============================
def measure_times_for_n(n, runs=3):
    """
    Measure average time per insert / search / delete operation
    for a chained hash table of size n, averaged over `runs`.
    Returns (insert_avg, search_avg, delete_avg) in seconds per operation.
    """
    insert_total = 0.0
    search_total = 0.0
    delete_total = 0.0

    for _ in range(runs):
        stations = generate_stations(n)

        # Create a new hash table for each run
        table = ChainedHashTable(n, Station.get_key)

        # --- Measure insert time ---
        start = time.perf_counter()
        for name in stations:
            key = cryptographic_hash(name, n)
            table.insert(Station(name, key))
        end = time.perf_counter()
        insert_total += (end - start)

        # --- Measure search time ---
        start = time.perf_counter()
        for name in stations:
            key = cryptographic_hash(name, n)
            table.search(key)  # returns node or None
        end = time.perf_counter()
        search_total += (end - start)

        # --- Measure delete time ---
        start = time.perf_counter()
        for name in stations:
            key = cryptographic_hash(name, n)
            node = table.search(key)
            if node:
                table.delete(node)   # CLRS delete takes the node itself
        end = time.perf_counter()
        delete_total += (end - start)

    # Average *per operation* time
    insert_avg = insert_total / (runs * n)
    search_avg = search_total / (runs * n)
    delete_avg = delete_total / (runs * n)

    return insert_avg, search_avg, delete_avg


# ============================
# Main experiment + plotting
# ============================
if __name__ == "__main__":
    # Different network sizes (n = number of stations)
    ns = [100, 500, 1000, 5000, 10000]

    insert_times = []
    search_times = []
    delete_times = []

    for n in ns:
        ins, sea, dele = measure_times_for_n(n, runs=3)
        insert_times.append(ins)
        search_times.append(sea)
        delete_times.append(dele)

        print(f"n={n}: "
              f"insert={ins:.3e} s/op, "
              f"search={sea:.3e} s/op, "
              f"delete={dele:.3e} s/op")

    # Plot average time per operation vs n
    plt.plot(ns, insert_times, marker="o", label="Insert")
    plt.plot(ns, search_times, marker="s", label="Search")
    plt.plot(ns, delete_times, marker="^", label="Delete")

    plt.xlabel("Network size n (number of stations)")
    plt.ylabel("Average time per operation (seconds)")
    plt.title("Chained Hash Table Performance vs Network Size")
    plt.legend()
    plt.grid(True)

    # Save the figure so you can drop it straight into your report
    plt.tight_layout()
    plt.savefig("task1b_hash_performance.png")

    # And/or show it interactively
    plt.show()
