from pydantic import BaseModel, Field, model_validator
from typing import Any, Annotated
from enum import Enum


class ZoneType(Enum):
    start_hub = "start_hub"
    end_hub = "end_hub"
    hub = "hub"


class TypeDataZone(Enum):
    normal = "normal"
    blocked = "blocked"
    restricted = "restricted"
    priority = "priority"


class DataZone(BaseModel):
    zone: TypeDataZone = Field(default=TypeDataZone.normal)
    color: str = Field(default=None)
    max_drones: int = Field(default=1)

    @model_validator(mode='before')
    @classmethod
    def clean_data(cls, data: dict[str, Any]) -> dict[str: Any]:
        if not data['zone']:
            data['zone'] = TypeDataZone.normal
        if not data['max_drones']:
            data['max_drones'] = 1
        return data


class Zone(BaseModel):
    type: ZoneType
    name: Annotated[str, Field(min_length=3), Field(max_length=10)]
    x: int
    y: int
    metadata: DataZone


class Connection(BaseModel):
    zone_from: str
    zone_to: str
    max_capacity: int = Field(default=1)
