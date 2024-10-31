"""
This module provides a function to scrape and extract structured data from a webpage
using the ScrapeGraph AI API. It allows specifying a schema for the output structure
using a Pydantic model.
"""

from pydantic import BaseModel
import requests

def scrape(api_key: str, url: str, prompt: str, schema: BaseModel) -> str:
    """Scrape and extract structured data from a webpage using ScrapeGraph AI.

    Args:
        api_key (str): Your ScrapeGraph AI API key
        url (str): The URL of the webpage to scrape
        prompt (str): Natural language prompt describing what data to extract
        schema (BaseModel): Pydantic model defining the output structure.
            The model will be converted to JSON schema before making the request.

    Returns:
        str: Extracted data in JSON format matching the provided schema
    """
    endpoint = "https://api.scrapegraph.ai/v1/scrape"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "prompt": prompt,
        "schema": schema.model_json_schema()
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.text
