class Drone:
    def __init__(self, drone_id, name_of_hub):
        self.drone_id = drone_id
        self.name_of_hub = name_of_hub

    def move_drone_to_hub(self, name_of_hub):
        self.name_of_hub = name_of_hub
