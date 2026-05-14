class ParsingError(Exception):
    """Custom Exception raises it when found error in map files
    """
    def __init__(self, line: str, line_number: int, error: str) -> None:
        """Raised parsing error when get error from parser file

        Args:
            msg: (str): msg of error raised
        Returns:
            None
        """
        self.red: str = "\033[1;31m"
        super().__init__(
            f"{self.red}line {line_number}: \"{line}\" {error}."
        )


class NotFoundError(Exception):
    """Raised when not found map requirements
    """
    def __init__(self, not_founded: str) -> None:
        """Initializ not found requirements

        Args:
            not_founded: what requirement not found
        """
        super().__init__(
            f"\033[1;31m{not_founded} not found!, please check map file."
        )


# Doesn't match syntax
class SyntaxLineError(ParsingError):
    """raised when a syntax line not valid
    """
    def __init__(self, line: str, line_number: int, msg: str) -> None:
        """Initialize the syntax line error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, f"Inavalid format:\033[0m {msg}")


class SyntaxHubError(SyntaxLineError):
    """Raised when line hub is invalid format
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid syntax hub

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(
            line, line_number, "<prefix>: <name> <x> <y> [optional metadata]"
        )


class SyntaxConnectionError(SyntaxLineError):
    """Raise when line connection is invalid format
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid syntax connection

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(
            line, line_number, "<prefix>: <hub1>-<hub2> [optional metadata]"
        )


class SyntaxDronesError(SyntaxLineError):
    """Raised when line nb_drones is inavlid
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid syntax nb_drones

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "<prefix>: <number of drones>")


class InvalidFirstLineError(ParsingError):
    """raised when first line not start by number of drones
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid first line error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(
            line, line_number, "first line must start with format nb_drones:"
        )


# duplicate Error
class DuplicateError(ParsingError):
    """Raised when found duplicated data in map file
    """
    def __init__(self, line: str, line_number: int, msg: str):
        """Initialize Duplicate Error when found duplicated.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, msg + " is duplicated")


class DuplicateNbDronesError(DuplicateError):
    """Raised when found line nb_drones duplicated
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize duplicated number of drones

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "nb_drones")


class DuplicateConnectionError(DuplicateError):
    """Raised when found duplicated connection in map file
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize duplicated connection error

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "Connection")


class DuplicateNameHub(DuplicateError):
    """Raised when found name hub duplicated
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize Duplicate Name hub error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "name hub")


class DuplicateCoordintesError(DuplicateError):
    """Raised when found duplicated coordinates in all hubs
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize Duplicate coordinates error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "coordinates")


class NotFoundNameHubError(ParsingError):
    """Raised when name hub not found in hubs
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize not found name in connection error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "name hub not found")


class ValueNbDronesError(ParsingError):
    """Raised when invalid value nb_drones
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid Value of number of drones.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(
            line, line_number, "nb_drones must be integer greather than Zero"
        )


class PrefixError(ParsingError):
    """Raised when lien start with different prefix
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid prefixes error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(
            line, line_number, "starts with different Prefix"
        )


# invalid key metadata
class KeyMetadataError(ParsingError):
    """Raised when Key metada is invalid
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid key in metadata.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "Invalid Key in metadata")


# invalid Value Metadata
class ValueMetadataError(ParsingError):
    """Raised when Value metadata is invalide
    """
    def __init__(self, line: str, line_number: int, error: str) -> None:
        """Initialize invalid value metadata error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "Invalid value " + error)


class ValueTypeZoneError(ParsingError):
    """Raised when value type zone is invalid
    """
    def __init__(self, line: str, line_number: int) -> None:
        """initialize value type zone error
        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, " Invalid value of type zone")


class ValueColorZoneError(ParsingError):
    """Raised when value color hub is invalid
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize Value color zone error.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, " Invalid Value color zone")


class ValueMaxDronesError(ParsingError):
    """Raised when Value Max drones is invalid
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid value max_drones.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, " Invalid value max drones")


class ValueMaxLinkCapacityError(ParsingError):
    """Raised when Value max link capacity is invalid
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid value max link capacity.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(
            line, line_number, "Invalid Value max_link_capacity"
        )


class KeyValMetadataError(ParsingError):
    """Raised when key and value of metadata not respect sysntax metadata
    """
    def __init__(self, line: str, line_number: int) -> None:
        """Initialize invalid syntax metadata.

        Args:
            line: The invalid line content.
            line_number: The line number where the error occurred.
        """
        super().__init__(line, line_number, "metadata must (key)=(value)")
