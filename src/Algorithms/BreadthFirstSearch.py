from collections import deque
from src.Algorithms.Algo import Algo
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.DataClasses.DataClasses import Hub, Connection


class BreadthFirstSearch(Algo):

    def __init__(self, graph: GraphBuilder) -> None:
        super().__init__(graph)

    def run(self) -> list[str]:
        """Return the first path found from the start hub to the end hub.

        Returns:
            The path from start to end, or an empty list if no path exists.
        """
        start_hub = self._graph.get_start_hub()
        end_hub = self._graph.get_end_hub()

        if start_hub is None or end_hub is None:
            return []

        queue: deque = deque()
        queue.append((start_hub.name, [start_hub.name]))
        self.visited.append(start_hub.name)
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
                    connection = self._graph.get_connection_by_names(
                        current,
                        neighbor
                    )
                    next = self._graph.get_hub_by_name(neighbor)
                    if connection is None or next is None:
                        continue

                    if self.__not_available_drone_to_move(connection, next):
                        continue

                    self.visited.append(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        return []

    def __not_available_drone_to_move(
        self,
        connection: Connection,
        next_hub: Hub
    ) -> bool:
        if connection.available_drones < 1:
            return True
        elif next_hub.available_drones < 1:
            return True
        return False
