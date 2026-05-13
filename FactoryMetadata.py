from DataClasses import HubMetadata, ConnectionMetadata
from Enums import MetaDataOfHub, MetaDataOfConnection, TypeZone


class FactoryMetadata:

    @classmethod
    def get_metadata_of_hub(cls) -> HubMetadata:
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

    @classmethod
    def get_metadata_of_connection(cls) -> ConnectionMetadata:
        """method return default metadata of connection

        Args:
            None
        Returns:
            dictionary : default metadata of connection
        """
        return {
            MetaDataOfConnection.max_link_capacity.name: 1
        }
