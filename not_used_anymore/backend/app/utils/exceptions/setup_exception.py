from app.utils.exceptions.base_app_exception import BaseAppException


class SetupException(BaseAppException):
    """Raised when there is an error during the setup phase of the game"""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)
