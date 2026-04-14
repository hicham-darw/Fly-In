from sys import exit
import re
from src.Exceptions.ParsingError import ParsingError
from src.Zone.Zone import Hub, Connection
from .ParseModel import TypeZone

class Parser:
    """
    Parser
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.hubs = list()
        self.connections = list()

    def parse_content_file(self) -> None:
        pass

    def parse_number_of_drones(self, line: str) -> None:
        match = re.match(r"nb_drones: (\d+)", line)
        if not match:
            raise ParsingError('line nb_drones doesn\'t support syntax.')
        self.nb_drones = int(match.group(1))
        if self.nb_drones <= 0:
            raise ParsingError("nb_drones")
    
    def parse_start_hub(self, line: str) -> None:
        match = re.match(r"^start_hub: [a-zA-Z0-9]+ \d+ \d+( \[.+\])?", line)
        if match is None:
            raise ParsingError("start_hub doesn't support syntax")
        splitted = line.split()
        if len(splitted) == 5:
            metadata = self.parse_metadata_of_hub(splitted[4])
        elif len(splitted) == 4:
            metadata = None
        else:
            raise ParsingError("metadata contains invalid data")
        self.start_hub = Hub(
            splitted[0][:-1],
            splitted[1],
            splitted[2],
            splitted[3],
            metadata
        )
    
    def parse_end_hub(self, line: str) -> None:
        match = re.match(r"^end_hub: [a-zA-Z0-9]+ \d+ \d+( \[.+\])?", line)
        if match is None:
            raise ParsingError("end_hub doesn't support syntax")
        splitted = line.split()
        if len(splitted) == 5:
            metadata = self.parse_metadata_of_hub(splitted[4])
        elif len(splitted) == 4:
            metadata = None
        else:
            raise ParsingError("metadata contains invalid data")
        self.end_hub = Hub(
            splitted[0][:-1],
            splitted[1],
            splitted[2],
            splitted[3],
            metadata
        )

    def parse_regular_hub(self, line: str) -> None:
        match = re.match(r"^hub: [a-zA-Z0-9]+ \d+ \d+( \[.+\])?", line)
        if match is None:
            raise ParsingError("end_hub doesn't support syntax")
        splitted = line.split()
        if len(splitted) == 5:
            metadata = self.parse_metadata_of_hub(splitted[4])
        elif len(splitted) == 4:
            metadata = None
        else:
            raise ParsingError("metadata contains invalid data")
        self.hubs.append(
            Hub(
                splitted[0][:-1],
                splitted[1],
                splitted[2],
                splitted[3],
                metadata
            )
        )

    def parse_metadata_of_hub(self, data) -> dict[str, int]:
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

            if d[0].lower() == 'zone' and d[1] in [e.value for e in TypeZone]:
                metadata['zone'] = d[1]
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
        match = re.match(r"^connection: [a-zA-Z0-9]+-[a-zA-Z0-9]( \[.+\])?", line)
        if match is None:
            raise ParsingError("end_hub doesn't support syntax")
        splitted = line.split()
        print(splitted)
        if len(splitted) == 3:
            metadata = self.parse_metadata_of_connection(splitted[2])
        elif len(splitted) == 2:
            metadata = None
        else:
            raise ParsingError("metadata contains invalid data")
        names_hub = splitted[1].split('-')
        if len(names_hub) != 2:
            raise ParsingError("must be two hubs name in connection")
        #  if names not in start_hub or end_hub or hubs return raise error

        self.connections.append(
            Connection(
                names_hub[0],
                names_hub[1],
                metadata
            )
        )

    def parse_metadata_of_connection(self, data: str) -> dict[str, int]:
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
        metadata['max_link_capacity'] =  int(pairs[1])
        return metadata

    def read_content_file(self) -> None:
        try:
            with open(self.filename, "r") as file:
                for line in file:
                    line = line[:line.find('#')].strip()
                    if not len(line):
                        continue
                    
                    if line.startswith("nb_drones:") and not self.nb_drones:
                        self.parse_number_of_drones(line)
                    elif line.startswith('start_hub:') and self.start_hub is None:
                        self.parse_start_hub(line)
                    elif line.startswith('end_hub:') and self.end_hub is None:
                        self.parse_end_hub(line)
                    elif line.startswith('hub:'):
                        self.parse_regular_hub(line)
                    elif line.startswith('connection:'):
                        self.parse_connection(line)
                    else:
                        raise ParsingError("ParsingError: line starts with different value!")
        except (ParsingError, Exception) as e:
            print(e)
            exit(42)
    

if __name__ == '__main__':
    parser = Parser('maps/easy/01_linear_path.txt')
    parser.read_content_file()