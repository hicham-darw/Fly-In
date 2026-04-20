from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone


if __name__ == '__main__':
    parser = Parser('maps/hard/01_maze_nightmare.txt')
    parser.parse_content_file()
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs)
    graph.add_edges(parser.connections)
    for key, value in graph.adj_graph.items():
        print(f"{key} :::: {value}")

    print("-" * 40)
    path_to_goal = graph.breadth_first_search()
    flow_path = graph.get_min_flow(path_to_goal)
    #  continue in main should count flow of network!!
    # use this in class graph ... continue!!!

    for index in range(len(path_to_goal) - 1):
        connection = graph.get_connection(path_to_goal[index], path_to_goal[index + 1])
        connection.metadata['max_link_capacity'] -= flow_path
        print(connection)
        print("-" * 30)

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
    print()
