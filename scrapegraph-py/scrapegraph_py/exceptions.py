"""
Custom exceptions for the ScrapeGraphAI SDK.

This module defines custom exception classes used throughout the SDK
for handling API errors and other exceptional conditions.
"""


class APIError(Exception):
    """
    Exception raised for API errors.

    This exception is raised when the API returns an error response,
    providing both the error message and HTTP status code for debugging.

    Attributes:
        message (str): The error message from the API
        status_code (int): HTTP status code of the error response

    Example:
        >>> try:
        ...     client.smartscraper(website_url="invalid")
        ... except APIError as e:
        ...     print(f"API error {e.status_code}: {e.message}")
    """

    def __init__(self, message: str, status_code: int = None):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")
