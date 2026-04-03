from sys import exit
from src.Exceptions.ParsingError import ParsingError
from .ParseModel import Zone, DataZone, Connection


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

                    if line.strip().startswith('#') or len(line.strip()) == 0:
                        continue
                    elif get_drones is False:
                        self.nb_drones = self.parse_number_of_drones(
                            line.strip()
                        )
                        if self.nb_drones <= 0:
                            raise ParsingError(
                                "Parsing Error: drones negative"
                            )
                        get_drones = True
                    elif line.strip().startswith('start_hub'):
                        self.create_hub(line.strip())
                    elif line.strip().startswith('end_hub'):
                        self.create_hub(line.strip())
                    elif line.strip().startswith('hub'):
                        self.create_hub(line.strip())
                    elif line.strip().startswith('connection'):
                        self.create_connection(line.strip())
                    else:
                        raise ParsingError("Parsing Error: another key!")
                    # should implement self.parse...
        except ParsingError as e:
            print(e)
            exit(42)

    def create_connection(self, line: str) -> None:
        splitted = line.split()
        dicdata = dict()
        # if len(splitted) == 3:
        #     
        # elif len(splitted) == 2:
        #     pass
        # else:
        #     raise ParsingError("Error splitted in connection")
        if len(splitted) == 3 and not splitted[2].startswith('[') and not splitted[2].startswith(']'):
            raise ParsingError(f"{splitted[2]} should be inside in bracket")
        elif len(splitted) == 2:
            dicdata = None
        else:
            raise ParsingError(f"{splitted[2]} should be inside in bracket")
        nodes = splitted[1].split('-')
        if len(nodes) != 2:
            raise ParsingError("connection: should include one dash")
        if dicdata:
            capacity_dic = splitted[2][1:-1].split('=')
            if len(capacity_dic) != 2 and capacity_dic[0] != 'max_link_capacity':
                raise ParsingError("connection: metadata max not included")
        else:
            capacity_dic = None
        if dicdata is None:
            self.connections.append(
                Connection(
                    zone_from=nodes[0],
                    zone_to=nodes[1],
                    max_capacity=int(capacity_dic[1])
                )
            )
        else:
            self.connections.append(
                Connection(
                    zone_from=nodes[0],
                    zone_to=nodes[1],
                )
            )

    def create_hub(self, line: str) -> None:
        splitted = line.split()
        dicdata = dict()
        if not splitted[4].startswith('[') and not splitted[4].endswith(']'):
            raise ParsingError("Parsing Error: metadata should in brakcet [...]")
        data = splitted[4][1:-1].split()
        for d in data:
            elem = d.split('=')
            if len(elem) != 2:
                raise ParsingError("Parsing Error: check zones")
            if elem[0] == 'color':
                dicdata[elem[0]] = elem[1]
            elif elem[0] == 'zone':
                dicdata[elem[0]] = elem[1]
            elif elem[0] == 'max_drones':
                dicdata[elem[0]] = int(elem[1])
            else:
                raise ParsingError("Parsing Error: check metadataZ")
        self.start_hub = Zone(
            type=splitted[0].rstrip(':'),
            name=splitted[1],
            x=splitted[2],
            y=splitted[3],
            metadata=DataZone(
                zone=dicdata.get('zone'),
                color=dicdata.get('color'),
                max_drones=dicdata.get('max_drones')
            )
        )

    def parse_number_of_drones(self, line: str) -> int:
        splitted = line.split(':')

        if len(splitted) != 2 or splitted[0].strip() != "nb_drones":
            raise ParsingError("Parsing Error: nb_drons syntax")
        try:
            drones = int(splitted[1].strip())
        except ValueError:
            raise ParsingError("Parsing Error: value nb_drons should be int")
        else:
            if drones <= 0:
                raise ParsingError("Parsing Error: drones cannot be negative!")
            return drones


if __name__ == '__main__':
    parser = Parser("maps/easy/01_linear_path.txt")
    parser.read_content_file()
