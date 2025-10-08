"""
Helper utility functions for the ScrapeGraphAI SDK.

This module provides utility functions for API key validation and
HTTP response handling for both synchronous and asynchronous requests.
"""

from typing import Any, Dict
from uuid import UUID

import aiohttp
from requests import Response

from scrapegraph_py.exceptions import APIError


def validate_api_key(api_key: str) -> bool:
    """
    Validate the format of a ScrapeGraphAI API key.

    API keys must follow the format: 'sgai-' followed by a valid UUID.

    Args:
        api_key: The API key string to validate

    Returns:
        True if the API key is valid

    Raises:
        ValueError: If the API key format is invalid

    Example:
        >>> validate_api_key("sgai-12345678-1234-1234-1234-123456789abc")
        True
        >>> validate_api_key("invalid-key")
        ValueError: Invalid API key format...
    """
    if not api_key.startswith("sgai-"):
        raise ValueError("Invalid API key format. API key must start with 'sgai-'")
    uuid_part = api_key[5:]  # Strip out 'sgai-'
    try:
        UUID(uuid_part)
    except ValueError:
        raise ValueError(
            "Invalid API key format. API key must be 'sgai-' followed by a valid UUID. "
            "You can get one at https://dashboard.scrapegraphai.com/"
        )
    return True


def handle_sync_response(response: Response) -> Dict[str, Any]:
    """
    Handle and parse synchronous HTTP responses.

    Parses the JSON response and raises APIError for error status codes.

    Args:
        response: The requests Response object

    Returns:
        Parsed JSON response data as a dictionary

    Raises:
        APIError: If the response status code indicates an error (>= 400)

    Example:
        >>> response = requests.get("https://api.example.com/data")
        >>> data = handle_sync_response(response)
    """
    try:
        data = response.json()
    except ValueError:
        # If response is not JSON, use the raw text
        data = {"error": response.text}

    if response.status_code >= 400:
        error_msg = data.get(
            "error", data.get("detail", f"HTTP {response.status_code}: {response.text}")
        )
        raise APIError(error_msg, status_code=response.status_code)

    return data


async def handle_async_response(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    """
    Handle and parse asynchronous HTTP responses.

    Parses the JSON response and raises APIError for error status codes.

    Args:
        response: The aiohttp ClientResponse object

    Returns:
        Parsed JSON response data as a dictionary

    Raises:
        APIError: If the response status code indicates an error (>= 400)

    Example:
        >>> async with session.get("https://api.example.com/data") as response:
        ...     data = await handle_async_response(response)
    """
    try:
        data = await response.json()
        text = None
    except ValueError:
        # If response is not JSON, use the raw text
        text = await response.text()
        data = {"error": text}

    if response.status >= 400:
        if text is None:
            text = await response.text()
        error_msg = data.get(
            "error", data.get("detail", f"HTTP {response.status}: {text}")
        )
        raise APIError(error_msg, status_code=response.status)

    return data
