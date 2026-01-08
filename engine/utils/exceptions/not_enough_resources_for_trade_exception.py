from engine.utils.exceptions.base_app_exception import BaseAppException


class NotEnoughResourcesForTradeException(BaseAppException):
    """Raised when a player does not have enough resources to complete a trade with the bank."""

    def __init__(
        self, message: str = "Not enough resources to complete trade with bank"
    ):
        super().__init__(message, status_code=400)
