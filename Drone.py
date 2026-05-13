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
        self.__is_moved_in_turn = False
        self.__drone_id = drone_id
        self.__can_move = True

    # getter methods
    def get_drone_id(self) -> int:
        """getter method for incapsulation get drone id

        Args:
            None:
        returns:
            self.__drone_id: (int): drone id
        """
        return self.__drone_id

    def get_is_moved_in_turn(self) -> bool:
        """get drone is moved in one turn

        Args:
            None
        returns:
            boolean: True if already moved in this turn otherwise
                return False
        """
        return self.__is_moved_in_turn

    # setter methods
    def set_can_move(self, bool: bool) -> None:
        """setter method set drone if reaches goal can't move

        Args:
            bool: (bool) set True if traverse between hubs otherwise
                set False
        Retuns:
            None
        """
        self.__can_move = bool

    def set_is_moved_in_turn(self, bool: bool) -> None:
        self.__is_moved_in_turn = bool

    def can_move_to_next_hub(self) -> bool:
        return self.__can_move
