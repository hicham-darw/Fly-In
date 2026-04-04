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
                    elif line.startswith('start_hub'):
                        match = re.match(r"^start_hub: (.*) (\d+) (\d+) (\[.*\])", line)
                        metadata = self.parse_metadata_of_zone(match.group(4))
                        print(metadata)
            #/// continue here .....!
                    # elif line.strip().startswith('end_hub'):
                    #     self.create_hub(line.strip())
                    # elif line.strip().startswith('hub'):
                    #     self.create_hub(line.strip())
                    # elif line.strip().startswith('connection'):
                    #     self.create_connection(line.strip())
                    else:
                        raise ParsingError("Parsing Error: another key!")
                    # should implement self.parse...
        except ParsingError as e:
            print(e)
            exit(42)

    def parse_metadata_of_zone(self, data):
        data = data[1:-1]
        metadata = dict()
        print("sssss", data)
        for dat in data.split():
            d = dat.split('=')
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