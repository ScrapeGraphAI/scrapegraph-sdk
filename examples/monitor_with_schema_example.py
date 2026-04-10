"""
Create a monitor with a JSON Schema for structured output.

The output_schema ensures each extraction returns data in a
consistent format.
"""

import json

from scrapegraph_py import Client

schema = {
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "price": {"type": "number"},
                    "currency": {"type": "string"},
                },
                "required": ["name", "price"],
            },
        },
    },
}

client = Client()  # uses SGAI_API_KEY env var

monitor = client.monitor.create(
    name="Weekly Product Monitor",
    url="https://example.com/shop",
    prompt="Extract all product names, prices, and currencies",
    interval="0 8 * * 1",  # Every Monday at 8am
    output_schema=schema,
)
print("Monitor created:", json.dumps(monitor, indent=2))

client.close()
