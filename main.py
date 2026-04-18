from src.Parser.Parser import Parser
from src.Graph.Graph import Graph


if __name__ == '__main__':
    parser = Parser('maps/medium/02_circular_loop.txt')
    parser.parse_content_file()
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs)
    graph.add_edges(parser.connections)
    for key, value in graph.adj_graph.items():
        print(f"{key} :::: {value}")

    print("-" * 40)
    path_to_exit = graph.breadth_first_search()
    for name_hub in path_to_exit:
        if name_hub != 'goal':
            print(f"{name_hub} ---> ", end='')
        else:
            print(name_hub, end='')
    print()