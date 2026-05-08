from src.Algorithms.Algo import Algo
from src.GraphBuilder.GraphBuilder import GraphBuilder


class DepthFirstSearch(Algo):
    def __init__(self, graph: GraphBuilder) -> None:
        self.super().__init__(graph)

    def run(self, start_node: str, target_node: str) -> str | None:

        adjacency_list = self.get_adjacency_list()
        if start_node == target_node:
            self.visited = []
            return start_node
        
        for neighbor in self.adjcency_list[start_node]:
            if neighbor not in self.visited:
                self.run(neighbor, target_name)
                self.visited.append(neighbor)
        return None