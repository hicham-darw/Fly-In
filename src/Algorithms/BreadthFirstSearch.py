from collections import deque
from typing import Any
from src.Algorithms.Algo import Algo
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.DataClasses.DataClasses import Hub, Connection


class BreadthFirstSearch(Algo):
    """class BreadthFirstSearch inherit from Algo base class
        blueprint how algo behave
    """
    def __init__(self, graph: GraphBuilder) -> None:
        """constructor of breadth first search intial graph and queue

        Args:
            graph: (GraphBuilder): graph for running algo on thi graph
        Return:
            None
        """
        super().__init__(graph)
        self.queue: deque[tuple[str, list[str]]] = deque()

    def run(self) -> Any:
        """Return the first path found from the start hub to the end hub.

        Returns:
            The path from start to end, or an empty list if no path exists.
        """
        start_hub = self._graph.get_start_hub()
        end_hub = self._graph.get_end_hub()

        if start_hub is None or end_hub is None:
            return []

        self.queue.append((start_hub.name, [start_hub.name]))
        self.visited.append(start_hub.name)
        while len(self.queue):

            current, path = self.queue.popleft()
            if current == self._graph.get_end_hub().name:
                self.__reinitialize_data()
                return path

            for neighbor in self._graph.get_adjacency_list()[current]:
                if self.__is_blocked_zone(neighbor):
                    continue

                if neighbor not in self.visited:
                    if self.__is_valid_neighbor(current, neighbor):
                        self.__add_to_queue(path, neighbor)
        return []

    def __is_blocked_zone(self, neighbor: str) -> bool:
        """method check next zone if is blocked or not

        Args:
            neighbor: (str): name of next zone
        Return:
            bool: return True if is blocked otherwise return False
        """
        type_of_zone = self._graph.get_type_of_zone(neighbor)
        if type_of_zone and type_of_zone.value == 4:
            return True
        return False

    def __reinitialize_data(self) -> None:
        """this method reinitialize data of this instance
            like visited and queue

        Args:
            None
        Returns:GraphBuilder
            None
        """
        self.visited = []
        self.queue = deque()

    def __is_valid_neighbor(self, current: str, neighbor: str) -> bool:
        """is valid neighbor check connection between current and neighbor
            is not None and has flow to move drone otherwise is not valid
        Args:
            current: (str): name of current hub
            neighbor: (str): name of next_hub or neighbor
        Returns:
            boolean: True if can go throw hub otherwise return False
        """
        connection = self._graph.get_connection_by_names(
            current,
            neighbor
        )
        next_hub = self._graph.get_hub_by_name(neighbor)

        if connection is None or next_hub is None:
            return False
        if self.__not_available_to_move(connection, next_hub):
            return False
        return True

    def __add_to_queue(self, path: list[str], neighbor: str) -> None:
        """add to queue new tuple neighbor and path

        Args:
            path: (list[str]): path from start to hub before neighbor
            neighbor: (str): neighbor should be added to new_path
        Returns:
            None
        """
        self.visited.append(neighbor)
        new_path = self.__create_new_path_with_neighbor(
            path, neighbor
        )
        self.queue.append((neighbor, new_path))
        return None

    def __create_new_path_with_neighbor(
        self, path: list[str], neighbor: str
    ) -> list[str]:
        """this method create new list from list path
            and append to it new string neighbor

        Args:
            path: (list[str]): list of strings contain names of hubs
            neighbor: (str): new string to append to new list
        Returns:
            new_path: (list[str]): path append to it neighbor
        """
        new_path = list(path)
        new_path.append(neighbor)
        return new_path

    def __not_available_to_move(
        self,
        connection: Connection,
        next_hub: Hub
    ) -> bool:
        """not available to move check connection and next_hub
            has available flow to move
            at least 1 flow in connection and 1 flow in next_hub

        Args:
            connection: (Connection): check this connection has flow at least 1
            next_hub: (Hub): this Hub can contain another drone or drones
        Returns:
            bool: if has both at least available drones 1 or greather
                return True
            otherwise return False
        """
        if connection.available_drones < 1:
            return True
        elif next_hub.available_drones < 1:
            return True
        return False
