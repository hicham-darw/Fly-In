import sys
from src.Parser.Parser import Parser
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.DroneFlowEngine.DroneFlowEngine import DroneFlowEngine
from src.Algorithms.EdmondsKarpAlgo import EdmondsKarpAlgo

if __name__ == '__main__':

    #  check argument.........!
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path to file>.")
        sys.exit(42)

    flow_engine = DroneFlowEngine()
    flow_engine.parse_file()
    flow_engine.init_graph()
    flow_engine.init_algo()
    flow_engine.create_drones()
    flow_engine.set_drones_in_start_hub()
    flow_engine.execute_simulation()

    print("number of turns:", flow_engine.turns_simulation)