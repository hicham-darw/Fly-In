from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone


if __name__ == '__main__':
    parser = Parser('maps/medium/02_circular_loop.txt')
    parser.parse_content_file()
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs, parser.nb_drones)
    graph.add_edges(parser.connections)
    for key, value in graph.adj_graph.items():
        print(f"{key} :::: {value}")

    print("-" * 40)

    all_paths = graph.edmonds_karp()
    print(f"main paths: {all_paths}")

    while graph.nb_drones:
        path = all_paths[0]
        for name in path:
            hub = graph.get_hub(name)
              
    # paths created new when back track function edmonds karp


    # for path_flow in all_paths:
    #     path, flow = path_flow
    #     print("path:", path)
    #     print("flow:", flow)

    #  continue in main should count flow of network!!
    # use this in class graph ... continue!!!


    #     if hub.metadata['zone'] == TypeZone.priority:
    #         print("priority")
    #     elif hub.metadata['zone'] == TypeZone.normal:
    #         print("normal")
    #     else:
    #         print("other")
    # for name_hub in path_to_goal:
    #     if name_hub != 'goal':
    #         print(f"{name_hub} ---> ", end='')
    #     else:
    #         print(name_hub, end='')
