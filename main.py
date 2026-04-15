from src.Parser.Parser import Parser
from src.Graph.Graph import Graph


if __name__ == '__main__':
    parser = Parser('maps/hard/03_ultimate_challenge.txt')
    parser.parse_content_file()
    graph = Graph(parser.start_hub, parser.end_hub, parser.hubs)
    graph.add_edges(parser.connections)
    print("-" * 40)
    for key, value in graph.adj_graph.items():
        print(f"{key} connect: {value}")