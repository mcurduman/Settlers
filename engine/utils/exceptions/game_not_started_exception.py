from engine.utils.exceptions.base_app_exception import BaseAppException


class GameNotStartedException(BaseAppException):
    """Raised when an operation is attempted but the game has not been started."""

    def __init__(self, message: str):
        super().__init__(message)
