"""
Retrieve your API request history.

The history endpoint lets you review past requests with optional filters.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Get all recent history
history = client.history()
print("Recent history:", json.dumps(history, indent=2))

# Filter by endpoint
scrape_history = client.history(endpoint="scrape", limit=5)
print("\nScrape history:", json.dumps(scrape_history, indent=2))

# Filter by status
completed = client.history(status="completed", limit=10)
print("\nCompleted requests:", json.dumps(completed, indent=2))

# Paginate
page2 = client.history(limit=10, offset=10)
print("\nPage 2:", json.dumps(page2, indent=2))

client.close()
