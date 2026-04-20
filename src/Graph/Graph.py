"""Graph utilities for building adjacency lists and searching paths."""

import sys
from src.Zone.Zone import Hub, Connection
from collections import deque
from src.Enums.Enums import TypeZone


class Graph:
    """Represent the zone graph and the path-search helpers."""

    def __init__(self, start_hub: Hub, end_hub: Hub, hubs: list[Hub]) -> None:
        """Initialize the graph from parsed hubs.

        Args:
            start_hub: The starting hub.
            end_hub: The destination hub.
            hubs: The intermediate hubs.
        """
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
        else:
            for hub in self.hubs:
                if hub.name == name_hub:
                    return hub

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
                return path

            for neighbor in self.adj_graph[current]:
                type_of_zone = self.get_type_of_zone(neighbor)
                if type_of_zone.value == 4:
                    continue
                elif neighbor not in self.visited:
                    self.visited.append(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return []            
            
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

    def get_min_flow(self, path_to_exit: list) -> int:
        """Return the minimum flow along a path to the exit.

        Args:
            path_to_exit: The path whose flow should be evaluated.

        Returns:
            The minimum flow value found on the path.
        """
        pass
