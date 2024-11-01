"""
This module provides functionality to interact with the ScrapeGraph AI API.

It includes functions to retrieve credits and send feedback, handling responses and errors appropriately.
"""

import requests
import json

def credits(api_key: str) -> str:
    """Retrieve credits from the API.

    Args:
        api_key (str): Your ScrapeGraph AI API key.

    Returns:
        str: Response from the API in JSON format.
    """
    endpoint = "https://sgai-api.onrender.com/api/v1/credits"
    headers = {
        "accept": "application/json",
        "SGAI-API-KEY": api_key
    }

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return json.dumps({"error": "HTTP error occurred", "message": str(http_err), "status_code": response.status_code})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "An error occurred", "message": str(e)})

    return response.text
