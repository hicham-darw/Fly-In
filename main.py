from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone


if __name__ == '__main__':
    parser = Parser('maps/easy/01_linear_path.txt')
    parser.parse_content_file()
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs, parser.nb_drones)
    graph.add_edges(parser.connections)

    all_data = graph.edmonds_karp()
    
    graph.start_simulation(all_data)
    print(f"turns: {graph.turns_simulation}")
    for data in all_data:
        print(f"data: {data}")
    print("#" * 50)
    print("#" * 50)
    print(f"{[drone.drone_id for drone in graph.end_hub.drones]}")

