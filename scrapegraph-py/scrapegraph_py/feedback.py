"""
This module provides functionality to send feedback to the ScrapeGraph AI API.

It includes a function to send feedback messages along with the necessary API key
and handles responses and errors appropriately.
"""

import requests
import json
from .client import ScrapeGraphClient
from .exceptions import APIError, BadRequestError

def feedback(client: ScrapeGraphClient, request_id: str, rating: int, feedback_text: str) -> str:
    """Send feedback to the API.

    Args:
        client (ScrapeGraphClient): Initialized ScrapeGraph client
        request_id (str): The request ID associated with the feedback
        rating (int): The rating score
        feedback_text (str): The feedback message to send

    Returns:
        str: Response from the API in JSON format.
    """
    # Validate rating
    if not 0 <= rating <= 5:
        raise BadRequestError("Rating must be between 0 and 5")

    endpoint = client.get_endpoint("feedback")
    headers = client.get_headers()
    
    feedback_data = {
        "request_id": request_id,
        "rating": rating,
        "feedback_text": feedback_text
    }

    try:
        response = requests.post(endpoint, headers=headers, json=feedback_data, timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request failed: {str(e)}", response=None) from e
