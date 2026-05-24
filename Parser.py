import re
from DataClasses import ParsedData, HubMetadata
from DataClasses import ConnectionMetadata
from ParsingError import ParsingError, SyntaxHubError, SyntaxConnectionError, \
    SyntaxDronesError, InvalidFirstLineError, DuplicateNbDronesError, \
    DuplicateConnectionError, DuplicateNameHub, \
    NotFoundError, NotFoundNameHubError, ValueNbDronesError, PrefixError, \
    KeyMetadataError, ValueTypeZoneError, ValueColorZoneError, \
    ValueMaxDronesError, ValueMaxLinkCapacityError, KeyValMetadataError
from DataClasses import Hub, Connection
from Enums import TypeZone, MetaDataOfHub, MetaDataOfConnection
from FactoryMetadata import FactoryMetadata
from sys import stderr


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
        self.red = '\033[1;31m'
        self.hubs: list[Hub] = list()
        self.connections: list[Connection] = list()

        self.filename: str = filename
        self.nb_drones: int = 0
        self.first_line: int = 1
        self.current_line: str = ''
        self.line_number: int = 0
        self.name_zones: list[str] = list()
        self.count_start_hub: int = 0
        self.count_end_hub: int = 0

    def parse(self) -> ParsedData:
        """ parse content file and return dictionary of data
                if throwing an exception in parsing catch it internaly
                otherwise return parsed_data

        Args:
            None
        Returns:
            Dictionary: parsed data (nb_drones - hubs - connection) or None
        """
        try:
            self.__parse_content_file()
            return self.get_parsed_data()
        except ParsingError as e:
            print(e, file=stderr)
        except NotFoundError as e:
            print(e, file=stderr)
        except FileNotFoundError:
            print(
                f"{self.red}Error: {self.filename} not found!.", file=stderr
            )
        except PermissionError:
            print(
                f"{self.red}Error: {self.filename} not permitted!", file=stderr
            )
        except IsADirectoryError:
            print(
                f"{self.red}Error:",
                f"{self.filename} is a directory!", file=stderr
            )
        except UnicodeDecodeError:
            print(f"{self.red}Error: can't decode content file", file=stderr)
        except ValueError as e:
            print(
                f"{self.red}line {self.line_number}: \"{self.current_line}\"",
                f"{e}"
            )
        except Exception as e:
            print(f"{self.red}Unexpected Error: you are a Great tester!")
            print(e)
        exit(42)

    def __parse_number_of_drones(self) -> None:
        """Parse the number of drones from a line.

        Args:
            None
        Raises:
            ValueNbDronesError: If the line does not match the expected syntax
                or if the value is not strictly positive.
        Returns:
            None
        """
        self.__is_valid_line('nb_drones')
        if self.nb_drones <= 0:
            raise ValueNbDronesError(self.current_line, self.line_number)

    def __parse_hub(self) -> None:
        """parse hub if matches syntax and store it

        Args:
            None
        Returns:
            None
        """
        self.__is_valid_line("hub")
        start_bracket = self.current_line.find('[')
        if start_bracket != -1:
            metadata: HubMetadata = self.__parse_metadata_of_hub(
                self.current_line[start_bracket:]
            )
            line_without_bracket = self.current_line[:start_bracket].rstrip()
        else:
            metadata = FactoryMetadata.get_metadata_of_hub()
            line_without_bracket = self.current_line.rstrip()

        data_of_hub = line_without_bracket.split()

        self.create_new_hub(
            type_zone=data_of_hub[0][:-1],
            name=data_of_hub[1],
            x=int(data_of_hub[2]),
            y=int(data_of_hub[3]),
            metadata=metadata
        )

    def __is_valid_line_nb_drones(self) -> None:
        """valid line with format nb_drones and not first line

        Args:
            None
        Raises:
            DuplicateNbDronesError: is duplicated nb_drones
            SyntaxDronesError:  if not a match format nb_drones
            ValueNbDronesError: if not valid number of drones
        Returns:
            None
        """
        if not self.first_line:
            raise DuplicateNbDronesError(self.current_line, self.line_number)
        match = re.match(r"nb_drones: ([-+]?\d+)$", self.current_line)
        if not match:
            raise SyntaxDronesError(self.current_line, self.line_number)
        try:
            self.nb_drones = int(match.group(1))
        except ValueError:
            raise ValueNbDronesError(self.current_line, self.line_number)

    def __is_valid_line_hub(self) -> None:
        """validate line with format hub and not first line

        Args:
            None
        Raises:
            InvalidFirstLineError: if is first line raised error
            SyntaxHubError: if not a match format connection
        Returns:
            None
        """
        if self.first_line:
            raise InvalidFirstLineError(self.current_line, self.line_number)
        if self.current_line.find('[') != -1 and self.current_line.find(']') != -1:
            match = re.match(
                r"^(start_hub|end_hub|hub): [^ \-]+ [-+]?\d+ [-+]?\d+ \[.*\]$",
                self.current_line
            )
        else:
            match = re.match(
                r"^(start_hub|end_hub|hub): [^ \-]+ [-+]?\d+ [-+]?\d+$",
                self.current_line
            )
        if match is None:
            raise SyntaxHubError(self.current_line, self.line_number)

    def __is_valid_line_connection(self) -> None:
        """validate line with format connection and not first line

        Args:
            None
        Raises:
            InvalidFirstLineError: if is first line raised error
            SyntaxConnectionError:  if not a match format connection
        Returns:
            None
        """
        if self.first_line:
            raise InvalidFirstLineError(self.current_line, self.line_number)

        if self.current_line.find('[') != -1 and self.current_line.find(']') != -1:
            match = re.match(
                r"^connection: [^ \-]+-[^ \-]+ \[.*\]$", self.current_line
            )
        else:
            match = re.match(
                r"^connection: [^ \-]+-[^ \-]+$", self.current_line
            )
            
        if match is None:
            raise SyntaxConnectionError(
                self.current_line, self.line_number
            )
        return

    def __is_valid_line(self, prefix_line: str) -> None:
        """ validate line with not first line and and syntax is valid

        Args:
            prefix_line: (str) validate line with prefix line
        Returns:
            None
        """
        if prefix_line == 'nb_drones':
            return self.__is_valid_line_nb_drones()
        elif prefix_line == 'hub':
            return self.__is_valid_line_hub()
        else:
            return self.__is_valid_line_connection()

    def __parse_metadata_of_hub(self, data: str) -> HubMetadata:
        """Parse hub metadata from a bracketed block.

        Args:
            data: Raw metadata string including the surrounding brackets.
        Raises:
            ParsingError: If metadata syntax or values are invalid.
        Returns:
            A dictionary containing parsed metadata values.
        """
        metadata: HubMetadata = FactoryMetadata.get_metadata_of_hub()
        data = data[1:-1]
        if not data:
            return metadata

        for pairs in data.split():
            key_val_data = pairs.split('=')
            metadata = self.__parse_each_pair_in_metadata_of_hub(
                key_val_data, metadata
            )
        return metadata

    def __parse_each_pair_in_metadata_of_hub(
        self, key_val_data: list[str], metadata: HubMetadata
    ) -> HubMetadata:
        """method parse each pair in metadata otherwise raise an exception

        Args:
            key_val_data: list[str]: list contain key and value
            metadata: dict: contains default values of metadata
        Raises:
            KeyValMetadataError: when found metadata not (key=value)
            KeyMetadataError: raised when unexpected key
            ValueTypeZoneError: when Value of Type Zone not valid
            ValueColorZoneError: when Value Color not a valid
            ValueMaxDronesError: when Value max_drones not valid integer

        Returns:
            updated metadata if valid metadata
        """
        if len(key_val_data) != 2 or not len(key_val_data[1]):
            raise KeyValMetadataError(self.current_line, self.line_number)

        if key_val_data[0].lower() == MetaDataOfHub.zone.name:
            if key_val_data[1] in [e.name for e in TypeZone]:
                metadata[MetaDataOfHub.zone.name] = TypeZone[key_val_data[1]]
            else:
                raise ValueTypeZoneError(self.current_line, self.line_number)
        elif key_val_data[0].lower() == MetaDataOfHub.color.name:
            if key_val_data[1].isalpha():
                metadata[MetaDataOfHub.color.name] = key_val_data[1].lower()
            else:
                raise ValueColorZoneError(self.current_line, self.line_number)
        elif key_val_data[0].lower() == MetaDataOfHub.max_drones.name:
            try:
                metadata[MetaDataOfHub.max_drones.name] = int(key_val_data[1])
            except ValueError:
                raise ValueMaxDronesError(self.current_line, self.line_number)
        else:
            raise KeyMetadataError(self.current_line, self.line_number)
        return metadata

    def __parse_connection(self) -> None:
        """Parse a connection definition.

        Args:
            None
        Returns:
            None
        """
        self.__is_valid_line("connection")
        metadata: ConnectionMetadata =\
            FactoryMetadata.get_metadata_of_connection()
        start_bracket = self.current_line.find('[')
        if start_bracket > -1:
            metadata = self.__parse_metadata_of_connection(
                self.current_line[start_bracket:]
            )
            self.current_line = self.current_line[:start_bracket]
        splitted = self.current_line.split()

        names_hub = self.__is_valid_names_in_connection(splitted[1])
        self.connections.append(
            Connection(
                names_hub[0], names_hub[1], metadata
            )
        )

    def __parse_metadata_of_connection(self, data: str) -> ConnectionMetadata:
        """Parse connection metadata from a bracketed block.

        Args:
            data: Raw metadata string including the surrounding brackets.
        Returns:
            A dictionary containing parsed metadata values.
        Raises:
            KeyValMetadataError: if metadata not contain (key=value)
            KeyMetadataError: if key not valid
            ValueMaxLinkCapacityError:  raised when MaxLinkCapacity not integer
        """
        metadata: ConnectionMetadata =\
            FactoryMetadata.get_metadata_of_connection()
        data = data[1:-1]
        for key_val_data in data.split():
            pairs = key_val_data.split('=')
            if len(pairs) != 2 or len(pairs[1]) == 0:
                raise KeyValMetadataError(self.current_line, self.line_number)

            if pairs[0] != MetaDataOfConnection.max_link_capacity.name:
                raise KeyMetadataError(
                    self.current_line, self.line_number
                )
            try:
                metadata[MetaDataOfConnection.max_link_capacity.name]\
                    = int(pairs[1])
            except ValueError:
                raise ValueMaxLinkCapacityError(
                    self.current_line, self.line_number
                )
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
            self.start_hub.metadata['max_drones'] = self.nb_drones
        elif type_zone == 'end_hub':
            self.end_hub = new_hub
            self.end_hub.metadata['max_drones'] = self.nb_drones
        else:
            self.hubs.append(new_hub)
        self.__add_name_to_name_zones(new_hub.name)

    def __is_valid_names_in_connection(self, names_hub: str) -> list[str]:
        """validate names in connection if exist name in hubs
            otherwise raise Parsing Error

        Args:
            names_hub: str : contain two names separated by dash -
        Raises:
            DuplicateConnectionError: if connection duplicated in file map
            NotFoundNameHubError: not found hubs by these names
        Returns:
            return list[str] : list has two names froms hubs
        """
        names = names_hub.split('-')

        for conn in self.connections:
            if conn.zone_one == names[0] and conn.zone_two == names[1]:
                raise DuplicateConnectionError(
                    self.current_line, self.line_number
                )
            elif conn.zone_two == names[0] and conn.zone_one == names[1]:
                raise DuplicateConnectionError(
                    self.current_line, self.line_number
                )

        if names[0] not in self.__get_all_hubs_name():
            raise NotFoundNameHubError(self.current_line, self.line_number)
        elif names[1] not in self.__get_all_hubs_name():
            raise NotFoundNameHubError(self.current_line, self.line_number)
        return names

    def __get_all_hubs_name(self) -> list[str]:
        """get names of hub already created
        Args:
            None
        Returns:
            list[str]: [list contain all names of hubs]
        """
        hubs: list[str] = list()
        try:
            hubs.append(self.start_hub.name)
        except AttributeError:
            pass
        try:
            hubs.append(self.end_hub.name)
        except AttributeError:
            pass
        for hub in self.hubs:
            hubs.append(hub.name)
        return hubs

    def __add_name_to_name_zones(self, new_name: str) -> None:
        """add name to name_zones for each hib has a unique name

        Args:
            new_name: new_name of hub
        Raises:
            DuplicateNameHub: if name already exists
        Returns:
            None
        """
        if new_name not in self.name_zones:
            self.name_zones.append(new_name)
            return
        raise DuplicateNameHub(self.current_line, self.line_number)

    def __filter_line(self, line: str) -> str:
        """ filter line method only search if line contains hashtag
            to slice comments and strip it

        Args:
            line: str : raw line from file
        Returns:
            line: filter line and return it
        """
        if line.find('#') != -1:
            return line[:line.find('#')].strip()
        else:
            return line.strip()

    def __is_completed_data(self) -> None:
        """if required data not initialized before or not change flag readline

        Args:
            None
        Raises:
            NotFoundError: start_hub or end_hub not initialized
                or not readed first_line
        Return:
            None
        """
        try:
            if self.start_hub is None:
                raise NotFoundError("start_hub")
        except AttributeError:
            raise NotFoundError("start_hub")
        try:
            if self.end_hub is None:
                raise NotFoundError("end_hub")
        except AttributeError:
            raise NotFoundError("end_hub")
        if self.first_line:
            raise NotFoundError("nb_drones")

    def __parse_content_file(self) -> None:
        """Read and parse the configured input file.

        Args:
            None
        Raises:
            PrefixError: raised when found line start with different prefix
        Returns:
            None
        """
        with open(self.filename, "r") as file:
            for line in file:
                line = self.__filter_line(line)
                self.current_line = line
                self.line_number += 1
                if not len(self.current_line):
                    continue

                if line.startswith("nb_drones:"):
                    self.__parse_number_of_drones()
                    self.first_line = False
                elif line.startswith("start_hub:") or line.startswith("hub:")\
                        or line.startswith('end_hub:'):
                    self.__parse_hub()
                elif line.startswith("connection:"):
                    self.__parse_connection()
                else:
                    raise PrefixError(self.current_line, self.line_number)
        self.__is_completed_data()

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
