"""
Refine an existing JSON Schema by adding new fields.

Pass an existing schema and ask the AI to extend it.
"""

import json

from scrapegraph_py import Client

existing_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "number"},
    },
    "required": ["name", "price"],
}

client = Client()  # uses SGAI_API_KEY env var

result = client.schema(
    prompt="Add fields for product images (list of URLs), brand name, and SKU",
    existing_schema=existing_schema,
)
print(json.dumps(result, indent=2))

client.close()
