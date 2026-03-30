"""
Search the web and get AI-extracted results.

The search endpoint performs a web search and uses AI to extract
structured data from the results.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.search("best python web scraping libraries 2025")
print(json.dumps(result, indent=2))

client.close()
