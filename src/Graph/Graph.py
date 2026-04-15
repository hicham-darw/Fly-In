from src.Zone.Zone import Hub, Connection


class Graph:

    def __init__(self, start_hub: Hub, end_hub: Hub, hubs: list[Hub]) -> None:
        self.adj_graph = dict()
        self.adj_graph[start_hub.name] = []
        for hub in hubs:
            self.adj_graph[hub.name] = []
        self.adj_graph[end_hub.name] = []

    def add_edges(self, connections) -> None:
        for conn in connections:
            self.adj_graph[conn.zone1].append(conn.zone2)
            self.adj_graph[conn.zone2].append(conn.zone1)
    