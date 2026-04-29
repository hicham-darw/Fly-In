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
        self.turns_simulation: int = 0

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
                    if connection.available_drones < 1 or next_hub.available_drones < 1:
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
            all_paths.append({'path': path_to_goal, 'flow': flow_path})
            self.update_flow_network(path_to_goal, flow_path)

    def update_flow_network(self, path: list[str], flow: int) -> None:
        for index in range(len(path) - 1):
            connection = self.get_connection(path[index], path[index + 1])
            next_hub = self.get_hub(path[index + 1])
            next_hub.available_drones -= flow
            connection.available_drones -= flow

    def move_drones_to_next_hub(self, current_hub: Hub, next_hub: Hub, flow: int) -> None:
        is_restricted = 0

        while flow:
            if next_hub.drones is None:
                next_hub.drones = []

            if not current_hub.drones:
                break

            # Check both hub and connection capacity (don't decrement connection capacity)
            if next_hub.available_drones < 1:
                break

            conn = self.get_connection(current_hub.name, next_hub.name)
            if conn.available_drones < 1:
                break

            try:
                drone = current_hub.drones.pop(0)
            except IndexError:
                break
            next_hub.drones.append(drone)
            next_hub.available_drones -= 1
            current_hub.available_drones += 1
            flow -= 1
    
    def reset_capacities_of_drones(self) -> None:
        # reset connections
        for conn in self.connections:
            conn.available_drones = conn.metadata.get('max_link_capacity')
            
        # reset start Hub 
        self.start_hub.available_drones = self.nb_drones - len(self.start_hub.drones) 

        # reset regular hubs            
        for hub in self.hubs + [self.end_hub]:
            max_drones_in_hub = hub.metadata.get('max_drones')
            drones_in_hub = 0 if hub.drones is None or not hub.drones else len(hub.drones)
            hub.available_drones = max_drones_in_hub - drones_in_hub


    def start_simulation(
        self, all_data: list[dict[str, list[str | Drone] | int]]
    ) -> None:
        self.reset_capacities_of_drones()

        while not self.end_hub.drones or len(self.end_hub.drones) != self.nb_drones:
            self.simulate_turn(all_data)

    def simulate_turn(self, all_data: list[dict[str, list[str | Drone] | int]]) -> None:
        for index_data in range(len(all_data)):
            path = all_data[index_data]['path']
            flow = all_data[index_data]['flow']
            
            # find first move in path simultaneously 
            i = 0
            while i < len(path) - 1: 
                current_hub = self.get_hub(path[i])
                next_hub = self.get_hub(path[i + 1])
                if next_hub.drones is None:
                    break
                i += 1
            
            if i == len(path) - 1:
                i -= 1

            while i >= 0:
                current_hub = self.get_hub(path[i])
                next_hub = self.get_hub(path[i + 1])
                self.move_drones_to_next_hub(current_hub, next_hub, flow)
                i -= 1

    def index_of_hub_let_fly(self, path: list[str], flow: int):
        index_current_hub = 0
        index_next_hub = 1

        while index_next_hub < len(path):
            next_hub = self.get_hub(path[index_next_hub])
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
            current_hub = self.get_hub(path[index_current_hub])
            next_hub = self.get_hub(path[index_next_hub])
        
            self.move_drones_to_next_hub(current_hub, next_hub, flow)
            index_current_hub -= 1
            index_next_hub -= 1   

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

