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

    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs, parser.nb_drones)
    graph.add_edges(parser.connections)

    all_data = graph.edmonds_karp()
    for data in all_data:
        print(f"data: {data}")
    print("----")
    graph.start_simulation(all_data)
    print("#" * 50)
    print(f"turns: {graph.turns_simulation}")
    print("#" * 50)
    print(f"{[drone.drone_id for drone in graph.end_hub.drones]}")

