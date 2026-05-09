from enum import Enum


class TypeZone(Enum):
    priority = 1
    normal = 2
    restricted = 3
    blocked = 4


class MetaDataOfHub(Enum):
    zone = 1
    color = 2
    max_drones = 3


class MetaDataOfConnection(Enum):
    max_link_capacity = 1
