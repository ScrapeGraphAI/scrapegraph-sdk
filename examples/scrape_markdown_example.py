"""
Scrape a webpage and get the content as clean markdown.

This is the simplest way to get readable content from any URL.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.scrape("https://example.com")
print(json.dumps(result, indent=2))

client.close()
