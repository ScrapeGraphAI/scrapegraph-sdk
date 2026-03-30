"""Async scrape a page and get markdown content."""

import asyncio

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        result = await client.scrape("https://example.com")
        print(result)

        result = await client.scrape("https://example.com", format="html")
        print(result)


asyncio.run(main())
