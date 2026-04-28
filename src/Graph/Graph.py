# import sys
from src.Zone.Zone import Hub, Connection
from collections import deque
from src.Enums.Enums import TypeZone
from src.Drone.Drone import Drone

import sys


class Graph:
    """Represent the zone graph and the path-search helpers."""

    def __init__(self, start_hub: Hub, end_hub: Hub, hubs: list[Hub], nb_drones) -> None:
        """Initialize the graph from parsed hubs.

        Args:
            start_hub: The starting hub.
            end_hub: The destination hub.
            hubs: The intermediate hubs.
        """
        self.nb_drones = nb_drones
        self.adj_graph = dict()
        self.start_hub = start_hub
        
        self.end_hub = end_hub
        self.hubs = hubs
        self.adj_graph[start_hub.name] = []
        for hub in hubs:
            self.adj_graph[hub.name] = []
        self.adj_graph[end_hub.name] = []
        self.visited = []
        self.unvisited = []

    def add_edges(self, connections) -> None:
        """Insert each connection into the adjacency lists.

        Args:
            connections: The list of connections to add.
        """
        self.connections = connections

        for conn in connections:
            pos = self.positionInAdjList(conn.zone2, self.adj_graph[conn.zone1])
            self.adj_graph[conn.zone1].insert(pos, conn.zone2)

            pos = self.positionInAdjList(conn.zone1, self.adj_graph[conn.zone2])
            self.adj_graph[conn.zone2].insert(pos, conn.zone1)

    def positionInAdjList(self, name_hub, lst) -> int:
        """Return the insertion index for a hub based on zone priority.

        Args:
            name_hub: The name of the hub to insert.
            lst: The current adjacency list.

        Returns:
            The index at which the hub should be inserted.
        """
        hub = self.get_hub(name_hub)
        current_zone = hub.metadata.get('zone', TypeZone.normal)

        for index, elem in enumerate(lst):
            check_hub = self.get_hub(elem)
            check_zone = check_hub.metadata.get('zone', TypeZone.normal)

            if current_zone.value < check_zone.value:
                return index

        return len(lst)

    def get_hub(self, name_hub: str) -> Hub | None:
        """Return the hub object by matching a hub name.

        Args:
            name_hub: The name of the hub to look up.

        Returns:
            The matching hub, or None if no hub matches.
        """
        if name_hub == self.start_hub.name:
            return self.start_hub
        elif name_hub == self.end_hub.name:
            return self.end_hub
        for hub in self.hubs:
            if hub.name == name_hub:
                return hub

    def get_connection(self, current_hub: str, next_hub: str) -> Connection:
        for conn in self.connections:
            if conn.zone1 == current_hub and conn.zone2 == next_hub:
                return conn
            elif conn.zone2 == current_hub and conn.zone1 == next_hub:
                return conn
        return None

    def breadth_first_search(self) -> list:
        """Return the first path found from the start hub to the end hub.

        Returns:
            The path from start to end, or an empty list if no path exists.
        """

        queue = deque()
        queue.append((self.start_hub.name, [self.start_hub.name]))
        self.visited.append(self.start_hub.name)
        while len(queue):

            current, path = queue.popleft()

            if current == self.end_hub.name:
                self.visited = []
                return path

            for neighbor in self.adj_graph[current]:
                type_of_zone = self.get_type_of_zone(neighbor)
                if type_of_zone.value == 4:
                    continue
                elif neighbor not in self.visited:

                    # for checking edmonds karp could be delete it
                    connection = self.get_connection(current, neighbor)
                    next_hub = self.get_hub(neighbor)
                    if connection.available_drones == 0 or next_hub.available_drones == 0:
                        continue
                    #  finish here!!

                    self.visited.append(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return []

    def edmonds_karp(self) -> list[tuple[list[str], int]]:
        all_paths = list()
        while True:
            path_to_goal = self.breadth_first_search()

            if not path_to_goal:
                all_paths = sorted(all_paths, key=lambda x: len(x['path']))
                return all_paths

            flow_path = self.get_max_flow(path_to_goal)
            all_paths.append({'path': path_to_goal, 'flow': flow_path, 'drones': None})
            self.update_flow_network(path_to_goal, flow_path)

    def update_flow_network(self, path: list[str], flow: int) -> None:
        for index in range(len(path) - 1):
            connection = self.get_connection(path[index], path[index + 1])
            next_hub = self.get_hub(path[index + 1])
            next_hub.available_drones -= flow
            connection.available_drones -= flow

    def move_drones_to_next_hub(self, prev_hub: Hub, current_hub: Hub, flow: int) -> None:
        while flow:
            if current_hub.drones is None:
                current_hub.drones = []
                continue
            try:
                drone = prev_hub.drones.pop(0)
            except IndexError:
                break
            current_hub.drones.append(drone)
            flow -= 1

    def prepare_drones(
        self, all_data: list[dict[str, list[str] | int]]
    ) -> list[dict[str, list[str | Drone] | int]]:

        number_of_drones = self.nb_drones
        index_data = 0
        i = 0
        
        while i < number_of_drones:

            best_path = self.best_position_of_drone(all_data)
            
            flow = best_path['flow']
            while flow:
                try:
                    best_path['drones'].append(self.start_hub.drones[i].drone_id)
                except IndexError:
                    break
                flow -= 1
                i += 1

        return all_data

    def best_position_of_drone(self, all_data) -> dict[str, list[int | str] | int]:
        best_path = None
        
        for data in all_data:
            
            if not data['drones']:
                data['drones'] = []
            
            if best_path is None:
                best_path = data
            elif len(data['path']) + (len(data['drones']) // data['flow'])\
            < len(best_path['path']) + (len(best_path['drones']) // best_path['flow']):
                best_path = data

        return best_path


    def simulate_turn(
        self, all_data: list[dict[str, list[str | Drone] | int]]
    ) -> None:
        while not self.end_hub.drones or len(self.end_hub.drones) != self.nb_drones:
            for data_turn in all_data:
                path = data_turn['path']
                flow = data_turn['flow']
                drones = data_turn['drones']
                print(f"path: {path}")
                print(f"flow: {flow}")
                print(f"drones: {drones}")

                for index_next_hub in range(len(path) - 1, 0):
                    index_current_hub = index_next_hub - 1

                    next_hub = self.get_hub(path[index_next_hub])
                    current_hub = self.get_hub(path[index_current_hub])
                    if not current_hub.drones:
                        continue
                    if not next_hub.drones:
                        next_hub.drones = []
                    print("OK!")
                    counter = flow
                    while counter:
                        try:
                            drone = current_hub.drones.pop(0)
                            next_hub.drones.append(drone)
                        except IndexError:
                            break
                        counter -= 1
                    print(f"next_hub.drones: {next_hub.drones}")
                    print(f"current_hub.drones: {current_hub.drones}")

            
                    



    def get_type_of_zone(self, name_hub: str) -> TypeZone:
        """Return the zone type associated with a hub name.

        Args:
            name_hub: The name of the hub.

        Returns:
            The zone type associated with the hub.
        """
        if name_hub == self.start_hub.name:
            return self.start_hub.metadata.get('zone')
        elif name_hub == self.end_hub.name:
            return self.end_hub.metadata.get('zone')
        else:
            for hub in self.hubs:
                if name_hub == hub.name:
                    return hub.metadata.get('zone')

    def get_flow_connection(self, current_hub: str, next_hub: str) -> int:
        for conn in self.connections:
            if conn.zone1 == current_hub and conn.zone2 == next_hub:
                return conn.available_drones
            elif conn.zone2 == current_hub and conn.zone1 == next_hub:
                return conn.available_drones
        return -1

    def get_max_flow(self, path_to_exit: list[str]) -> int:
        """Return the minimum flow along a path to the exit.

        Args:
            path_to_exit: The path whose flow should be evaluated.

        Returns:
            The minimum flow value found on the path.
        """
        flow = -1
        for i in range(len(path_to_exit) - 1):
            
            flow_conn = self.get_flow_connection(path_to_exit[i], path_to_exit[i + 1])
            flow_hub = self.get_hub(path_to_exit[i + 1]).available_drones
            
            if flow_hub < flow_conn:
                if flow == -1:
                    flow = flow_hub
                elif flow != -1 and flow > flow_hub:
                    flow = flow_hub
            else:
                if flow == -1:
                    flow = flow_conn
                elif flow != -1 and flow > flow_conn:
                    flow = flow_conn

        return flow

