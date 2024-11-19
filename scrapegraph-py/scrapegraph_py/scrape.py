from pydantic import BaseModel
import requests
from typing import Optional
import json
from .client import ScrapeGraphClient
from .exceptions import APIError

def raise_for_status_code(status_code: int, response: requests.Response):
    if status_code >= 400:
        raise APIError(f"API request failed with status {status_code}", response=response)

def scrape(client: ScrapeGraphClient, url: str, prompt: str, schema: Optional[BaseModel] = None) -> str:
    """Scrape and extract structured data from a webpage using ScrapeGraph AI.

    Args:
        client (ScrapeGraphClient): Initialized ScrapeGraph client
        url (str): The URL of the webpage to scrape
        prompt (str): Natural language prompt describing what data to extract
        schema (Optional[BaseModel]): Pydantic model defining the output structure,
            if provided. The model will be converted to JSON schema before making 
            the request

    Returns:
        str: Extracted data in JSON format matching the provided schema
    """
    endpoint = client.get_endpoint("smartscraper")
    headers = client.get_headers()
    
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
        raise_for_status_code(response.status_code, response)
        return response.text
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request failed: {str(e)}", response=None)