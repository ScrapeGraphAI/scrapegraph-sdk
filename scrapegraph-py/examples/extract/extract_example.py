"""Extract structured data from a page using AI."""

from pydantic import BaseModel, Field

from scrapegraph_py import Client


class Product(BaseModel):
    name: str = Field(description="Product name")
    price: float = Field(description="Product price")


client = Client()  # uses SGAI_API_KEY env var

# Extract with a prompt
result = client.extract(
    url="https://example.com",
    prompt="Extract the page title and description",
)
print(result)

# Extract with a Pydantic schema
result = client.extract(
    url="https://example.com",
    prompt="Extract product information",
    output_schema=Product,
)
print(result)

client.close()
