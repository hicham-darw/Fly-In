from collections import deque
from src.Graph.Graph import Graph
from src.Drone.Drone import Drone
from src.Enums.Enums import TypeZone


class DroneFlowEngine:

    def __init__(self, graph: Graph) -> None:
        """Constructor engine of flow drones

        Args:
            graph (Graph): [graph to simulate hubs and connection between them]
            drones (list[Drone]): [drones]
        """
        self.__graph = graph
        self.__drones: list[Drone] = []

        self.turns_simulation = 0
        
        self.visited = []

    # setter method
    def set_drones_in_start_hub(self) -> None:
        self.__drones = []
        for i in range(self.__graph.get_number_of_drones()):
            self.__drones.append(Drone(i + 1))
        self.__graph.get_start_hub().drones = self.__drones

    # getters method ----------------->
    def get_graph(self) -> Graph:
        return self.__graph

    def run(self) -> None:
        """put drones in start_hub and starting simulation
        
        Args:
            None
        
        Returns:
            None
        """
        self.set_drones_in_start_hub()
        all_data = self.edmonds_karp()
        self.start_simulation(all_data)
        
    def start_simulation(
        self, all_data: list[dict[str, list[str | Drone] | int]]
    ) -> None:
        if not all_data:
            print("all_data is empty!");
            return

        while self.__graph.get_end_hub().drones is None or len(self.__graph.get_end_hub().drones) != self.__graph.get_number_of_drones():
            self.simulate_turn(all_data)

    def simulate_turn(self, all_data: list[dict[str, list[str | Drone] | int]]) -> None:
        for index_data in range(len(all_data)):
            path = all_data[index_data]['path']
            flow = all_data[index_data]['flow']

            # find first move in path simultaneously # check simulate_turn rafcatoring hard here!
            i = 0
            while i < len(path) - 1: 
                current_hub = self.__graph.get_hub_by_name(path[i])
                next_hub = self.__graph.get_hub_by_name(path[i + 1])
                if next_hub.drones is None:
                    break
                i += 1
            if i == len(path) - 1:
                i -= 1

            while i >= 0:
                current_hub = self.__graph.get_hub_by_name(path[i])
                next_hub = self.__graph.get_hub_by_name(path[i + 1])
                self.__graph.move_drones_to_next_hub(path[i], path[i + 1], flow)
                i -= 1
        self.turns_simulation += 1

    def edmonds_karp(self) -> list[dict[str, list[str], int]]:
        all_paths = list()
        flow_path = 10
        while True:
            path_to_goal = self.breadth_first_search()
            if not path_to_goal or flow_path == 0:
                all_paths = sorted(all_paths, key=lambda x: x['turns'])
                return all_paths

            flow_path = self.__graph.get_max_flow(path_to_goal)

            number_of_turns_in_path = self.count_turns_in_path(path_to_goal)
            all_paths.append({'path': path_to_goal, 'flow': flow_path, 'turns': number_of_turns_in_path})
            self.update_flow_network(path_to_goal, flow_path)
        return []

    def count_turns_in_path(self, path: list[str]) -> int:
        number_of_turns = 0
        for i in range(0, len(path) - 1):
            next_hub = self.__graph.get_hub_by_name(path[i + 1])
            if next_hub.metadata['zone'].value == 3:
                number_of_turns += 2
            else:
                number_of_turns += 1
        return number_of_turns

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
                type_of_zone = self.get_type_of_zone(neighbor)
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

    # helpers
    def index_of_hub_let_fly(self, path: list[str], flow: int):
        index_current_hub = 0
        index_next_hub = 1

        while index_next_hub < len(path):
            next_hub = self.__graph.get_hub_by_name(path[index_next_hub])
            if next_hub.drones is None or not next_hub.drones:
                break
            index_current_hub += 1
            index_next_hub += 1

        self.update_path_flow(path, index_current_hub, index_next_hub, flow)

    def update_path_flow(self, path: list[str], index_current_hub: int, index_next_hub: int, flow: int) -> None:
        
        if index_next_hub == len(path):
            index_next_hub -= 1
            index_current_hub -= 1
        
        while index_current_hub >= 0:
            current_hub = self.__graph.get_hub_by_name(path[index_current_hub])
            next_hub = self.__graph.get_hub_by_name(path[index_next_hub])
        
            self.move_drones_to_next_hub(current_hub, next_hub, flow)
            index_current_hub -= 1
            index_next_hub -= 1   

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

    def get_type_of_zone(self, name_hub: str) -> TypeZone:
        """Return the zone type associated with a hub name.

        Args:
            name_hub: The name of the hub.

        Returns:
            The zone type associated with the hub.
        """
        if self.__graph.get_start_hub() and name_hub == self.__graph.get_start_hub().name:
            return self.__graph.get_start_hub().metadata.get('zone')
        
        if self.__graph.get_end_hub() and name_hub == self.__graph.get_end_hub().name:
            return self.__graph.get_end_hub().metadata.get('zone')
        else:
            for hub in self.__graph.get_regular_hubs():
                if name_hub == hub.name:
                    return hub.metadata.get('zone')
