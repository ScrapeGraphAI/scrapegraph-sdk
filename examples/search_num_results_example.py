"""
Search with a custom number of results.

num_results controls how many web pages are scraped (3-20).
More results = more comprehensive but costs more credits.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Get more results for deeper research
result = client.search(
    query="machine learning frameworks comparison",
    num_results=10,
)
print(json.dumps(result, indent=2))

client.close()
