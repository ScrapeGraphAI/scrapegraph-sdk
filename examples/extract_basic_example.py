"""
Extract structured data from a webpage using a natural language prompt.

The extract endpoint uses AI to understand your prompt and pull out
exactly the data you need.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.extract(
    url="https://example.com",
    prompt="Extract the page title and main description",
)
print(json.dumps(result, indent=2))

client.close()
