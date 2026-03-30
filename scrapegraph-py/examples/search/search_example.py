"""Search the web and extract structured results."""

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

result = client.search("best python web scraping libraries 2025", num_results=5)
print(result)

client.close()
