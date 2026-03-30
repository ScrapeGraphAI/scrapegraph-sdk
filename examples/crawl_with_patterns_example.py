"""
Crawl a website with URL pattern filtering.

Use include_patterns and exclude_patterns to control which pages
the crawler visits. Patterns support * (any chars) and ** (any path segments).
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

job = client.crawl.start(
    "https://example.com",
    depth=3,
    max_pages=20,
    format="markdown",
    include_patterns=["/blog/*", "/docs/**"],
    exclude_patterns=["/admin/*", "/api/*"],
)
print("Crawl started:", json.dumps(job, indent=2))

client.close()
