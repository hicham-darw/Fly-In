from sys import exit
import re
from src.Exceptions.ParsingError import ParsingError
from src.Zone.Zone import Hub, Connection
from src.Enums.Enums import TypeZone

class Parser:
    """Parse a map file into drones, hubs, and connections.

    The parser reads the input file line by line, validates syntax, and stores
    parsed data for later graph construction and simulation.
    """
    
    def __init__(self, filename: str) -> None:
        """Initialize the parser.

        Args:
            filename: Path to the input map file to parse.
        """
        self.filename = filename
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = list()
        self.connections = list()
        self.first_line = 1
        self.name_zones = list()

    def parse_number_of_drones(self, line: str) -> None:
        """Parse the number of drones from a line.

        Args:
            line: Input line containing the drone count.

        Raises:
            ParsingError: If the line does not match the expected syntax or if
                the value is not strictly positive.
        """
        match = re.match(r"nb_drones: (\d+)", line)
        if not match:
            raise ParsingError('line nb_drones doesn\'t support syntax.')
        self.nb_drones = int(match.group(1))
        if self.nb_drones <= 0:
            raise ParsingError("nb_drones")
    
    def parse_start_hub(self, line: str) -> None:
        """Parse the start hub definition.

        Args:
            line: Input line defining the start hub.

        Raises:
            ParsingError: If the syntax is invalid or the hub name is not
                unique.
        """
        match = re.match(r"^start_hub: [^ \-]+ \d+ \d+( \[.+\])?$", line)
        if match is None:
            raise ParsingError("start_hub doesn't support syntax")
        start_bracket = line.find('[')
        if start_bracket < 0:
            metadata = None
        else:
            metadata = self.parse_metadata_of_hub(line[start_bracket:])
            line = line[:start_bracket].strip()
        splitted = line.split()
        if len(splitted) != 4:
            raise ParsingError("metadata contains invalid data")

        if splitted[1] not in self.name_zones:
            self.name_zones.append(splitted[1])
        else:
            raise ParsingError("name must be a unique name")

        x = int(splitted[2])
        y = int(splitted[3])

        self.start_hub = Hub(
            splitted[0][:-1],
            splitted[1],
            splitted[2],
            splitted[3],
            metadata
        )
    
    def parse_end_hub(self, line: str) -> None:
        """Parse the end hub definition.

        Args:
            line: Input line defining the end hub.

        Raises:
            ParsingError: If the syntax is invalid or the hub name is not
                unique.
        """
        match = re.match(r"^end_hub: [^ \-]+ \d+ \d+( \[.+\])?", line)
        if match is None:
            raise ParsingError("end_hub doesn't support syntax")

        start_bracket = line.find('[')
        if start_bracket < 0:
            metadata = None
        else:
            metadata = self.parse_metadata_of_hub(line[start_bracket:])
            line = line[:start_bracket].strip()
        splitted = line.split()
        if len(splitted) != 4:
            raise ParsingError("metadata contains invalid data")

        if splitted[1] not in self.name_zones:
            self.name_zones.append(splitted[1])
        else:
            raise ParsingError("name must be a unique name")

        x = int(splitted[2])
        y = int(splitted[3])

        self.end_hub = Hub(
            splitted[0][:-1],
            splitted[1],
            splitted[2],
            splitted[3],
            metadata
        )

    def parse_regular_hub(self, line: str) -> None:
        """Parse a regular hub definition.

        Args:
            line: Input line defining a regular hub.

        Raises:
            ParsingError: If the syntax is invalid or the hub name is not
                unique.
        """
        match = re.match(r"^hub: [^ \-]+ \d+ \d+( \[.+\])?", line)
        if match is None:
            raise ParsingError("hub doesn't support syntax")
        start_bracket = line.find('[')
        if start_bracket < 0:
            metadata = None
        else:
            metadata = self.parse_metadata_of_hub(line[start_bracket:])
            line = line[:start_bracket].strip()
        splitted = line.split()
        if len(splitted) != 4:
            raise ParsingError("metadata contains invalid data")

        x = int(splitted[2])
        y = int(splitted[3])

        if splitted[1] not in self.name_zones:
            self.name_zones.append(splitted[1])
        else:
            raise ParsingError("name must be a unique name")

        self.hubs.append(
            Hub(
                splitted[0][:-1],
                splitted[1],
                x,
                y,
                metadata
            )
        )

    def parse_metadata_of_hub(self, data) -> dict[str, int | str | TypeZone]:
        """Parse hub metadata from a bracketed block.

        Args:
            data: Raw metadata string including the surrounding brackets.

        Returns:
            A dictionary containing parsed metadata values.

        Raises:
            ParsingError: If metadata syntax or values are invalid.
        """
        data = data[1:-1]
        metadata = {
            'zone': TypeZone.normal,
            'color': None,
            'max_drones': 1
        }
        if len(data.split()) > 3:
            raise ParsingError("metadata must be contains 3 pairs.")
        for pairs in data.split():
            d = pairs.split('=')
            if len(d) != 2:
                raise ParsingError("Hub metadata {key}={value}")
            if d[0].lower() not in ['zone', 'color', 'max_drones']:
                raise ParsingError("Hub metadata invalid key.")
            
            if d[0].lower() == 'zone' and d[1] in [e.name for e in TypeZone]:
                metadata['zone'] = TypeZone[d[1]]
            elif d[0].lower() == 'color' and d[1].isalpha():
                metadata['color'] = d[1]
            elif d[0].lower() == 'max_drones':
                metadata['max_drones'] = int(d[1])
            else:
                raise ParsingError("metadata of zones [zone, color, max_drones]")
            if metadata['max_drones'] <= 0:
                metadata[max_drones] = 1
        return metadata

    def parse_connection(self, line) -> None:
        """Parse a connection definition.

        Args:
            line: Input line defining a connection between two hubs.

        Raises:
            ParsingError: If the syntax is invalid, if a referenced hub does
                not exist, or if the connection is malformed.
        """
        match = re.match(r"^connection: [^ \-]+-[^ \-]+( \[.+\])?", line)
        if match is None:
            raise ParsingError("end_hub doesn't support syntax")
        splitted = line.split()

        if len(splitted) == 3:
            metadata = self.parse_metadata_of_connection(splitted[2])
        elif len(splitted) == 2:
            metadata = None
        else:
            raise ParsingError("metadata contains invalid data")

        names_hub = splitted[1].split('-')
        if len(names_hub) != 2:
            raise ParsingError("must be two hubs name in connection")

        if names_hub[0] != self.start_hub.name and names_hub[0] != self.end_hub.name and names_hub[0] not in [hub.name for hub in self.hubs]:
            raise ParsingError(f"{names_hub[0]} must be name from hubs")
        elif names_hub[1] != self.start_hub.name and names_hub[1] != self.end_hub.name and names_hub[1] not in [hub.name for hub in self.hubs]:
            raise ParsingError(f"{names_hub[1]} must be name from hubs")
    
        self.connections.append(
            Connection(
                names_hub[0],
                names_hub[1],
                metadata
            )
        )

    def parse_metadata_of_connection(self, data: str) -> dict[str, int]:
        """Parse connection metadata from a bracketed block.

        Args:
            data: Raw metadata string including the surrounding brackets.

        Returns:
            A dictionary containing parsed metadata values.

        Raises:
            ParsingError: If metadata syntax or values are invalid.
        """
        metadata = {
            'max_link_capacity': 1
        }
        data = data[1:-1]
        if len(data.split()) != 1:
            raise ParsingError("metadata connection must contain 1 argument")
        pairs = data.split('=')
        if len(pairs) != 2:
            raise ParsingError('metadata connection must contain {key}={value}')
        
        if pairs[0] != 'max_link_capacity':
            raise ParsingError("metadata connection key must be {max_link_capacity}")
        elif int(pairs[1]) < 0:
            raise ParsingError("max_link_capacity must be greather than zero.")
        metadata['max_link_capacity'] =  int(pairs[1])
        return metadata

    def parse_content_file(self) -> None:
        """Read and parse the configured input file.

        The method strips comments, dispatches each non-empty line to the
        appropriate parser, and stops the program with exit code 42 on any
        parsing error.

        Raises:
            ParsingError: Internally raised for malformed input before being
                caught and reported.
        """
        try:
            with open(self.filename, "r") as file:
                first_lin = 1
                for line in file:
                    if line.find('#') != -1:
                        line = line[:line.find('#')].strip()
                    else:
                        line = line.strip()
                    if not len(line):
                        continue

                    if line.startswith("nb_drones:") and not self.nb_drones and self.first_line:
                        self.parse_number_of_drones(line)
                        self.first_line = 0
                    elif line.startswith('start_hub:') and self.start_hub is None and not self.first_line:
                        self.parse_start_hub(line)
                    elif line.startswith('end_hub:') and self.end_hub is None and not self.first_line:
                        self.parse_end_hub(line)
                    elif line.startswith('hub:') and not self.first_line:
                        self.parse_regular_hub(line)
                    elif line.startswith('connection:') and not self.first_line:
                        self.parse_connection(line)
                    else:
                        raise ParsingError("ParsingError: line starts with different value!")
            if self.start_hub is None or self.end_hub is None or not len(self.hubs)\
            or not len(self.connections) or self.first_line:
                raise ParsingError("please check config file!")

        except (ParsingError, Exception) as e:
            print(e)
            exit(42)
    

if __name__ == '__main__':
    parser = Parser('maps/easy/01_linear_path.txt')
    parser.parse_content_file()