
class ScrapeGraphClient:
    """Client for interacting with the ScrapeGraph AI API."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.scrapegraphai.com/v1"):
        """Initialize the ScrapeGraph client.
        
        Args:
            api_key (str): Your ScrapeGraph AI API key
            base_url (str): Base URL for the API (optional)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
    def get_headers(self, include_content_type: bool = True) -> dict:
        """Get the headers for API requests.
        
        Args:
            include_content_type (bool): Whether to include Content-Type header
            
        Returns:
            dict: Headers for the API request
        """
        headers = {
            "accept": "application/json",
            "SGAI-API-KEY": self.api_key
        }
        
        if include_content_type:
            headers["Content-Type"] = "application/json"
            
        return headers
    
    def get_endpoint(self, path: str) -> str:
        """Get the full endpoint URL.
        
        Args:
            path (str): API endpoint path
            
        Returns:
            str: Full endpoint URL
        """
        return f"{self.base_url}/api/v1/{path}"