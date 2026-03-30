"""Crawl a website and get pages as markdown."""

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Start a crawl
job = client.crawl.start(
    "https://example.com",
    depth=2,
    max_pages=10,
    format="markdown",
)
print("Crawl started:", job)

# Check status
crawl_id = job["id"]
status = client.crawl.status(crawl_id)
print("Crawl status:", status)

# Stop if needed
# client.crawl.stop(crawl_id)

# Resume if stopped
# client.crawl.resume(crawl_id)

client.close()
