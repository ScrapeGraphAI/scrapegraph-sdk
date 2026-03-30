"""
Scrape a webpage and capture a screenshot.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.scrape("https://example.com", format="screenshot")
print(json.dumps(result, indent=2))

client.close()
