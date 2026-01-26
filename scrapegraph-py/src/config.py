"""
Configuration and constants for the ScrapeGraphAI SDK.

This module contains API configuration settings including the base URL
and default headers used for all API requests.

Attributes:
    API_BASE_URL (str): Base URL for the ScrapeGraphAI API endpoints
    DEFAULT_HEADERS (dict): Default HTTP headers for API requests
"""
API_BASE_URL = "https://api.scrapegraphai.com/v1"
DEFAULT_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}
