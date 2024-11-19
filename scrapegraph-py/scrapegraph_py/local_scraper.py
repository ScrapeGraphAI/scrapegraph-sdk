from pydantic import BaseModel
import requests
from typing import Optional
import json
from .client import ScrapeGraphClient
from .exceptions import raise_for_status_code, APIError

def scrape_text(client: ScrapeGraphClient, website_text: str, prompt: str, schema: Optional[BaseModel] = None) -> str:
    """Scrape and extract structured data from website text using ScrapeGraph AI.

    Args:
        client (ScrapeGraphClient): Initialized ScrapeGraph client
        website_text (str): The text content to analyze
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
        "website_text": website_text,
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
