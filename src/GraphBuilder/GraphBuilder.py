from src.Zone.Zone import Hub, Connection
from typing_extensions import Self
from src.Enums.Enums import TypeZone


class GraphBuilder:

    def __init__(self) -> None:
        """Constructor method take only required like start_hub and end_hub
            initial attributes of object only
        Args:
            None
        Returns:
            None
        """
        self.__start_hub: Hub = None
        self.__hubs: list[Hub]= []
        self.__end_hub: Hub = None
        self.__connections: list[Connection] = list()
        self.__adjacency_list: dict[str, list[str]] = dict()

    def build_start_hub(self, start_hub: Hub) -> Self:
        """setter method set start_hub

        Args:
            start_hub: Hub where start all drones

        Returns:
            self: Self return Same object
        """
        if self.__start_hub is None:
            self.__start_hub = start_hub
        return self

    def build_end_hub(self, end_hub: Hub) -> Self:
        """setter method set end_hub

        Args:
            start_hub: (Hub): where all_drones should reach it

        Returns:
            self: (Self): return Same object
        """
        if self.__end_hub is None:
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
        for hub in hubs:
            self.__hubs.append(hub)
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

        for conn in self.__connections:
            if self.__adjacency_list.get(conn.zone1, None) is None:
                self.__adjacency_list[conn.zone1] = []
            if self.__adjacency_list.get(conn.zone2, None) is None:
                self.__adjacency_list[conn.zone2] = []

            pos = self.get_position_in_adjacency_list(conn.zone2, self.__adjacency_list[conn.zone1])
            self.__adjacency_list[conn.zone1].insert(pos, conn.zone2)

            pos = self.get_position_in_adjacency_list(conn.zone1, self.__adjacency_list[conn.zone2])
            self.__adjacency_list[conn.zone2].insert(pos, conn.zone1)
        return self
    
    # getter methods
    def get_position_in_adjacency_list(self, name_hub: str, lst: list[str]) -> int:
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

    def get_connection_by_names(self, current_hub: str, next_hub: str) -> Connection | None:
        """Getter method
            get edge betwen two hubs by their name

        Args:
            current_hub (str): [first hub name]
            next_hub (str): [second hub name]

        Returns:
            Connection: [edge Object contains own data]
        """
        for conn in self.__connections:
            if conn.zone1 == current_hub and conn.zone2 == next_hub:
                return conn
            elif conn.zone2 == current_hub and conn.zone1 == next_hub:
                return conn
        return None

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
            if conn.zone1 == current_hub and conn.zone2 == next_hub:
                return conn.available_drones
            elif conn.zone2 == current_hub and conn.zone1 == next_hub:
                return conn.available_drones
        return -1

    def get_type_of_zone(self, name_hub: str) -> TypeZone:
        """Return the zone type associated with a hub name.

        Args:
            name_hub: The name of the hub.

        Returns:
            The zone type associated with the hub.
        """
        if self.get_start_hub() and name_hub == self.get_start_hub().name:
            return self.get_start_hub().metadata.get('zone')
        
        if self.get_end_hub() and name_hub == self.get_end_hub().name:
            return self.get_end_hub().metadata.get('zone')
        else:
            for hub in self.get_regular_hubs():
                if name_hub == hub.name:
                    return hub.metadata.get('zone')

    def build(
        self,
        graph_data: dict[str, list[Hub] | Hub | int | list[Connection]]
    ) -> None:
        """build my graph object step by step
        Args:
            dictionary (dict): all_parsed_data from parser
            nb_drones: int: number of drones
            start_hub: Hub: start all drones
            end_hub: Hub: all drones target this hub
            hubs: list[hub]: hubs between start and end can has no \
                    connection between other hubs
            connections: list[Connection]: edges between two hubs
        
        Returns:
            None
        """
        self.build_start_hub(graph_data.get('start_hub'))\
        .build_end_hub(graph_data.get('end_hub'))\
        .build_hubs(graph_data.get('hubs'))\
        .build_connections(graph_data.get('connections'))\
        .build_adjacency_list()
