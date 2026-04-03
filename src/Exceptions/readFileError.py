class ReadFileError(Exception):
    def __init__(self):
        super().__init__("Error: Cannot read file!")
