import pytest
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from scrapegraphaiapisdk.scrape import scrape

# Load environment variables from .env file
load_dotenv()

class Product(BaseModel):
    name: str
    price: float
    description: str

class ProductList(BaseModel):
    products: List[Product]

def test_scrape_successful():
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    url = "https://example.com/products"
    prompt = "Extract all products"
    schema = ProductList
    
    # Mock the response
    with pytest.mock.patch('requests.post') as mock_post:
        mock_post.return_value.text = '{"products": [{"name": "Test Product", "price": 99.99, "description": "Test Description"}]}'
        mock_post.return_value.raise_for_status.return_value = None
        
        result = scrape(api_key, url, prompt, schema)
        assert isinstance(result, str)
        assert "Test Product" in result

def test_scrape_invalid_api_key():
    api_key = "invalid_key"
    url = "https://example.com/products"
    prompt = "Extract all products"
    schema = ProductList
    
    with pytest.mock.patch('requests.post') as mock_post:
        mock_post.side_effect = Exception("Invalid API key")
        
        with pytest.raises(Exception):
            scrape(api_key, url, prompt, schema) 