"""
Helper utility functions for the ScrapeGraphAI SDK v2.
"""

from typing import Any, Dict

import aiohttp
from requests import Response

from scrapegraph_py.exceptions import APIError


def validate_api_key(api_key: str) -> bool:
    """Validate that an API key is present and non-empty.

    Args:
        api_key: The API key string to validate

    Returns:
        True if the API key is valid

    Raises:
        ValueError: If the API key is empty or missing
    """
    if not api_key or not api_key.strip():
        raise ValueError(
            "API key cannot be empty. "
            "Get one at https://dashboard.scrapegraphai.com/"
        )
    return True


def handle_sync_response(response: Response) -> Dict[str, Any]:
    """Handle and parse synchronous HTTP responses.

    Args:
        response: The requests Response object

    Returns:
        Parsed JSON response data as a dictionary

    Raises:
        APIError: If the response status code indicates an error (>= 400)
    """
    try:
        data = response.json()
    except ValueError:
        data = {"error": response.text}

    if response.status_code >= 400:
        error_msg = data.get(
            "error", data.get("detail", f"HTTP {response.status_code}: {response.text}")
        )
        raise APIError(error_msg, status_code=response.status_code)

    return data


async def handle_async_response(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    """Handle and parse asynchronous HTTP responses.

    Args:
        response: The aiohttp ClientResponse object

    Returns:
        Parsed JSON response data as a dictionary

    Raises:
        APIError: If the response status code indicates an error (>= 400)
    """
    try:
        data = await response.json()
        text = None
    except ValueError:
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
