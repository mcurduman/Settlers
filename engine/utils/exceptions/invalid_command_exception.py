class InvalidCommandException(Exception):
    """
    Raised when an invalid or unsupported command is attempted in the game.
    """

    def __init__(self, message="Invalid command."):
        super().__init__(message)
