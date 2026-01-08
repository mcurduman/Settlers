from engine.utils.exceptions.base_app_exception import BaseAppException


class GameEndedException(BaseAppException):
    """
    Raised when an action is attempted after the game has ended.
    """

    def __init__(self, message="The game has ended. No further actions are allowed."):
        super().__init__(message)
