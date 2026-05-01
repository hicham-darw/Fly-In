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
    flow_engine.reset_capacities_of_drones()
    all_data = flow_engine.edmonds_karp()
    print(f"all_data: {all_data}")
    # should check data of each one here ....! handle infinite loop in start_simulation()
    sys.exit(0)
    flow_engine.start_simulation(all_data)

    # print(f"{[drone.drone_id for drone in graph.end_hub.drones]}")


    # flow_engine = DroneFlowEngine()
    # flow_engine.set_nb_drones(parser.nb_drones).set_
    # .set_start_hub()
#///////////////////////////////////////////

    # if len(sys.argv) != 2:
    #     print("need file!")
    #     sys.exit(0)
    # parser = Parser(sys.argv[1])
    # parser.parse_content_file()

    # graph = Graph(parser.start_hub, parser.end_hub, parser.hubs, parser.nb_drones)
    # graph.add_edges(parser.connections)

    # all_data = graph.edmonds_karp()
    # for data in all_data:
    #     print(f"data: {data}")
    # print("----")
    # graph.start_simulation(all_data)
    # print("#" * 50)
    # print(f"turns: {graph.turns_simulation}")
    # print("#" * 50)
    # print(f"{[drone.drone_id for drone in graph.end_hub.drones]}")

