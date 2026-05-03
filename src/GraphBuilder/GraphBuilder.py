from src.Zone.Zone import Hub, Connection
from typing_extensions import Self
from src.Enums.Enums import TypeZone, MetaDataOfHub
from src.Drone.Drone import Drone


class GraphBuilder:

    def __init__(self) -> None:
        """Constructor method take only required like start_hub and end_hub
            initial attributes of object only
        Args:
            None
        Returns:
            None
        """
        self.__nb_drones: int = 0
        self.__start_hub: Hub = None
        self.__hubs: list[Hub]= []
        self.__end_hub: Hub = None
        self.__connections: list[Connection] = list()

        self.__adjacency_list: dict[str, list[str]] = dict()
    
    #  setter methods for builder
    def set_number_of_drones(self, number_of_drones: int) -> Self:
        """setter method
            set number of drones
        Args:
            number_of_drones: [number of drones can fly to end_hub]
        Return:
            self: Self same object
        """
        if self.__nb_drones == 0:
            self.__nb_drones = number_of_drones
        return self

    def set_start_hub(self, start_hub: Hub) -> Self:
        """setter method set start_hub

        Args:
            start_hub: Hub where start all drones

        Returns:
            self: Self return Same object
        """
        if self.__start_hub is None:
            self.__start_hub = start_hub
        return self

    def set_end_hub(self, end_hub: Hub) -> Self:
        """setter method set end_hub

        Args:
            start_hub: (Hub): where all_drones should reach it

        Returns:
            self: (Self): return Same object
        """
        if self.__end_hub is None:
            self.__end_hub = end_hub
        return self

    def set_hubs(self, hubs: list[Hub]) -> Self:
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

    def set_connections(self, connections: list[Connection]) -> Self:
        """ setter method
            set new_connections
        Args:
            hubs (list[Hub]): [hubs can added them to graph]
        
        Returns:
            self: (Self): return same object
        """
        self.__connections = connections
        return self

    def set_adjacency_list(self) -> Self:
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

    
    def get_number_of_drones(self) -> int:
        """get number of drones
        
        Args:
            None
        
        Returns:
            int: number of drones
        """
        return self.__nb_drones
    
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
        for current, neighbors in self.__adjacency_list.items():
            for neighbor in neighbors:
                if current == current_hub and neighbor == next_hub:
                    conn = self.get_connections() 
        for conn in self.__connections:
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
        flow = 0
        for i in range(len(path_to_exit) - 1):
            
            flow_conn = self.get_flow_connection(path_to_exit[i], path_to_exit[i + 1])
            flow_hub = self.get_hub_by_name(path_to_exit[i + 1]).available_drones

            if flow_conn is None or flow_hub is None:
                break

            if flow_hub < flow_conn:
                if i == 0:
                    flow = flow_hub
                elif flow > flow_hub:
                    flow = flow_hub
            else:
                if i == 0:
                    flow = flow_conn
                elif flow > flow_conn:
                    flow = flow_conn
        return flow

    def build(self, graph_data: dict[str, list[Hub] | Hub | int | list[Connection]]) -> None:
        self.set_number_of_drones(graph_data.get('nb_drones'))\
        .set_start_hub(graph_data.get('start_hub'))\
        .set_end_hub(graph_data.get('end_hub'))\
        .set_hubs(graph_data.get('hubs'))\
        .set_connections(graph_data.get('connections')).set_adjacency_list()

    # update data
    def move_drone_has_restricted_zone(self, current_hub_name: str, next_hub_name: str):
        current_hub = self.get_hub_by_name(current_hub_name)
        next_hub = self.get_hub_by_name(next_hub_name)
        conn = self.get_connection_by_names(current_hub.name, next_hub.name)
        if conn.drones is None:
            conn.drones = []

        if len(conn.drones) > 0:
            if next_hub.drones is None:
                next_hub.drones = []

            drone_in_conn = conn.drones.pop(0)
            next_hub.drones.append(drone_in_conn)                    

        if not current_hub.drones:
            return

        drone = current_hub.drones.pop(0)
        conn.drones.append(drone)
    
    def move_drone_has_not_restricted_zone(self, current_hub_name: str, next_hub_name: str):
        current_hub = self.get_hub_by_name(current_hub_name)
        next_hub = self.get_hub_by_name(next_hub_name)

        if next_hub.drones is None:
            next_hub.drones = []

        if not current_hub.drones:
            return

        try:
            drone = current_hub.drones.pop(0)
        except IndexError:
            return
        next_hub.drones.append(drone)

    def move_drones_to_next_hub(self, current_hub_name: str, next_hub_name: str, flow: int) -> None:
        current_hub = self.get_hub_by_name(current_hub_name)
        next_hub = self.get_hub_by_name(next_hub_name)
        while flow:
            if next_hub.metadata[MetaDataOfHub.zone.name].value == TypeZone.restricted.value:
                self.move_drone_has_restricted_zone(current_hub_name, next_hub_name)
            else:
                self.move_drone_has_not_restricted_zone(current_hub_name, next_hub_name)
            flow -= 1
