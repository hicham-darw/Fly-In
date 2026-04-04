from sys import exit
import re
from src.Exceptions.ParsingError import ParsingError
# from src.Parser.ParseModel import Zone, DataZone, Connection


class Parser:
    """
    Parser
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.nb_drones = 0
        self.start_hub = None
        self.end_hub = None
        self.connections = list()

    def parse_content_file(self) -> None:
        pass

    def read_content_file(self) -> None:
        try:
            with open(self.filename, "r") as file:
                get_drones = False
                for line in file:
                    print(f"[{line.strip()}]")
                    line = line.strip()
                    if line.strip().startswith('#') or len(line.strip()) == 0:
                        continue
                    elif get_drones is False:
                        match = re.match(r"nb_drones: (\d+)", line)
                        if not match:
                            raise ParsingError('line nb_drones Error:')
                        self.nb_drones = int(match.group(1))
                        if self.nb_drones <= 0:
                            raise ParsingError("nb_drones")
                        get_drones = True
                    elif line.startswith('start_hub:') and self.start_hub is None:
                        match = re.match(r"^start_hub: (.*) (\d+) (\d+) (\[.*\])", line)
                        if match is None:
                            raise ParsingError("start_hub doesn't support syntax")
                        metadata = self.parse_metadata_of_zone(match.group(4))
                        ...
                    elif line.startswith('end_hub:') and self.end_hub is None:
                        match = re.match(r"^end_hub: (.*) (\d+) (\d+) (\[.*\])", line)
                        if match is None:
                            raise ParsingError("end_hub: doesn't support syntax")
                        metadata = self.parse_metadata_of_zone(match.group(4))
                        ...
                    elif line.startswith('hub:'):
                        match = re.match(r"^hub: (.*) (\d+) (\d+) (\[.*\])", line)
                        if match is None:
                            raise ParsingError("hub: doesn't support syntax")
                        metadata = self.parse_metadata_of_zone(match.group(4))
                        ...
                    elif line.startswith('connection:'):
                        # match = re.match(r"connection: (.*?)-(.*?)\s*(\[[^\]]*\])?", line)
                        print("this is a match0: ", match.group(0))
                        print("this is a match1: ", match.group(1))
                        print("this is a match2: ", match.group(2))
                        print("this is a match3: ", match.group())
                        if match is None:
                            raise ParsingError("connection: doesn't support syntax")
                        print("@@@@@@@", match.group(3))
                        metadata = self.parse_metadata_of_connection(match.group(2))

                        ...
                    else:
                        raise ParsingError("ParsingError: line start with different")
        except ParsingError as e:
            print(e)
            exit(42)

    def parse_metadata_of_connection(self, data):
        print("ccccccc", data);
        data = data[1:-1]
        metadata = dict()

        for dat in data.split():
            d = dat.split('=')
            if len(d) != 2:
                raise ParsingError("connection metadata {key}={value}")
            if d[0] == 'max_link_capacity':
                number = int(d[1])
                metadata[d[0]] = number
            else:
                raise ParsingError('Connection metadata key must be max_link_capacity')
        return metadata
    
    def parse_metadata_of_zone(self, data):
        print("data1: ", data)
        data = data[1:-1]
        print("data2: ", data)
        metadata = dict()

        for dat in data.split():
            d = dat.split('=')
            print("ddddd:", d)
            if len(d) != 2:
                raise ParsingError("Zone metadata {key}={value}")
            if d[0] == 'zone':
                metadatap[d[0]] = d[1]
            elif d[0] == 'color':
                metadata[d[0]] = d[1]
            elif d[0] == 'max_drones':
                metadata[d[0]] = d[1]
            else:
                raise ParsingError("metadata of zones")
        return metadata

if __name__ == '__main__':
    parser = Parser('maps/easy/01_linear_path.txt')
    parser.read_content_file()