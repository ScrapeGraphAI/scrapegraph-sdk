"""
Create a monitor to track changes on a webpage.

Monitors run on a cron schedule and use AI to extract data each time.
This replaces the old scheduled jobs API.
"""

import json

from scrapegraph_py import Client

client = Client()  # uses SGAI_API_KEY env var

monitor = client.monitor.create(
    name="Daily Price Tracker",
    url="https://example.com/products",
    prompt="Extract all product names and prices",
    cron="0 9 * * *",  # Every day at 9am
)
print("Monitor created:", json.dumps(monitor, indent=2))

client.close()
