"""
Crawl with custom fetch configuration.

Use FetchConfig to set the fetch mode, wait time, etc. for all
pages during the crawl.
"""

import json

from scrapegraph_py import Client, FetchConfig

client = Client()  # uses SGAI_API_KEY env var

job = client.crawl.start(
    "https://example.com",
    depth=2,
    max_pages=10,
    format="html",
    fetch_config=FetchConfig(
        mode="js",
        wait=1000,
    ),
)
print("Crawl started:", json.dumps(job, indent=2))

client.close()
