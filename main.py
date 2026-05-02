import sys
from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone
#///////////////////////////////////////
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.DroneFlowEngine.DroneFlowEngine import DroneFlowEngine

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("need file!")
        sys.exit(0)

    parser = Parser(sys.argv[1])
    parser.parse_content_file()

    # graph builder here....!
    graph_builder = GraphBuilder()
    graph_builder.set_number_of_drones(parser.nb_drones)\
    .set_start_hub(parser.start_hub).set_end_hub(parser.end_hub)\
    .set_hubs(parser.hubs).set_connections(parser.connections).set_adjacency_list()
    
    print("data start_hub:", graph_builder.get_start_hub())
    print("data end_hub:", graph_builder.get_end_hub())
    for data_hub in graph_builder.get_regular_hubs():
        print("data hub:", data_hub)

    flow_engine = DroneFlowEngine(graph_builder, graph_builder.get_number_of_drones())
    all_data = flow_engine.edmonds_karp()

    flow_engine.start_simulation(all_data)