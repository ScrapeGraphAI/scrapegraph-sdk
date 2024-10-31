import os
from dotenv import load_dotenv
from scrapegraphaiapisdk.scrape import scrape
from pydantic import BaseModel
from typing import List

# Load environment variables from .env file
load_dotenv()

class Product(BaseModel):
    name: str
    price: float
    description: str

class ProductList(BaseModel):
    products: List[Product]

def main():
    # Get API key from environment variables
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    
    # URL to scrape
    url = "https://example.com/products"
    
    # Natural language prompt
    prompt = "Extract all products from this page including their names, prices, and descriptions"
    
    # Create schema
    schema = ProductList
    
    # Make the request
    try:
        result = scrape(api_key, url, prompt, schema)
        print(f"Scraped data: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main() 