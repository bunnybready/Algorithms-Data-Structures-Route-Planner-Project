from lib.clrsPython.ch22.graph import Graph

stations = ["A", "B", "C", "D", "E"]
station_to_index = {s: i for i, s in enumerate(stations)}

graph = Graph(len(stations), directed=False)

graph.add_edge(station_to_index['A'], station_to_index['B'], 4)
graph.add_edge(station_to_index['A'], station_to_index['C'], 2)
graph.add_edge(station_to_index['B'], station_to_index['C'], 1)
graph.add_edge(station_to_index['B'], station_to_index['D'], 5)
graph.add_edge(station_to_index['C'], station_to_index['D'], 8)
graph.add_edge(station_to_index['C'], station_to_index['E'], 10)
graph.add_edge(station_to_index['D'], station_to_index['E'], 2)
