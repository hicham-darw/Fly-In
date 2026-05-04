import sys
from src.Parser.Parser import Parser
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.DroneFlowEngine.DroneFlowEngine import DroneFlowEngine
from src.EdmondsKarpAlgo.EdmondsKarpAlgo import EdmondsKarpAlgo

if __name__ == '__main__':

    #  check argument.........!
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path to file>.")
        sys.exit(42)
    
    #  parse file....
    parser = Parser(sys.argv[1])
    graph_data = parser.parse()
    if graph_data is None:
        sys.exit(42)

    #  graph builder here....!
    graph_builder = GraphBuilder()
    graph_builder.build(graph_data)

    #  starting simulation here.....!
    flow_engine = DroneFlowEngine(graph_builder, EdmondsKarpAlgo(graph_builder), graph_data['nb_drones'])
    flow_engine.run()
    print("number of turns:", flow_engine.turns_simulation)