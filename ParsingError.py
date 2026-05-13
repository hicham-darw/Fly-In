class ParsingError(Exception):
    """Custom Exception if found error when parsing files
    """
    def __init__(self, line: str, line_number: int, error: str) -> None:
        """Constructor of object

        Args:
            msg: (str): msg of error raised
        Returns:
            None
        """

        super().__init__(
            f"line {line_number}: '{line} {error}."
        )


class SyntaxLineError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "Inavalid format")


class DuplicateNbDronesError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "Already exist")


class DuplicateConnectionError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "Connection Already exist")


class DuplicateNameHub(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "name hub Already exist")


class DuplicateCoordintesError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "coordintes already exist")


class NotFoundNameHubError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "name hub not found")


class ValueNbDronesError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(
            line, line_number, "nb_drones must be integer greather than Zero"
        )


class InvalidFirstLineError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(
            line, line_number, "first line must start with format nb_drones:"
        )


class PrefixError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(
            line, line_number, "starts with different Prefix"
        )


class KeyMetadataError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "Invalid Key")


class TypeZoneError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "invalid type zone")


class ColorZoneError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "invalid color zone")


class MaxDronesError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "invalid max drones")


class KeyValMetadataError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(line, line_number, "metadata must (key)=(value)")


class MaxLinkCapacityError(ParsingError):
    def __init__(self, line: str, line_number: int) -> None:
        super().__init__(
            line, line_number, "max_lin_capacity must be positive number"
        )
