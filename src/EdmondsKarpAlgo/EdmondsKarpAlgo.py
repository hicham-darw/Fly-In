from src.GraphBuilder.GraphBuilder import GraphBuilder
from collections import deque


class EdmondsKarpAlgo:

    def __init__(self, graph: GraphBuilder) -> None:
        """Constructor algo Edmonds-karp for calcul drones flow

        Args:
            graph: (GraphBuilder): graph to run algo on it
        
        returns:
            None
        """
        self.__graph = graph
        self.visited = []

    def reset_capacities(self) -> None:
        """reset_capacities graph to run algo

        Args:
            None

        Returns:
            None
        """
        self.reset_start_hub()
        self.reset_end_hub()
        self.reset_regular_hubs()
        self.reset_connections()
    
    def reset_start_hub(self) -> None:
        """reset start_hub capacity

        Args:
            None
        
        Returns:
            None
        """
        start_hub = self.__graph.get_start_hub()
        start_hub.available_drones = start_hub.metadata['max_drones']
    
    def reset_end_hub(self) -> None:
        """Reset end_hub capacity

        Args:
            None
        
        Returns:
            None
        """
        end_hub = self.__graph.get_end_hub()
        end_hub.available_drones = end_hub.metadata['max_drones']
    
    def reset_regular_hubs(self) -> None:
        """resert regular hubs capacities

        Args:
            None

        Returns:
            None
        """
        for hub in self.__graph.get_regular_hubs():
            hub.available_drones = hub.metadata['max_drones']
    
    def reset_connections(self) -> None:
        """reste connections capacities

        Args:
            None
        
        Returns:
            None
        """
        for conn in self.__graph.get_connections():
            conn.available_drones = conn.metadata['max_link_capacity']

    def get_max_flow(self, path_to_exit: list[str]) -> int:
        """Return the minimum flow along a path to the exit.

        Args:
            path_to_exit: The path whose flow should be evaluated.

        Returns:
            The minimum flow value found on the path.
        """
        flow = 0
        for i in range(len(path_to_exit) - 1):
            
            flow_conn = self.__graph.get_flow_connection(path_to_exit[i], path_to_exit[i + 1])
            flow_hub = self.__graph.get_hub_by_name(path_to_exit[i + 1]).available_drones

            if flow_conn is None or flow_hub is None:
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
            connection = self.__graph.get_connection_by_names(path[index], path[index + 1])
            next_hub = self.__graph.get_hub_by_name(path[index + 1])
            next_hub.available_drones -= flow
            if connection:
                connection.available_drones -= flow

    def count_turns_in_path(self, path: list[str]) -> int:
        number_of_turns = 0
        for i in range(0, len(path) - 1):
            next_hub = self.__graph.get_hub_by_name(path[i + 1])
            if next_hub.metadata['zone'].value == 3:
                number_of_turns += 2
            else:
                number_of_turns += 1
        return number_of_turns

    def edmonds_karp(self) -> list[dict[str, list[str], int]]:
        all_paths = list()
        flow_path = 10
        while True:
            path_to_goal = self.breadth_first_search()
            if not path_to_goal or flow_path == 0:
                all_paths = sorted(all_paths, key=lambda x: x['turns'])
                return all_paths

            flow_path = self.get_max_flow(path_to_goal)

            number_of_turns_in_path = self.count_turns_in_path(path_to_goal)
            all_paths.append({'path': path_to_goal, 'flow': flow_path, 'turns': number_of_turns_in_path})
            self.update_flow_network(path_to_goal, flow_path)
        return []

    def breadth_first_search(self) -> list:
        """Return the first path found from the start hub to the end hub.

        Returns:
            The path from start to end, or an empty list if no path exists.
        """
        if self.__graph.get_start_hub() is None or self.__graph.get_end_hub() is None:
            return []

        queue = deque()
        queue.append((self.__graph.get_start_hub().name, [self.__graph.get_start_hub().name]))
        self.visited.append(self.__graph.get_start_hub().name)
        while len(queue):

            current, path = queue.popleft()

            if current == self.__graph.get_end_hub().name:
                self.visited = []
                return path

            for neighbor in self.__graph.get_adjacency_list()[current]:
                type_of_zone = self.__graph.get_type_of_zone(neighbor)
                if type_of_zone and type_of_zone.value == 4:
                    continue
                elif neighbor not in self.visited:
                    connection = self.__graph.get_connection_by_names(current, neighbor)
                    next_hub = self.__graph.get_hub_by_name(neighbor)
                    if (connection and connection.available_drones < 1) or (next_hub and next_hub.available_drones < 1):
                        continue
                    self.visited.append(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return []
