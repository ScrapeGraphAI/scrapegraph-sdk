"""
This module provides a function to scrape and extract structured data from a webpage
using the ScrapeGraph AI API. It allows specifying a schema for the output structure
using either a dictionary or a Pydantic model.
"""

from typing import Union
from pydantic import BaseModel
import requests

def scrape(api_key: str, url: str, prompt: str, schema: Union[dict, BaseModel, None] = None) -> str:
    """Scrape and extract structured data from a webpage using ScrapeGraph AI.

    Args:
        api_key (str): Your ScrapeGraph AI API key
        url (str): The URL of the webpage to scrape
        prompt (str): Natural language prompt describing what data to extract
        schema (Union[dict, BaseModel, None], optional): Schema definition for the output structure.
            Can be either a dictionary or a Pydantic model. If None, returns raw JSON.

    Returns:
        str: Extracted data in JSON format matching the provided schema (if specified)
    """
    endpoint = "https://api.scrapegraph.ai/v1/scrape"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "prompt": prompt,
        "schema": schema.dict() if isinstance(schema, BaseModel) else schema if schema is not None else None
    }
    
    response = requests.post(endpoint, headers=headers, json=payload)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    return response.text
