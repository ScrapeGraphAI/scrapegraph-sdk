from pydantic import BaseModel
import requests
from typing import Optional
import json

def scrape(api_key: str, url: str, prompt: str, schema: Optional[BaseModel] = None) -> str:
    """Scrape and extract structured data from a webpage using ScrapeGraph AI.

    Args:
        api_key (str): Your ScrapeGraph AI API key.
        url (str): The URL of the webpage to scrape.
        prompt (str): Natural language prompt describing what data to extract.
        schema (Optional[BaseModel]): Pydantic model defining the output structure,
            if provided. The model will be converted to JSON schema before making 
            the request.

    Returns:
        str: Extracted data in JSON format matching the provided schema.
    """
    endpoint = "https://sgai-api.onrender.com/api/v1/smartscraper"
    headers = {
        "accept": "application/json",
        "SGAI-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "website_url": url,
        "user_prompt": prompt
    }
    
    if schema:
        schema_json = schema.model_json_schema()
        payload["output_schema"] = {
            "description": schema_json.get("title", "Schema"),
            "name": schema_json.get("title", "Schema"),
            "properties": schema_json.get("properties", {}),
            "required": schema_json.get("required", [])
        }
    
    try:
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        # Handle HTTP errors specifically
        if response.status_code == 403:
            return json.dumps({"error": "Access forbidden (403)", "message": "You do not have permission to access this resource."})
        return json.dumps({"error": "HTTP error occurred", "message": str(http_err), "status_code": response.status_code})
    except requests.exceptions.RequestException as e:
        # Handle other request exceptions (e.g., connection errors, timeouts)
        return json.dumps({"error": "An error occurred", "message": str(e)})
    
    return response.text
