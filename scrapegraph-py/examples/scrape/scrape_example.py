"""Scrape a page and get markdown content."""

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

# Scrape as markdown (default)
result = client.scrape("https://example.com")
print(result)

# Scrape as HTML
result = client.scrape("https://example.com", format="html")
print(result)

client.close()
