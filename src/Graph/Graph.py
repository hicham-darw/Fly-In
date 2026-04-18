from src.Zone.Zone import Hub, Connection
from collections import deque
import sys


class Graph:

    def __init__(self, start_hub: Hub, end_hub: Hub, hubs: list[Hub]) -> None:
        self.adj_graph = dict()
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.adj_graph[start_hub.name] = []
        for hub in hubs:
            self.adj_graph[hub.name] = []
        self.adj_graph[end_hub.name] = []
        self.visited = []
        self.unvisited = []

    def add_edges(self, connections) -> None:
        for conn in connections:
            self.adj_graph[conn.zone1].append(conn.zone2)
            self.adj_graph[conn.zone2].append(conn.zone1)

    def breadth_first_search(self) -> list:

        queue = deque()
        queue.append((self.start_hub.name, [self.start_hub.name]))
        self.visited.append(self.start_hub.name)

        while len(queue):

            current, path = queue.popleft()
            if current == self.end_hub.name:
                return path

            for neighbor in self.adj_graph[current]:

                if neighbor not in self.visited:
                    self.visited.append(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return []            

