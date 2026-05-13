from sys import exit, argv, stderr
from DroneFlowEngine import DroneFlowEngine
from Parser import Parser

if __name__ == '__main__':

    #  check argument.........!
    if len(argv) != 2:
        print("Usage: python3 main.py <path to file>.", file=stderr)
        exit(42)
    parser = Parser(argv[1])
    parsed_data = parser.parse()

    flow_engine = DroneFlowEngine(parsed_data)
    flow_engine.execute_simulation()

    print("\033[1;32mnumber of turns: ", flow_engine.turns_simulation)
