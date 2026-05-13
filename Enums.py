from enum import Enum


class TypeZone(Enum):
    """Enum of Type Zone Each type has value
    """
    priority = 1
    normal = 2
    restricted = 3
    blocked = 4


class MetaDataOfHub(Enum):
    """Enum metadata of hub each name has value
    """
    zone = 1
    color = 2
    max_drones = 3


class MetaDataOfConnection(Enum):
    """enum metadata of connection max_link has value 1
    """
    max_link_capacity = 1
