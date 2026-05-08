from src.Algorithms.Algo import Algo
from src.GraphBuilder.GraphBuilder import GraphBuilder
from collections import deque


class BreadthFirstSearch(Algo):

    def __init__(self, graph: GraphBuilder) -> None:
        super().__init__(graph)

    def run(self) -> list[str]:
        """Return the first path found from the start hub to the end hub.

        Returns:
            The path from start to end, or an empty list if no path exists.
        """
        if self._graph.get_start_hub() is None or self._graph.get_end_hub() is None:
            return []

        queue = deque()
        queue.append((self._graph.get_start_hub().name, [self._graph.get_start_hub().name]))
        self.visited.append(self._graph.get_start_hub().name)
        while len(queue):

            current, path = queue.popleft()

            if current == self._graph.get_end_hub().name:
                self.visited = []
                return path

            for neighbor in self._graph.get_adjacency_list()[current]:
                type_of_zone = self._graph.get_type_of_zone(neighbor)
                if type_of_zone and type_of_zone.value == 4:
                    continue
                elif neighbor not in self.visited:
                    connection = self._graph.get_connection_by_names(current, neighbor)
                    next_hub = self._graph.get_hub_by_name(neighbor)
                    if (connection and connection.available_drones < 1) or (next_hub and next_hub.available_drones < 1):
                        continue
                    self.visited.append(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return []

