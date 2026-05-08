import sys
from src.Drone.Drone import Drone
from src.Enums.Enums import TypeZone
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.Enums.Enums import MetaDataOfHub
from src.Algorithms.EdmondsKarpAlgo import EdmondsKarpAlgo
from src.Color.Color import ColorsRGB
from src.Algorithms.Algo import Algo
from time import sleep
import webcolors
from src.Parser.Parser import Parser

class DroneFlowEngine:
    """engine of simulation made drones can traverse between hubs
    and track each one to reach goal
    """
    def __init__(self) -> None:
        """Constructor engine of flow drones

        Args:
            graph (GraphBuilder): [graph to simulate hubs and connection between them]
            drones (list[Drone]): [drones]
        Return:
            None
        """
        self.__parsed_data = None
        self.__algo = None

        self.__graph = None
        self.__drones: list[Drone] = []

        self.turns_simulation = 0

    def init_algo(self) -> None:
        self.__algo = EdmondsKarpAlgo(self.__graph)

    def parse_file(self) -> None:
        self.__parser = Parser(sys.argv[1])
        self.__parser.parse()
        self.__parsed_data = self.__parser.get_parsed_data()

    def init_graph(self) -> None:
        graph_builder = GraphBuilder()
        graph_builder.build_start_hub(self.__parsed_data.get('start_hub'))\
        .build_end_hub(self.__parsed_data.get('end_hub'))\
        .build_hubs(self.__parsed_data.get('hubs'))\
        .build_connections(self.__parsed_data.get('connections'))\
        .build_adjacency_list()
        
        self.__graph = graph_builder
    
    def create_drones(self) -> None:
        """create Drones to simulate fly-in
        Args:
            number_of_drones: (int): number_of_drones
        None:
            None
        """
        for i in range(self.__parsed_data['nb_drones']):
            self.__drones.append(Drone(i + 1))

    # setter method
    def set_drones_in_start_hub(self) -> None:
        """set all drones to start_hub to start simulation

        Args:
            None
        Return:
            None
        """
        if self.__graph.get_start_hub().drones is None:
            self.__graph.get_start_hub().drones = []

        for drone in self.__drones:
            self.__graph.get_start_hub().drones.append(drone)

    # getters method ----------------->
    def get_number_of_drones(self) -> int:
        """get number of drones

        Args:
            None
        Returns:
            int: number of drones
        """
        return self.__nb_drones

    def execute_simulation(self) -> None:
        """put drones in start_hub and starting simulation

        Args:
            None        
        Returns:
            None
        """
        self.set_drones_in_start_hub()
        self.__graph.reset_capacities()
        all_data = self.__algo.run()
        for d in all_data:
            print(d)
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
        if self.__graph.get_end_hub().drones is None:
            return True
        elif len(self.__graph.get_end_hub().drones) != len(self.__drones):
            return True
        return False

    def start_simulation(
        self, all_data: list[dict[str, list[str | Drone] | int]]
    ) -> None:

        while self.not_reaches_goal():
            self.simulate_turn(all_data)

    def simulate_turn(self, all_data: list[dict[str, list[str | Drone] | int]]) -> None:
        """ function simulate 1 turn move all_drones from current_hub to next_hub

        Args:
            all_data: list[] : all_data ned to run 1 turn and move drones to next hub

        Returns:
            None
        """
        for index_data in range(len(all_data)):
            path = all_data[index_data]['path']
            flow = all_data[index_data]['flow']

            i = 0
            while i < len(path) - 1: 
                next_hub = self.__graph.get_hub_by_name(path[i + 1])
                if next_hub.drones is None:
                    break
                i += 1
            if i == len(path) - 1:
                i -= 1

            while i >= 0:
                self.move_drones_to_next_hub(path[i], path[i + 1], flow)
                i -= 1
        sleep(0.8)
        print("\033[1J\033[1H", end='')
        self.turns_simulation += 1

    def move_drone_has_restricted_zone(self, current_hub_name: str, next_hub_name: str) -> None:
        """ move drone if nect_hub is restricted should check connection 
            if has simulation not completed

        Args:
            current_hub : drone start flyin to
            next_hub_name: next move drones stop on it
        Returns:
            None
        """
        current_hub = self.__graph.get_hub_by_name(current_hub_name)
        next_hub = self.__graph.get_hub_by_name(next_hub_name)
        conn = self.__graph.get_connection_by_names(current_hub.name, next_hub.name)
        if conn.drones is None:
            conn.drones = []

        if len(conn.drones) > 0:
            if next_hub.drones is None:
                next_hub.drones = []
            drone_in_conn = conn.drones.pop(0)
            if drone_in_conn.can_move_to_next_hub() is True:
                next_hub.drones.append(drone_in_conn)
                text_move = 'D' + str(drone_in_conn.get_drone_id()) + '-' + next_hub.name + ' ' 
                self.colored_print(text_move, next_hub.metadata['color'])        
                if next_hub == self.__graph.get_end_hub():
                    drone_in_conn.set_cant_move()
    
        if not current_hub.drones:
            return

        drone = current_hub.drones.pop(0)
        if drone.can_move_to_next_hub() is True:
            conn.drones.append(drone)
            text_move = 'D' + str(drone.get_drone_id()) + '-' + conn.zone1 + '-' + conn.zone2 + ' '
            self.colored_print(text_move, "white", "connection")

    def colored_print(self, move_action: str, color: str, connection=None) -> None:
            
        if color is None:
            color = 'white'
        try:
            rgb = webcolors.name_to_rgb(color.lower())
        except ValueError as e:
            rgb = webcolors.name_to_rgb('white')
        colored = '\033[38;2;' + str(rgb.red) + ';' + str(rgb.green) + ';' + str(rgb.blue) + 'm' 
        if connection is not None:
            colored += " \033[5m"
        print(colored, end='', flush=True)
        for c in move_action:
            print(c, end='', flush=True)
            sleep(0.008)
        print('\033[0m \033[25m', end='', flush=True)            

    def move_drone_has_not_restricted_zone(self, current_hub_name: str, next_hub_name: str) -> None:
        """move drones is normal or preferred zone is only move drones  to next hub

        Args:
            current_hub_name: name of current_hub
            next_hub_name: name of next_hub

        Returns:
            None
        """

        current_hub = self.__graph.get_hub_by_name(current_hub_name)
        next_hub = self.__graph.get_hub_by_name(next_hub_name)

        if next_hub.drones is None:
            next_hub.drones = []

        if not current_hub.drones:
            return

        try:
            drone = current_hub.drones.pop(0)
        except IndexError:
            return
        if drone.can_move_to_next_hub() is True:
            next_hub.drones.append(drone)
            text_move = 'D' + str(drone.get_drone_id()) + '-' + next_hub.name + ' '
            self.colored_print(text_move, next_hub.metadata['color'])
            if next_hub == self.__graph.get_end_hub():
                drone.set_cant_move()

    def move_drones_to_next_hub(self, current_hub_name: str, next_hub_name: str, flow: int) -> None:
        """like manager count how many drones can fly to next hub
        Args:
            current_hub_name: name of current_hub
            next_hub_name: name of next hub
        
        Returns:
            None
        """
        next_hub = self.__graph.get_hub_by_name(next_hub_name)
        while flow:
            if next_hub.metadata[MetaDataOfHub.zone.name].value == TypeZone.restricted.value:
                self.move_drone_has_restricted_zone(current_hub_name, next_hub_name)
            else:
                self.move_drone_has_not_restricted_zone(current_hub_name, next_hub_name)
            flow -= 1
