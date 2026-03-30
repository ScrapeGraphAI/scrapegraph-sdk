"""
Extract structured data using a raw JSON Schema dict.

You can pass a JSON Schema dictionary directly if you prefer not to
use Pydantic models.
"""

import json

from scrapegraph_py import Client

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "Page title"},
        "links": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "href": {"type": "string"},
                },
            },
            "description": "All links on the page",
        },
    },
    "required": ["title", "links"],
}

client = Client()  # uses SGAI_API_KEY env var

result = client.extract(
    url="https://example.com",
    prompt="Extract the page title and all links",
    output_schema=schema,
)
print(json.dumps(result, indent=2))

client.close()
