from src.Algorithms.Algo import Algo
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.Algorithms.BreadthFirstSearch import BreadthFirstSearch
from src.DataClasses.DataClasses import PathsAndFlow

class EdmondsKarpAlgo(Algo):

    def __init__(self, graph: GraphBuilder) -> None:
        """Constructor algo Edmonds-karp for calcul drones flow

        Args:
            graph: (GraphBuilder): graph to run algo on it
        returns:
            None
        """
        super().__init__(graph)

    def get_max_flow(self, path_to_exit: list[str]) -> int:
        """Return the minimum flow along a path to the exit.

        Args:
            path_to_exit: The path whose flow should be evaluated.
        Returns:
            The minimum flow value found on the path.
        """
        flow = 0
        for i in range(len(path_to_exit) - 1):
            first = path_to_exit[i]
            second = path_to_exit[i + 1]
            flow_conn = self._graph.get_flow_connection(first, second)
            next_hub = self._graph.get_hub_by_name(path_to_exit[i + 1])
            if next_hub is None:
                break
            flow_hub = next_hub.available_drones

            if flow_conn == -1 or flow_hub == -1:
                break

            if flow_hub < flow_conn:
                if i == 0:
                    flow = flow_hub
                elif flow > flow_hub:
                    flow = flow_hub
            else:
                if i == 0:
                    flow = flow_conn
                elif flow > flow_conn:
                    flow = flow_conn
        return flow

    def update_flow_network(self, path: list[str], flow: int) -> None:
        """ update_flow_network
            update available_drones in hub and connection
        Args:
            path (list[str]): [name of hubs and connection to update path]
            flow (int): [updated by flow]
        """
        for index in range(len(path) - 1):
            first = path[index]
            second = path[index + 1]
            connection = self._graph.get_connection_by_names(first, second)
            next_hub = self._graph.get_hub_by_name(path[index + 1])
            if next_hub is None:
                break
            next_hub.available_drones -= flow
            if connection:
                connection.available_drones -= flow

    def count_turns_in_path(self, path: list[str]) -> int:
        """how paths take turns ro reach goal hub

        Args:
            path: (list[str]): contains names of hubs from start to last
        Returns:
            number_of_tunrs: (int) how man turns take to reach end hub
        """
        number_of_turns = 0
        for i in range(0, len(path) - 1):
            next_hub = self._graph.get_hub_by_name(path[i + 1])
            if next_hub is None:
                break
            zone = next_hub.metadata.get('zone')
            if zone is None or not hasattr(zone, 'value'):
                break
            if zone.value == 3:
                number_of_turns += 2
            else:
                number_of_turns += 1
        return number_of_turns

    def create_bfs_algorithm(self) -> BreadthFirstSearch:
        return BreadthFirstSearch(self._graph)

    #  should be set breadth first search required !!
    def run(self) -> list[PathsAndFlow]:
        all_paths: list[PathsAndFlow] = list()
        bfs = self.create_bfs_algorithm()

        while True:

            path_to_goal = bfs.run()
            if not path_to_goal:
                all_paths = sorted(all_paths, key=lambda x: x['turns'])
                return all_paths

            flow_path = self.get_max_flow(path_to_goal)

            number_of_turns_in_path = self.count_turns_in_path(path_to_goal)
            all_paths.append({
                'path': path_to_goal,
                'flow': flow_path,
                'turns': number_of_turns_in_path
            })
            self.update_flow_network(path_to_goal, flow_path)
