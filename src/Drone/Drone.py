class Drone:
    """class Drone to track drones
    each drone has a unique id

    """
    def __init__(self, drone_id: int) -> None:
        """Constructor to create an instance

        Args:
            drone_id: (int): unique int number
        Return:
            None
        """
        self.__drone_id = drone_id
        self.__can_move = True

    # getter method

    def get_drone_id(self) -> int:
        """getter method for incapsulation get drone id

        Args:
            None:
        returns:
            self.__drone_id: (int): drone id
        """
        return self.__drone_id

    def can_move_to_next_hub(self) -> bool:
        return self.__can_move

    def set_cant_move(self) -> None:
        self.__can_move = False
