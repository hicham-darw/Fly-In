import re
from typing import TypedDict
from src.DataClasses.DataClasses import ParsedData, HubMetadata, ConnectionMetadata
from src.Exceptions.ParsingError import ParsingError
from src.DataClasses.DataClasses import Hub, Connection
from src.Enums.Enums import TypeZone, MetaDataOfHub, MetaDataOfConnection


class Parser:
    """Parse a map file into drones, hubs, and connections.

    The parser reads the input file line by line, validates syntax, and stores
    parsed data for later graph construction and simulation.
    """

    def __init__(self, filename: str) -> None:
        """the Constructor parser.

        Args:
            filename: Path to the input map file to parse.
        Returns:
            None
        """
        self.hubs: list[Hub] = list()
        self.connections: list[Connection] = list()
        
        self.filename = filename
        self.nb_drones = 0
        self.first_line = 1
        self.name_zones: list[str] = list()
        self.count_start_hub = 0
        self.count_end_hub = 0

    def parse(self) -> ParsedData | None:
        """ parse content file and return dictionary of data
                if throwing an exception in parsing catch it internaly an return None
                otherwise return parsed_data

        Args:
            None
        Returns:
            Dictionary: parsed data (nb_drones - hubs - connection)
        """
        try:
            self.parse_content_file()
            return self.get_parsed_data()
        except ParsingError as e:
            print(e)
        except FileNotFoundError:
            print("Error: file not found!.")
        except PermissionError:
            print("Error: file not permitted!.")
        except IsADirectoryError:
            print(f"Error: {self.filename} is a directory!.")
        return None

    # getters
    def get_default_metadata_of_hub(self) -> HubMetadata:
        """this method return default metadata of hub

        Args:
            None
        Returns:
            dictionary default metadata of hub
        """
        return {
            MetaDataOfHub.zone.name: TypeZone.normal,
            MetaDataOfHub.color.name: None,
            MetaDataOfHub.max_drones.name: 1
        }

    def get_default_metadata_of_connection(self) -> ConnectionMetadata:
        """method return default metadata of connection

        Args:
            None
        Returns:
            None
        """
        return {
            MetaDataOfConnection.max_link_capacity.name: 1
        }

    def parse_number_of_drones(self, line: str) -> None:
        """Parse the number of drones from a line.

        Args:
            line: Input line containing the drone count.
        Raises:
            ParsingError: If the line does not match the expected syntax or if
                the value is not strictly positive.
        Returns: None
        """
        match = re.match(r"nb_drones: +?(\d+)$", line)
        if not match:
            raise ParsingError('nb_drones must integer and greather than Zero.')
        self.nb_drones = int(match.group(1))

    def parse_hub(self, line: str) -> None:
        """parse hub is matches syntax

        Args:
            line: (str): stripped line 
        """
        match = re.match(r"^(start_hub|end_hub|hub): [^ \-]+ -?\d+ -?\d+( \[.+\])?$", line)
        if match is None:
            err_line = line[:line.find(':')] if line.find(":") != -1 else line
            raise ParsingError(f"({err_line}) Doesn't match syntax of hubs.")
        
        start_bracket = line.find('[')
        if start_bracket != -1:
            metadata: HubMetadata = self.parse_metadata_of_hub(line[start_bracket:])
            line_without_bracket = line[:start_bracket].rstrip()
        else:
            metadata = self.get_default_metadata_of_hub()
            line_without_bracket = line.rstrip()
        
        data_of_hub = line_without_bracket.split()
        self.create_new_hub(
            type_zone=data_of_hub[0][:-1],
            name=data_of_hub[1],
            x=int(data_of_hub[2]),
            y=int(data_of_hub[3]),
            metadata=metadata
        )

    def parse_metadata_of_hub(self, data: str) -> HubMetadata:
        """Parse hub metadata from a bracketed block.

        Args:
            data: Raw metadata string including the surrounding brackets.
        Raises:
            ParsingError: If metadata syntax or values are invalid.
        Returns:
            A dictionary containing parsed metadata values.
        """
        metadata: HubMetadata = self.get_default_metadata_of_hub()
        data = data[1:-1]
        if len(data.split()) > 3:
            raise ParsingError("metadata contains 3 pairs at most.")
        
        for pairs in data.split():
            key_val_data = pairs.split('=')
            metadata = self.parse_each_pair_in_metadata_of_hub(key_val_data, metadata)

        return metadata

    def parse_each_pair_in_metadata_of_hub(
        self, key_val_data: list[str], metadata: HubMetadata
    ) -> HubMetadata:
        """method parse each pair in metadata otherwise raise an exception (parsing)

        Args:
            key_val_data: list[str]: list contain key and value only
            metadata: dict: contains default values of metadata
        Raises:
            ParsingError: If the data is invalid
        Returns:
            updated metadata if valid metadata
        """        
        if len(key_val_data) != 2:
            raise ParsingError("Hub metadata must {key}={value}")
        
        if key_val_data[0].lower() not in [elem.name for elem in MetaDataOfHub]:
            raise ParsingError("Hub metadata invalid key.")
        
        if key_val_data[0].lower() == MetaDataOfHub.zone.name and key_val_data[1] in [e.name for e in TypeZone]:
            metadata[MetaDataOfHub.zone.name] = TypeZone[key_val_data[1]]
        elif key_val_data[0].lower() == MetaDataOfHub.color.name:
            if key_val_data[1].isalpha():
                metadata[MetaDataOfHub.color.name] = key_val_data[1].lower()
            else:
                raise ParsingError("color must be alphabetical string.")
        elif key_val_data[0].lower() == MetaDataOfHub.max_drones.name:
            try:
                metadata[MetaDataOfHub.max_drones.name] = int(key_val_data[1])
            except ValueError:
                raise ParsingError("max_drones must be integer.")
        else:
            raise ParsingError("invalid metadata. please check hubs in file")
        
        max_drones = metadata[MetaDataOfHub.max_drones.name]
        if not isinstance(max_drones, int):
            raise ParsingError('max_drones must be integer.')
        if max_drones < 0:
            raise ParsingError("max_drones must be greater than zero.")
        return metadata

    def parse_connection(self, line: str) -> None:
        """Parse a connection definition.

        Args:
            line: Input line defining a connection between two hubs.
        Raises:
            ParsingError: If the syntax is invalid, if a referenced hub does
                not exist, or if the connection is malformed.
        Returns:
            None
        """
        match = re.match(r"^connection: [^ \-]+-[^ \-]+( \[.+\])?", line)
        if match is None:
            raise ParsingError("end_hub doesn't support syntax")
        
        metadata = self.get_default_metadata_of_connection()
        start_bracket = line.find('[')
        if start_bracket > -1:
            metadata = self.parse_metadata_of_connection(line[start_bracket:])
            line = line[:start_bracket]
        splitted = line.split()

        names_hub = self.is_valid_names_in_connection(splitted[1])
        self.connections.append(
            Connection(
                names_hub[0],
                names_hub[1],
                metadata                
            )
        )

    def parse_metadata_of_connection(self, data: str) -> ConnectionMetadata:
        """Parse connection metadata from a bracketed block.

        Args:
            data: Raw metadata string including the surrounding brackets.
        Returns:
            A dictionary containing parsed metadata values.
        Raises:
            ParsingError: If metadata syntax or values are invalid.
        """
        metadata = self.get_default_metadata_of_connection()
        data = data[1:-1]
        if len(data.split()) != 1:
            raise ParsingError("metadata connection must contain 1 argument")
        pairs = data.split('=')
        if len(pairs) != 2:
            raise ParsingError('metadata connection must contain {key}={value}')
        if pairs[0] != MetaDataOfConnection.max_link_capacity.name:
            raise ParsingError("metadata connection key must be {max_link_capacity}")
        elif int(pairs[1]) < 0:
            raise ParsingError("max_link_capacity must be greather than zero.")
        metadata[MetaDataOfConnection.max_link_capacity.name] =  int(pairs[1])
        return metadata

    def create_new_hub(
        self,
        type_zone: str,
        name: str,
        x: int, y: int,
        metadata: HubMetadata
    ) -> None:
        """create new Zone it based on type_zone
        Args:
            type_zone: type of hub start - end or regular hub
            name: name of hub
            x:  x coordinate in map
            y: y cooordinate in map
            metadata: metadata of hub like color zone type and max_drones
        Returns:
            None
        """
        new_hub = Hub(
            type_zone=type_zone,
            name=name,
            x=x,
            y=y,
            metadata=metadata,
        )
        if type_zone == "start_hub":
            self.start_hub = new_hub
        elif type_zone == 'end_hub':
            self.end_hub = new_hub
        else:
            self.hubs.append(new_hub)
        self.add_name_to_name_zones(new_hub.name)

    def is_valid_names_in_connection(self, names_hub: str) -> list[str]:
        """validate names in connection if exist name in hubs
            otherwise raise Parsing Error

        Args:
            names_hub: str : contain two names separated by dash -
        Raises:
            ParsingError if not a valid data
        Returns:
            return list[str] : list has two names froms hubs
        """
        names = names_hub.split('-')
        if len(names) != 2:
            raise ParsingError("must be two hubs name in 1 connection")

        if names[0] not in [self.start_hub.name] + [self.end_hub.name] + [hub.name for hub in self.hubs]:
            raise ParsingError(f"{names[0]} must be a name from hubs")
        elif names[1] not in [self.start_hub.name] + [self.end_hub.name] + [hub.name for hub in self.hubs]:
            raise ParsingError(f"{names[1]} must be a name from hubs")
        return names

    def add_name_to_name_zones(self, new_name: str) -> None:
        """add name to name_zones for each hib has a unique name

        Args:
            new_name: new_name of hub
        Raises:
            ParsingError: if name already exists
        Returns:
            None
        """
        if new_name not in self.name_zones:
            self.name_zones.append(new_name)
            return
        raise ParsingError("name must be a unique name.")

    def filter_line(self, line: str) -> str:
        """ filter line method only search if line contains hashtag
            to slice comments and strip it

        Args:
            line: str : raw line from file
        Returns:
            line: filter line and return it
        """
        if line.find('#') != -1:
            line = line[:line.find('#')].strip()
        else:
            line = line.strip()
        return line

    def is_completed_data(self) -> None:
        """if required data not initialized before or not change flag readline

        Args:
            None
        Raises:
            ParsingError: start_hub or end_hub not initialized or not read first_line
        Return:
            None
        """
        if self.start_hub is None:
            raise ParsingError("start_hub not Found!, please check your file.")
        elif self.end_hub is None:
            raise ParsingError("end_hub not Found!, please check your file.")
        elif not len(self.connections):
            raise ParsingError("connections not Found!, 1 connection at least.")
        elif self.first_line:
            raise ParsingError("file is empty or has only comments or spaces")

    def parse_content_file(self) -> None:
        """Read and parse the configured input file.

        Args:
            None
        Raises:
            ParsingError: Internally raised for malformed input before being
                caught and reported.
        Returns:
            None
        """
        with open(self.filename, "r") as file:
            for line in file:
                line = self.filter_line(line)
                if not len(line):
                    continue
                if line.startswith("nb_drones:") and not self.nb_drones and self.first_line:
                    self.parse_number_of_drones(line)
                    self.first_line = 0
                elif (line.startswith('start_hub') or line.startswith('end_hub') or line.startswith('hub')) and not self.first_line:
                    self.parse_hub(line)
                elif line.startswith('connection:') and not self.first_line:
                    self.parse_connection(line)
                else:
                    raise ParsingError("ParsingError: line starts with different value!")
        self.is_completed_data()
   
    def get_parsed_data(self) -> ParsedData:
        """get all data need for graph like:
            start_hub - end_hub - hubs and connections

        Args:
            None
        Returns:
            dictionary: valid data of start_hub - end_hub - hubs - connections
        """
        return {
            'nb_drones': self.nb_drones,
            'start_hub': self.start_hub,
            'end_hub': self.end_hub,
            'hubs': self.hubs,
            'connections': self.connections
        }