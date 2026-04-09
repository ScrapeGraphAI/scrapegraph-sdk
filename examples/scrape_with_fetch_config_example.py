"""
Scrape a webpage with custom fetch configuration.

FetchConfig allows you to control the fetch mode (proxy strategy),
wait times, cookies, headers, country-based geolocation, and more.

Available modes:
  - auto: Automatically selects the best provider chain (default)
  - fast: Direct HTTP fetch, fastest option, no JS rendering
  - js: Headless browser rendering for JavaScript-heavy pages
  - direct+stealth: Residential proxy with stealth headers (no JS)
  - js+stealth: JS rendering combined with stealth/residential proxy
"""

import json

from scrapegraph_py import Client, FetchConfig

client = Client()  # uses SGAI_API_KEY env var

result = client.scrape(
    "https://example.com",
    format="markdown",
    fetch_config=FetchConfig(
        mode="js+stealth",
        wait=3000,
        headers={"User-Agent": "MyBot/1.0"},
        cookies={"session": "abc123"},
        country="us",
    ),
)
print(json.dumps(result, indent=2))

client.close()
