from dataclasses import dataclass, field
from typing import TypedDict
from Enums import TypeZone
from Drone import Drone


class HubMetadata(TypedDict):
    """HubMetadata custom dictionary
        contain specific data

    Attributes:
        zone: (TypeZone): type zone of hub
        color: (str | None): color of hub
        max_drones: int: hub how can take number of drones
    """
    zone: TypeZone
    color: str | None
    max_drones: int


class ConnectionMetadata(TypedDict):
    """ConnectionMetadata custom dictionary
        contain specific data
    Attributes:
        max_link_capacity: (int): max_link can traverse in connetcion
    """
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

    zone_one: str
    zone_two: str
    metadata: ConnectionMetadata
    available_drones: int = 0
    drones: list[Drone] = field(default_factory=list)


class PathsAndFlow(TypedDict):
    """custom dictionary represent path and flow and turns

    Attributes:
        path: (list[str]): path to end_hub
        flow: (int): many drones can move in this path
        turns: (int): how can take turns to reach to end_hub
    """
    path: list[str]
    flow: int
    turns: int


class ParsedData(TypedDict):
    """custom dictionary represent parsed data

    Attributes:
        nb_drones: (int): number of drones
        start_hub: (Hub): start hub
        end_hub: (Hub): end_hub
        hubs: (list[Hub]): regular hubs
        connections: (list[Connection]): connections or vertices between hubs
    """
    nb_drones: int
    start_hub: Hub
    end_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
