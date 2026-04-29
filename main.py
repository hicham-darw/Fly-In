import sys
from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("need file!")
        sys.exit(0)
    parser = Parser(sys.argv[1])
    parser.parse_content_file()
    print("start_hub:---------------------------------------")
    print(f"name: {parser.end_hub.name}")
    print(f"type: {parser.end_hub.type_zone}")
    print(f"metadata: {parser.end_hub.metadata}")
    print(f"available_drones: {parser.end_hub.drones}")
    print("-" * 50)
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs, parser.nb_drones)
    graph.add_edges(parser.connections)

    all_data = graph.edmonds_karp()
    
    graph.start_simulation(all_data)
    for data in all_data:
        print(f"data: {data}")
    print("#" * 50)
    print(f"turns: {graph.turns_simulation}")
    print("#" * 50)
    print(f"{[drone.drone_id for drone in graph.end_hub.drones]}")

