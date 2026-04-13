class Hub:
    def __init__(self, type, name, x, y, metadata) -> None:
        self.type: str = type
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.metadata: dict[str, str] | None = metadata
