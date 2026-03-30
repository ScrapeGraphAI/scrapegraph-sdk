"""
Scrape a webpage with custom fetch configuration.

FetchConfig allows you to control stealth mode, JavaScript rendering,
wait times, cookies, headers, country-based geolocation, and more.
"""

import json

from scrapegraph_py import Client, FetchConfig

client = Client()  # uses SGAI_API_KEY env var

result = client.scrape(
    "https://example.com",
    format="markdown",
    fetch_config=FetchConfig(
        stealth=True,
        render_js=True,
        wait_ms=3000,
        headers={"User-Agent": "MyBot/1.0"},
        cookies={"session": "abc123"},
        country="us",
    ),
)
print(json.dumps(result, indent=2))

client.close()
