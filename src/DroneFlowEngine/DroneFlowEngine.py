from collections import deque
from src.Drone.Drone import Drone
from src.Enums.Enums import TypeZone
from src.GraphBuilder.GraphBuilder import GraphBuilder
from src.Enums.Enums import MetaDataOfHub
from src.EdmondsKarpAlgo.EdmondsKarpAlgo import EdmondsKarpAlgo
from termcolor import cprint


class DroneFlowEngine:

    def __init__(self, graph: GraphBuilder, algo: EdmondsKarpAlgo, number_of_drones: int) -> None:
        """Constructor engine of flow drones

        Args:
            graph (GraphBuilder): [graph to simulate hubs and connection between them]
            drones (list[Drone]): [drones]
        """
        self.__nb_drones = number_of_drones
        
        self.__graph = graph
        self.__algo = algo
        self.__drones: list[Drone] = []

        self.turns_simulation = 0
        
        self.visited = []

    # setter method
    def set_drones_in_start_hub(self) -> None:
        self.__drones = []
        for i in range(self.__nb_drones):
            self.__drones.append(Drone(i + 1))
        self.__graph.get_start_hub().drones = self.__drones

    # getters method ----------------->
    def get_number_of_drones(self) -> int:
        """get number of drones
        
        Args:
            None
        
        Returns:
            int: number of drones
        """
        return self.__nb_drones

    def run(self) -> None:
        """put drones in start_hub and starting simulation
        
        Args:
            None
        
        Returns:
            None
        """
        self.set_drones_in_start_hub()
        self.__algo.reset_capacities()
        all_data = self.__algo.edmonds_karp()
        for d in all_data:
            print(d)
        self.start_simulation(all_data)
        
    def start_simulation(
        self, all_data: list[dict[str, list[str | Drone] | int]]
    ) -> None:

        while self.__graph.get_end_hub().drones is None or len(self.__graph.get_end_hub().drones) != self.__nb_drones:
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
        print()
        self.turns_simulation += 1

    def move_drone_has_restricted_zone(self, current_hub_name: str, next_hub_name: str) -> None:
        """ move drone if nect_hub is restricted should check connection 
            if has simulation not completed
        
        Args:
            current_hub : drone start flyin to
            next_hub_name: next move drones stop on it
        Returns:

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
            next_hub.drones.append(drone_in_conn)
            text_move = 'D<' + str(drone_in_conn.drone_id) + '>-<' + next_hub.name + '> ' 
            try:
                cprint(f"{text_move}", next_hub.metadata.get('color'), end='')
            except KeyError:
                cprint(f"{text_move}", "red",end='')
        if not current_hub.drones:
            return

        drone = current_hub.drones.pop(0)
        conn.drones.append(drone)
        text_move = 'D<' + str(drone.drone_id) + '>-<' + conn.zone1 + '-' + conn.zone2 + '> '
        cprint(f"{text_move}", end='') 

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
        next_hub.drones.append(drone)
        text_move = 'D<' + str(drone.drone_id) + '>-<' + next_hub.name + '> '
        try:
            cprint(f"{text_move}", next_hub.metadata.get('color', 'white'), end='')
        except KeyError:
            cprint(f"{text_move}", end='')

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
