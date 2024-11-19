class APIError(Exception):
    """Base class for API exceptions."""
    def __init__(self, message=None, response=None):
        self.message = message or self.__doc__
        self.response = response
        super().__init__(self.message)

class AuthenticationError(APIError):
    """Raised when API key is invalid or missing."""

class RateLimitError(APIError):
    """Raised when rate limits are exceeded."""
    def __init__(self, message=None, reset_time=None, response=None):
        super().__init__(message, response)
        self.reset_time = reset_time

class BadRequestError(APIError):
    """Raised when a 400 Bad Request error occurs."""

class InternalServerError(APIError):
    """Raised when a 500 Internal Server Error occurs."""
