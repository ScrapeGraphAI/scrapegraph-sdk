"""
Module for ScrapeGraph Exceptions

This module defines custom exception classes for handling errors that may occur
when interacting with the ScrapeGraph API. These exceptions provide a structured
way to manage different types of errors, such as authentication issues, rate limits,
bad requests, and server errors. Each exception class inherits from a base exception
class, allowing for more granular error handling in client applications.
"""

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

class ScrapeGraphException(Exception):
    """Base exception for ScrapeGraph errors"""
    pass

def raise_for_status_code(status_code: int, response_text: str = None):
    """
    Raise appropriate exception based on HTTP status code.
    
    Args:
        status_code (int): The HTTP status code returned from the API response.
        response_text (str): Optional text providing additional context for the error.
    
    Raises:
        ScrapeGraphException: For various HTTP error statuses, including 401, 403, 404, and 500.
    """
    if 200 <= status_code < 300:
        return

    error_message = f"HTTP {status_code}"
    if response_text:
        error_message += f": {response_text}"

    if status_code == 401:
        raise ScrapeGraphException("Unauthorized - Invalid API key")
    elif status_code == 403:
        raise ScrapeGraphException("Forbidden - You don't have access to this resource")
    elif status_code == 404:
        raise ScrapeGraphException("Not Found - The requested resource doesn't exist")
    elif status_code >= 500:
        raise ScrapeGraphException("Server Error - Something went wrong on our end")
    else:
        raise ScrapeGraphException(error_message)
