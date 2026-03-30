"""
Crawl a website and get pages as markdown.

The crawl endpoint discovers and fetches multiple pages from a website,
starting from a given URL and following links up to a specified depth.
"""

import json
import time

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Start the crawl
job = client.crawl.start(
    "https://example.com",
    depth=2,
    max_pages=5,
    format="markdown",
)
print("Crawl started:", json.dumps(job, indent=2))

# Poll for status
crawl_id = job["id"]
while True:
    status = client.crawl.status(crawl_id)
    print(f"Status: {status.get('status')}")
    if status.get("status") in ("completed", "failed"):
        break
    time.sleep(2)

print("\nFinal result:", json.dumps(status, indent=2))

client.close()
