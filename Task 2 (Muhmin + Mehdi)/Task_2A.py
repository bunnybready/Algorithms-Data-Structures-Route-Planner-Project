#Importing Dijkstra function and Adjacency list graph from clrs library provided
from clrsPython.Chapter_22.dijkstra import dijkstra
from clrsPython.Utility_functions.adjacency_list_graph import AdjacencyListGraph
#Listing the station
print("--Stations-- \n A \n B \n C \n D \n E")

#Define stations and mapping them to integer indices
stations = ['A', 'B', 'C', 'D', 'E']
station_to_index = {station: i for i, station in enumerate(stations)}
index_to_station = {i: station for station, i in station_to_index.items()}

#Creating the graph: 5 vertices, undirected, weighted
graph = AdjacencyListGraph(len(stations), directed=False, weighted=True)

#Adding weighted edges
graph.insert_edge(station_to_index['A'], station_to_index['B'], 4)
graph.insert_edge(station_to_index['A'], station_to_index['C'], 2)
graph.insert_edge(station_to_index['B'], station_to_index['C'], 1)
graph.insert_edge(station_to_index['B'], station_to_index['D'], 5)
graph.insert_edge(station_to_index['C'], station_to_index['D'], 8)
graph.insert_edge(station_to_index['C'], station_to_index['E'], 10)
graph.insert_edge(station_to_index['D'], station_to_index['E'], 2)

#Selecting Start and End stations
start_station = 'A'
end_station = 'E'

print(f"\nFinding shortest path from {start_station} to {end_station}...")

#Converting the start and end stations
start_index = station_to_index[start_station]
end_index = station_to_index[end_station]

#Calling the library's Dijkstra function
try:
    d, pi = dijkstra(graph, start_index)
    #Reconstructing the path
    path = []
    current = end_index

    #Follow predecessors backward from end until you reach start
    while current is not None:
        path.insert(0, index_to_station[current])
        current = pi[current]

#Displaying the result
    total_time = d[end_index]

    print(f"Library Dijkstra result: {path}")
    print(f"Total duration: {total_time} minutes")
#For error handling
except Exception as e:
    print(f"Error with library function: {e}")

#Verification
#Checking if the result from manual computation and code computation matches
print("\n--VERIFICATION--")
print("Manual computation result: A -> C -> B -> D -> E, 10 minutes")
print(f"Code computation result: {' -> '.join(path)}, {total_time} minutes")

if total_time == 10 and path == ['A', 'C', 'B', 'D', 'E']:
    print("SUCCESS: Manual and code results match!")
else:
    print("❌ DISCREPANCY: There is a difference between manual and code results.")