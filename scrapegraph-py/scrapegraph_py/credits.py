"""
This module provides functionality to interact with the ScrapeGraph AI API.

It includes functions to retrieve credits and send feedback, 
handling responses and errors appropriately.
"""

import requests
from .client import ScrapeGraphClient
from .exceptions import raise_for_status_code, APIError

def credits(client: ScrapeGraphClient) -> str:
    """Retrieve credits from the API.

    Args:
        client (ScrapeGraphClient): Initialized ScrapeGraph client

    Returns:
        str: Response from the API in JSON format.
    """
    endpoint = client.get_endpoint("credits")
    headers = client.get_headers(include_content_type=False)

    try:
        response = requests.get(endpoint, headers=headers)
        raise_for_status_code(response.status_code, response)
        return response.text
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request failed: {str(e)}", response=None)
