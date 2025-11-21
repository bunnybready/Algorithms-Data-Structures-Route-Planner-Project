import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from clrsPython.Chapter_11.chained_hashtable import ChainedHashTable
from clrsPython.Chapter_11.hash_functions import cryptographic_hash

class Station:
    def __init__(self, name, key):
        self.name = name  # station name
        self.key = key  # integer key (hashed)

    # CLRS tables expect a static method to extract the key
    @staticmethod
    def get_key(obj):
        return obj.key

    def __str__(self):
        return f"{self.name}"


table_size = 5
T = ChainedHashTable(table_size)

stations = [
    "Ealing Broadway",
    "West Acton",
    "North Acton",
    "East Acton",
    "White City"
]
for station in stations:
    T.insert(station)
    print(f"Inserted '{station}")


print("\nFinal hash table state:")
print("T")

#Membership test
query = "West Acton"
result = T.search(query)

print("\nMembership test:")
if result:
    print(f"{query}: Operational")
else:
    print(f"{query}: Not Found")

# Deletion example
closed_station = "West Acton"
print(result)

if result:
    print("Node found:", result.data)
    T.delete(result)   # CLRS delete requires node reference
    print(f"Deleted {closed_station}")
else:
    print(f"'{closed_station}' not found for deletion.")
