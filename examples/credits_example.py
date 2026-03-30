"""
Check your remaining API credits.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

credits = client.credits()
print(json.dumps(credits, indent=2))

client.close()
