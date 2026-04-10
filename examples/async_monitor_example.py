"""
Async monitor example.
"""

import asyncio
import json

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        # Create a monitor
        monitor = await client.monitor.create(
            name="Async Price Tracker",
            url="https://example.com/products",
            prompt="Extract product prices",
            interval="0 12 * * *",  # Every day at noon
        )
        print("Created:", json.dumps(monitor, indent=2))

        # List all monitors
        all_monitors = await client.monitor.list()
        print("\nAll monitors:", json.dumps(all_monitors, indent=2))


asyncio.run(main())
