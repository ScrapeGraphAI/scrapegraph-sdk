"""
Stop and resume a crawl job.

You can stop a running crawl and resume it later.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Start a crawl
job = client.crawl.start("https://example.com", depth=3, max_pages=50)
crawl_id = job["id"]
print("Crawl started:", crawl_id)

# Stop the crawl
stopped = client.crawl.stop(crawl_id)
print("Stopped:", json.dumps(stopped, indent=2))

# Resume the crawl later
resumed = client.crawl.resume(crawl_id)
print("Resumed:", json.dumps(resumed, indent=2))

client.close()
