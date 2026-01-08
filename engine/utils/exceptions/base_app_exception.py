class BaseAppException(Exception):
    """Base exception for our application"""

    def __init__(self, message: str):
        self.message = message
