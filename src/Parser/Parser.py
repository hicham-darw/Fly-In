from sys import exit
from src.Exceptions.readFileError import ReadFileError
from src.Exceptions.ParsingError import ParsingError


class Parser:
    """
    Parser
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def parse_content_file(self) -> None:
        pass

    def read_content_file(self) -> None:
        try:
            with open(self.filename, "r") as file:
                i = 0
                for line in file:
                    if line.strip().startswith('#'):
                        continue
                    elif i == 0:
                        self.nb_drones = self.parse_number_of_drones(
                            line.strip()[:-1])
                        if self.nb_drones < 0:
                            raise ParsingError(
                                "Parsing Error: drones negative"
                            )
                    elif line.strip().startswith('start_hub'):
                        self.parse_start_hub(line.strip()[:-1])
                    elif line.strip().startswith('end_hub'):
                        self.parse_end_hub(line.strip()[:-1])
                    elif line.strip().startswith('hub'):
                        self.parse.hub(line.strip()[:-1])
                    elif line.strip().startswith('connection'):
                        self.parse_connection(line.strip()[:-1])
                    else:
                        raise ParsingError("Parsing Error: another key!")
                    # should implement selfs.parse...
        except ReadFileError as e:
            print(e)
            exit(42)

    def parse_number_of_drones(self, line: str) -> int:
        try:
            splitted = line.split(':')
            if len(splitted) != 2 or splitted[0].strip() != "nb_drones":
                return -1
            drones = int(splitted[1])
            if drones <= 0:
                raise("Parsing Error: drones cannot be negative!")
            return drones
        except ParsingError as e:
            return -1

if __name__ == '__main__':
    parser = Parser("main.py")
    parser.read_content_file()
