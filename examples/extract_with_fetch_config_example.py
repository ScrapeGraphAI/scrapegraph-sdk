"""
Extract data from a JavaScript-heavy page using FetchConfig.

Use FetchConfig to enable stealth mode, JS rendering, scrolling,
and other options needed for dynamic pages.
"""

import json

from scrapegraph_py import Client, FetchConfig

client = Client()  # uses SGAI_API_KEY env var

result = client.extract(
    url="https://example.com",
    prompt="Extract all visible text content",
    fetch_config=FetchConfig(
        stealth=True,
        render_js=True,
        wait_ms=2000,
        scrolls=3,
    ),
)
print(json.dumps(result, indent=2))

client.close()
