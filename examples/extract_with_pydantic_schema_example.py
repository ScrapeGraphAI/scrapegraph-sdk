"""
Extract structured data using a Pydantic model as the output schema.

When you pass a Pydantic BaseModel class, the SDK automatically converts
it to a JSON Schema and sends it to the API. This ensures the response
matches your expected structure.
"""

import json
from typing import List, Optional

from pydantic import BaseModel, Field

from scrapegraph_py import Client


class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Product price in USD")
    description: Optional[str] = Field(description="Product description")
    in_stock: bool = Field(description="Whether the product is in stock")


class ProductList(BaseModel):
    products: List[Product] = Field(description="List of products found on the page")


client = Client()  # uses SGAI_API_KEY env var

result = client.extract(
    url="https://example.com",
    prompt="Extract all products with their prices and availability",
    output_schema=ProductList,
)
print(json.dumps(result, indent=2))

client.close()
