"""
Module for Scraping Web Data with ScrapeGraph AI

This module provides functionality to scrape and extract structured data from
webpages using the ScrapeGraph AI API. It defines the `scrape` function, which
takes a ScrapeGraph client, a URL, a user prompt, and an optional Pydantic schema
to specify the desired output structure. The extracted data is returned in JSON
format, adhering to the specified schema if provided. This module is designed to
facilitate the integration of web scraping capabilities into applications utilizing
ScrapeGraph AI services.
"""
from typing import Optional

from pydantic import BaseModel
import requests
from .client import ScrapeGraphClient
from .exceptions import APIError, raise_for_status_code

def smart_scraper(client: ScrapeGraphClient, url: str, prompt: str, 
           schema: Optional[BaseModel] = None) -> str:
    """smart_scraper and extract structured data from a webpage using ScrapeGraph AI.

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
        "user_prompt": prompt,
        "output_schema": {}
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
        response = requests.post(endpoint, headers=headers, json=payload, timeout=10)
        raise_for_status_code(response.status_code, response)
        return response.text
    except requests.exceptions.RequestException as e:
        raise APIError(f"Request failed: {str(e)}", response=None)
