from DataClasses import Hub, Connection
from typing_extensions import Self
from Enums import TypeZone


class GraphBuilder:
    """graph builder build graph with parsed data from parser
        is a builder :)
    """
    def build_start_hub(self, start_hub: Hub) -> Self:
        """setter method set start_hub

        Args:
            start_hub: Hub where start all drones
        Returns:
            self: Self return Same object
        """
        self.__start_hub: Hub = start_hub
        return self

    def build_end_hub(self, end_hub: Hub) -> Self:
        """setter method set end_hub

        Args:
            start_hub: (Hub): where all_drones should reach it
        Returns:
            self: (Self): return Same object
        """
        self.__end_hub = end_hub
        return self

    def build_hubs(self, hubs: list[Hub]) -> Self:
        """ setter method
            set new hubs to graph

        Args:
            hubs (list[Hub]): [hubs can added them to graph]
        Returns:
            self: (Self): return same object
        """
        self.__hubs: list[Hub] = hubs
        return self

    def build_connections(self, connections: list[Connection]) -> Self:
        """ setter method
            set new_connections
        Args:
            hubs (list[Hub]): [hubs can added them to graph]
        Returns:
            self: (Self): return same object
        """
        self.__connections = connections
        return self

    def build_adjacency_list(self) -> Self:
        """set an adjacency list nodes and edges.

        Args:
            connections: (Connection):The list of connections to add.
        Returns:
            self: (Self): return same object
        """
        self.__adjacency_list: dict[str, list[str]] = dict()
        for conn in self.__connections:

            if self.__adjacency_list.get(conn.zone_one, None) is None:
                self.__adjacency_list[conn.zone_one] = []
            if self.__adjacency_list.get(conn.zone_two, None) is None:
                self.__adjacency_list[conn.zone_two] = []

            pos = self.get_position_in_adjacency_list(
                conn.zone_two, self.__adjacency_list[conn.zone_one]
            )
            self.__adjacency_list[conn.zone_one].insert(pos, conn.zone_two)

            pos = self.get_position_in_adjacency_list(
                conn.zone_one, self.__adjacency_list[conn.zone_two]
            )
            self.__adjacency_list[conn.zone_two].insert(pos, conn.zone_one)
        return self

    # getter methods
    def get_position_in_adjacency_list(
        self,
        name_hub: str, lst: list[str]
    ) -> int:
        """Return the insertion index for a hub based on zone priority.

        Args:
            name_hub: The name of the hub to insert.
            lst: The current adjacency list that target it.
        Returns:
            The index at which the hub should be inserted. otherwise return 1
        """
        hub = self.get_hub_by_name(name_hub)
        if hub is None:
            return -1

        current_zone = hub.metadata.get('zone', TypeZone.normal)
        for index, elem in enumerate(lst):
            check_hub = self.get_hub_by_name(elem)
            if check_hub is None:
                return -1
            check_zone = check_hub.metadata.get('zone', TypeZone.normal)

            if isinstance(current_zone, TypeZone)\
                    and isinstance(check_zone, TypeZone):
                if current_zone.value < check_zone.value:
                    return index

        return len(lst)

    def get_adjacency_list(self) -> dict[str, list[str]]:
        """get adjacency list of graph

        Args:
            None:
        Returns:
            dictionary: adjacency list
        """
        return self.__adjacency_list

    def get_regular_hubs(self) -> list[Hub]:
        """get all regular hubs

        Args:
            None
        Returns:
            list: (list[hub]): all regular hubs inside graph
        """
        return self.__hubs

    def get_start_hub(self) -> Hub:
        """get start_hub where start all_drones

        Args:
            None:
        return:
            start_hub: Hub: hub where starting all_drons
        """
        return self.__start_hub

    def get_end_hub(self) -> Hub:
        """get end hub where Drones should arrive at the end hub.

        Args:
            None
        Returns:
            end_hub: (Hub): end hub
        """
        return self.__end_hub

    def get_connections(self) -> list[Connection]:
        """ get all connections or edges of graph

        Args:
            None
        Returns:
            connections: (list[Conection]): edges of graph
        """
        return self.__connections

    def get_hub_by_name(self, name_hub: str) -> Hub | None:
        """Return the hub object by matching a hub name.

        Args:
            name_hub: The name of the hub to look up.

        Returns:
            The matching hub, or None if no hub matches.
        """
        if self.__start_hub and name_hub == self.__start_hub.name:
            return self.__start_hub
        elif self.__end_hub and name_hub == self.__end_hub.name:
            return self.__end_hub
        elif self.__hubs:
            for hub in self.__hubs:
                if hub.name == name_hub:
                    return hub
        return None

    def get_connection_by_names(
        self,
        current_hub: str, next_hub: str
    ) -> Connection | None:
        """Getter method
            get edge betwen two hubs by their name

        Args:
            current_hub (str): [first hub name]
            next_hub (str): [second hub name]
        Returns:
            Connection: [edge Object contains own data]
        """
        for conn in self.__connections:
            if conn.zone_one == current_hub and conn.zone_two == next_hub:
                return conn
            elif conn.zone_two == current_hub and conn.zone_one == next_hub:
                return conn
        return None

    def get_type_of_zone(self, name_hub: str) -> TypeZone | None:
        """Return the zone type associated with a hub name.

        Args:
            name_hub: The name of the hub.
        Returns:
            The zone type associated with the hub.
        """
        hub = self.get_start_hub()
        if hub and name_hub == self.get_start_hub().name:
            return hub.metadata.get('zone', TypeZone.normal)

        if self.get_end_hub() and name_hub == self.get_end_hub().name:
            return self.get_end_hub().metadata.get('zone')
        else:
            for hub in self.get_regular_hubs():
                if name_hub == hub.name:
                    return hub.metadata.get('zone')
        return None

    # getters method
    def get_flow_connection(self, current_hub: str, next_hub: str) -> int:
        """getter method
            get_flow connection between two hubs

        Args:
            current_hub (str): [name of current hub]
            next_hub (str): [name of next hub]
        Returns:
            int: [flow between them or -1 if not find connection]
        """
        for conn in self.get_connections():
            if conn.zone_one == current_hub and conn.zone_two == next_hub:
                return conn.available_drones
            elif conn.zone_two == current_hub and conn.zone_one == next_hub:
                return conn.available_drones
        return -1

    def reset_capacities(self) -> None:
        """reset_capacities graph to run algo

        Args:
            None

        Returns:
            None
        """
        self.__reset_start_hub()
        self.__reset_end_hub()
        self.__reset_regular_hubs()
        self.__reset_connections()

    def __reset_start_hub(self) -> None:
        """reset start_hub capacity

        Args:
            None
        Returns:
            None
        """
        start_hub = self.get_start_hub()
        start_hub.available_drones = start_hub.metadata['max_drones']

    def __reset_end_hub(self) -> None:
        """Reset end_hub capacity

        Args:
            None
        Returns:
            None
        """
        end_hub = self.get_end_hub()
        end_hub.available_drones = end_hub.metadata['max_drones']

    def __reset_regular_hubs(self) -> None:
        """resert regular hubs capacities

        Args:
            None
        Returns:
            None
        """
        for hub in self.get_regular_hubs():
            hub.available_drones = hub.metadata['max_drones']

    def __reset_connections(self) -> None:
        """reste connections capacities

        Args:
            None
        Returns:
            None
        """
        for conn in self.get_connections():
            conn.available_drones = conn.metadata.get('max_link_capacity', 1)
