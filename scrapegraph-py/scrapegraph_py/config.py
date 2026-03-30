"""
Configuration and constants for the ScrapeGraphAI SDK v2.
"""

VERSION = "2.0.0"
API_BASE_URL = "https://api.scrapegraphai.com/api/v1"
DEFAULT_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "X-SDK-Version": f"python@{VERSION}",
}
