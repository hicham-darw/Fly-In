class Hub:
    def __init__(self, typee, name, x, y, metadata) -> None:
        self.type: TypeZone = typee
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.metadata: dict[str, str] | None = metadata

class Connection:
    def __init__(self, zone1: str, zone2: str, metadata: dict[str, int] | None) -> None:
        self.zone1 = zone1
        self.zone2 = zone2
        self.metadata = metadata