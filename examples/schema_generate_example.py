"""
Generate a JSON Schema from a natural language description.

Useful when you want the AI to design the output structure for you
before running an extraction.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.schema(
    prompt="An e-commerce product with name, price, description, rating, number of reviews, and availability status"
)
print(json.dumps(result, indent=2))

client.close()
