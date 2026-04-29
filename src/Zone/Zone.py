from src.Enums.Enums import TypeZone
from dataclasses import dataclass
from src.Drone.Drone import Drone



@dataclass
class Hub:
    """Represent a zone node in the parsed graph.

    Attributes:
        type: Hub category such as start, end, or regular hub.
        name: Unique hub name.
        x: Horizontal coordinate.
        y: Vertical coordinate.
        metadata: Optional metadata associated with the hub.
    """

    type_zone: TypeZone
    name: str
    x: int
    y: int
    metadata: dict[str, str | int | TypeZone] | None = None
    drones: list[Drone] | None = None
    available_drones: int = 0


@dataclass
class Connection:
    """Represent an undirected connection between two zones.

    Attributes:
        zone1: Name of the first connected zone.
        zone2: Name of the second connected zone.
        metadata: Optional metadata associated with the connection.
    """

    zone1: str
    zone2: str
    metadata: dict[str, int] | None = None
    available_drones: int = 0
    drones: list[Drone] | None = None