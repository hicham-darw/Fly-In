import sys
from src.Parser.Parser import Parser
from src.Graph.Graph import Graph
from src.Enums.Enums import TypeZone
#///////////////////////////////////////
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.DroneFlowEngine.DroneFlowEngine import DroneFlowEngine
from src.Exceptions.ParsingError import ParsingError

if __name__ == '__main__':

    #  check argument.........!
    if len(sys.argv) != 2:
        print("need file!")
        sys.exit(0)
    
    #  parse file....
    parser = Parser(sys.argv[1])
    graph_data = parser.parse()
    if graph_data is None:
        sys.exit(0)

    #  graph builder here....!
    graph_builder = GraphBuilder()
    graph_builder.build(graph_data)

    #  starting simulation here.....!
    flow_engine = DroneFlowEngine(graph_builder)
    flow_engine.run()
    print("number of turns:", flow_engine.turns_simulation)