from dataclasses import dataclass, field
from typing import TypedDict
from src.Enums.Enums import TypeZone
from src.Drone.Drone import Drone


class HubMetadata(TypedDict):
    zone: TypeZone
    color: str | None
    max_drones: int


class ConnectionMetadata(TypedDict):
    max_link_capacity: int


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

    type_zone: str
    name: str
    x: int
    y: int
    metadata: HubMetadata
    drones: list[Drone] = field(default_factory=list)
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
    metadata: ConnectionMetadata
    available_drones: int = 0
    drones: list[Drone] = field(default_factory=list)


class PathsAndFlow(TypedDict):
    path: list[str]
    flow: int
    turns: int


class ParsedData(TypedDict):
    nb_drones: int
    start_hub: Hub
    end_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
