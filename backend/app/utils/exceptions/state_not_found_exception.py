from app.utils.exceptions.base_app_exception import BaseAppException


class StateNotFoundException(BaseAppException):
    """Raised when a requested game state is not found"""

    def __init__(self, message: str):
        super().__init__(message, status_code=404)
