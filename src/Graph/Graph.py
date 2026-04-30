import sys
from src.Zone.Zone import Hub, Connection
from collections import deque
from src.Enums.Enums import TypeZone
from src.Drone.Drone import Drone

import sys


class Graph:
    """Represent the zone graph and the path-search helpers."""

    def __init__(self, start_hub: Hub, end_hub: Hub, hubs: list[Hub], nb_drones) -> None:
        """Initialize the graph from parsed hubs.

        Args:
            start_hub: The starting hub.
            end_hub: The destination hub.
            hubs: The intermediate hubs.
        """
        

