from app.utils.exceptions.base_app_exception import BaseAppException


class SettlementException(BaseAppException):
    """Raised when there is an error related to settlement placement or management"""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)
