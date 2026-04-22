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

    while graph.get_hub(all_paths[0]['path'][-1]).drones is None or len(graph.get_hub(all_paths[0]['path'][-1]).drones) != graph.nb_drones:
        path = all_paths[0]['path']
        flow = all_paths[0]['flow']
        prev_hub = None
        current_hub = graph.get_hub(path[0])
        for i in range(1, len(path)):
            prev_hub = graph.get_hub(path[i - 1])
            current_hub = graph.get_hub(path[i])
            while flow:
                if current_hub.drones is None:
                    current_hub.drones = list()
                else:
                    try:
                        drone = prev_hub.drones.pop(0)
                    except IndexError:
                        break
                    current_hub.drones.append(drone)
                    flow -= 1
            flow = all_paths[0]['flow']

            # should every hub take flow of drones and put them into next_hub
        graph.nb_drones -= flow
        break
    print("-" * 40)
    print(graph.get_hub(path[i - 4]).drones)
    for drone in graph.get_hub(path[i - 4]).drones:
        print(drone.drone_id)

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
