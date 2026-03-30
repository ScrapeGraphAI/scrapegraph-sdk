"""
Async scrape example - scrape multiple pages concurrently.
"""

import asyncio
import json

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        # Scrape multiple pages concurrently
        urls = [
            "https://example.com",
            "https://httpbin.org/html",
        ]

        tasks = [client.scrape(url) for url in urls]
        results = await asyncio.gather(*tasks)

        for url, result in zip(urls, results):
            print(f"\n=== {url} ===")
            print(json.dumps(result, indent=2))


asyncio.run(main())
