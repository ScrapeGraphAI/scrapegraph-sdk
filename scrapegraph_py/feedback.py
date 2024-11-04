"""
This module provides functionality to send feedback to the ScrapeGraph AI API.

It includes a function to send feedback messages along with the necessary API key
and handles responses and errors appropriately.
"""

import requests
import json

def feedback(api_key: str, request_id: str, rating: int, feedback_text: str) -> str:
    """Send feedback to the API.

    Args:
        api_key (str): Your ScrapeGraph AI API key.
        request_id (str): The request ID associated with the feedback.
        rating (int): The rating score.
        feedback_text (str): The feedback message to send.

    Returns:
        str: Response from the API in JSON format.
    """
    endpoint = "https://sgai-api.onrender.com/api/v1/feedback"
    headers = {
        "accept": "application/json",
        "SGAI-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    feedback_data = {
        "request_id": request_id,
        "rating": rating,
        "feedback_text": feedback_text
    }  

    try:
        response = requests.post(endpoint, headers=headers, json=feedback_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return json.dumps({"error": "HTTP error occurred", "message": str(http_err), "status_code": response.status_code})
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "An error occurred", "message": str(e)})
    
    return response.text
