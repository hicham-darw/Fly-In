class ParsingError(Exception):
    """Custom Exception if found error when parsing files
    """
    def __init__(self, msg: str) -> None:
        """Constructor of object

        Args:
            msg: (str): msg of error raised
        Returns:
            None
        """
        super().__init__(msg)
