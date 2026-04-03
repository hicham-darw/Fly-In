class ParsingError(Exception):
    def __init__(self) -> None:
        super().__init__("Error: Parsing check file please!")
