from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone


if __name__ == '__main__':
    parser = Parser('maps/easy/01_linear_path.txt')
    parser.parse_content_file()
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs, parser.nb_drones)
    graph.add_edges(parser.connections)
    for key, value in graph.adj_graph.items():
        print(f"{key} :::: {value}")

    print("-" * 40)

    all_paths = graph.edmonds_karp()
    
    print(f"main paths: {all_paths}")
    print(f"graph drones: {graph.nb_drones}")
    while graph.get_hub(all_paths[0]['path'][-1]).drones is None or len(graph.get_hub(all_paths[0]['path'][-1]).drones) != graph.nb_drones:
        path = all_paths[0]['path']
        flow = all_paths[0]['flow']
        current_hub = graph.get_hub(path[0])
        index_hub = len(path) - 1
        while index_hub != 0:

            prev_hub = graph.get_hub(path[index_hub - 1])
            current_hub = graph.get_hub(path[index_hub])

            if not prev_hub.drones or not len(prev_hub.drones):
                index_hub -= 1
                continue
            
            print(f"prev_hub drones: {prev_hub.drones}")
            print(f"current hub drones: {current_hub.drones}")
            graph.move_drones_to_next_hub(prev_hub, current_hub, flow)
            index_hub -= 1
        break
    print("@" * 40)
    print("drones of end-hub:", graph.get_hub('darwin').drones)
    print("drones of start-hub:", graph.start_hub.drones)













    #         # should every hub take flow of drones and put them into next_hub
    # print("@" * 20)
    # print(f"drones in end_hub: {len(graph.get_hub('goal').drones)}")
    # print("@" * 20)

