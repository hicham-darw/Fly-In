import sys
from time import sleep

from DataClasses import ParsedData, PathsAndFlow
from Drone import Drone
from Enums import TypeZone
from GraphBuilder import GraphBuilder
from Enums import MetaDataOfHub
from EdmondsKarpAlgo import EdmondsKarpAlgo
from Visualizer import Visualizer


class DroneFlowEngine:
    """engine of simulation made drones can traverse between hubs
    and track each one to reach goal
    """
    def __init__(self, parsed_data: ParsedData) -> None:
        """Constructor engine of flow drones

        Args:
            graph (GraphBuilder):
                [graph to simulate hubs and connection between them]
            drones (list[Drone]): [drones]
        Return:
            None
        """
        self.__parsed_data = parsed_data
        self.__graph: GraphBuilder = self.__build_graph()
        self.__algo: EdmondsKarpAlgo = EdmondsKarpAlgo(self.__graph)
        self.__drones: list[Drone] = self.__create_drones()

        self.turns_simulation = 0

    def __build_graph(self) -> GraphBuilder:
        """build graph by parsed_data passed to constructor

        Args:
            None
        Returns:
            GraphBuilder: [completely graph to use with helpful functions]
        """
        graph = GraphBuilder()
        (graph.build_start_hub(self.__parsed_data['start_hub'])
         .build_end_hub(self.__parsed_data['end_hub'])
         .build_hubs(self.__parsed_data['hubs'])
         .build_connections(self.__parsed_data['connections'])
         .build_adjacency_list())
        return graph

    def __create_drones(self) -> list[Drone]:
        """create Drones to simulate agents
        Args:
            number_of_drones: (int): number_of_drones
        None:
            None
        """
        drones: list[Drone] = list()
        for i in range(self.__parsed_data['nb_drones']):
            drones.append(Drone(i + 1))
        return drones

    # setter method
    def set_drones_in_start_hub(self) -> None:
        """set all drones to start_hub to start simulation

        Args:
            None
        Return:
            None
        """
        start_hub = self.__graph.get_start_hub()
        if start_hub.drones is None:
            start_hub.drones = []
        for drone in self.__drones:
            start_hub.drones.append(drone)

    # getters method ----------------->
    def get_number_of_drones(self) -> int:
        """get number of drones

        Args:
            None
        Returns:
            int: number of drones
        """
        return len(self.__drones)

    def execute_simulation(self) -> None:
        """put drones in start_hub and starting simulation

        Args:
            None
        Returns:
            None
        """
        self.set_drones_in_start_hub()
        self.__graph.reset_capacities()
        all_data: list[PathsAndFlow] = self.__algo.run()
        if not all_data:
            print(
                "Error: No path found! from start hub to end hub.",
                file=sys.stderr
            )
            sys.exit(42)
        self.start_simulation(all_data)

    def not_reaches_goal(self) -> bool:
        """check every simulation id all drones reaches to goal hub

        Args:
            None
        Returns:
            bool : if drones end hub still None or not have all drones
                return True.
                otherwise return False
        """
        if len(self.__graph.get_end_hub().drones) != len(self.__drones):
            return True
        return False

    def start_simulation(
        self, all_data: list[PathsAndFlow]
    ) -> None:
        """start routing drones in between hubs
        Args:
            all_data (list[PathsAndFlow]): [contains path flow and turns]
        """
        while self.not_reaches_goal():
            self.simulate_turn(all_data)

    def simulate_turn(self, all_data: list[PathsAndFlow]) -> None:
        """ function simulate 1 turn move all_drones from current_hub to next

        Args:
            all_data: list[] : all_data ned to run 1 turn
            and move drones to next

        Returns:
            None
        """
        for index_data in range(len(all_data)):
            path = all_data[index_data]['path']
            flow = all_data[index_data]['flow']

            i = len(path) - 2
            while i >= 0:
                self.move_drones_to_next_hub(path[i], path[i + 1], flow)
                i -= 1
        sleep(0.8)
        print()
        self.reset_all_drones_can_move()
        self.turns_simulation += 1

    def reset_all_drones_can_move(self) -> None:
        """reset drones after each move can move now

        Args:
            None
        Returns:
            None
        """
        for drone in self.__drones:
            drone.set_is_moved_in_turn(False)

    def move_drone_has_restricted_zone(
        self,
        current_hub_name: str,
        next_hub_name: str
    ) -> None:
        """ move drones to restricted zone each drone must take 2 moves

        Args:
            current_hub : drone start flyin to
            next_hub_name: next move drones stop on it
        Returns:
            None
        """
        current_hub = self.__graph.get_hub_by_name(current_hub_name)
        next_hub = self.__graph.get_hub_by_name(next_hub_name)
        if current_hub is None or next_hub is None:
            return None

        conn = self.__graph.get_connection_by_names(
            current_hub.name, next_hub.name
        )
        if conn is None:
            return None

        if len(conn.drones) > 0:
            if next_hub.drones is None:
                next_hub.drones = []
            drone_in_conn = conn.drones.pop(0)
            if drone_in_conn.can_move_to_next_hub() is True\
                    and drone_in_conn.get_is_moved_in_turn() is False:
                next_hub.drones.append(drone_in_conn)
                drone_in_conn.set_is_moved_in_turn(True)
                text_move = self.__move_format(
                    str(drone_in_conn.get_drone_id()), next_hub.name
                )
                Visualizer.colored_print(
                    text_move, next_hub.metadata['color'], None
                )
                if next_hub == self.__graph.get_end_hub():
                    drone_in_conn.set_can_move(False)

        if not current_hub.drones:
            return

        drone = current_hub.drones.pop(0)
        if drone.can_move_to_next_hub() is True\
                and drone.get_is_moved_in_turn() is False:
            conn.drones.append(drone)
            drone.set_is_moved_in_turn(True)
            text_move = self.__move_format(
                str(drone.get_drone_id()),
                conn.zone_one + '-' + conn.zone_two
            )
            Visualizer.colored_print(text_move, "white", "connection")

    def __move_format(self, drone_id: str, hub_name: str) -> str:
        """this prepare format output of drone move

        Args:
            drone_id: (str): drone id as string
            hub_name: (str): name of next_hub
        Returns:
            new_str: (str): output format
        """
        return 'D' + drone_id + '-' + hub_name + ' '

    def move_drone_has_not_restricted_zone(
        self, current_hub_name: str, next_hub_name: str
    ) -> None:
        """move drones is normal or preferred zone cost 1 move

        Args:
            current_hub_name: name of current_hub
            next_hub_name: name of next_hub

        Returns:
            None
        """
        current_hub = self.__graph.get_hub_by_name(current_hub_name)
        next_hub = self.__graph.get_hub_by_name(next_hub_name)
        if current_hub is None or next_hub is None:
            return None

        if not current_hub.drones:
            return

        drone = current_hub.drones[0]
        if drone.can_move_to_next_hub() is True\
                and drone.get_is_moved_in_turn() is False:
            drone = current_hub.drones.pop(0)
            next_hub.drones.append(drone)
            drone.set_is_moved_in_turn(True)
            text_move = self.__move_format(
                str(drone.get_drone_id()), next_hub.name
            )
            Visualizer.colored_print(
                text_move, next_hub.metadata['color'], None
            )
            if next_hub == self.__graph.get_end_hub():
                drone.set_can_move(False)

    def move_drones_to_next_hub(
        self, current_hub_name: str, next_hub_name: str, flow: int
    ) -> None:
        """like manager count how many drones can fly to next hub

        Args:
            current_hub_name: name of current_hub
            next_hub_name: name of next hub
        Returns:
            None
        """
        next_hub = self.__graph.get_hub_by_name(next_hub_name)
        while flow:
            if next_hub and next_hub.metadata[MetaDataOfHub.zone.name].value\
                    == TypeZone.restricted.value:
                self.move_drone_has_restricted_zone(
                    current_hub_name, next_hub_name
                )
            else:
                self.move_drone_has_not_restricted_zone(
                    current_hub_name, next_hub_name
                )
            flow -= 1
