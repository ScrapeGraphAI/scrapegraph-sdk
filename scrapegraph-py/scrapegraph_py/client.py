"""
Module for ScrapeGraph Client

This module contains the ScrapeGraphClient class, which provides methods to interact
with the ScrapeGraph AI API. It allows users to initialize the client with an API key,
retrieve necessary headers for API requests, and construct full endpoint URLs for
making requests to the ScrapeGraph API. This facilitates seamless integration with
ScrapeGraph AI services.
"""

class ScrapeGraphClient:
    """Client for interacting with the ScrapeGraph AI API.

    This class provides methods to initialize the client with an API key and base URL,
    retrieve headers for API requests, and construct full endpoint URLs for making
    requests to the ScrapeGraph API. It is designed to facilitate seamless interaction
    with the ScrapeGraph AI services.

    Attributes:
        api_key (str): Your ScrapeGraph AI API key.
        base_url (str): Base URL for the API, defaulting to "https://api.scrapegraphai.com/v1".
    """

    def __init__(self, api_key: str, base_url: str = "https://api.scrapegraphai.com/v1"):
        """Initialize the ScrapeGraph client.
        
        Args:
            api_key (str): Your ScrapeGraph AI API key.
            base_url (str): Base URL for the API (optional, defaults 
            to "https://api.scrapegraphai.com/v1").
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def get_headers(self, include_content_type: bool = True) -> dict:
        """Get the headers for API requests.
        
        Args:
            include_content_type (bool): Whether to include the Content-Type header 
            (default is True).
            
        Returns:
            dict: A dictionary containing the headers for the API request, including
                  the API key and optionally the Content-Type.
        """
        headers = {
            "accept": "application/json",
            "SGAI-APIKEY": self.api_key
        }

        if include_content_type:
            headers["Content-Type"] = "application/json"
 
        return headers

    def get_endpoint(self, path: str) -> str:
        """Get the full endpoint URL.
        
        Args:
            path (str): The API endpoint path to be appended to the base URL.
            
        Returns:
            str: The full endpoint URL constructed from the base URL and the provided path.
        """
        return f"{self.base_url}/{path}"
