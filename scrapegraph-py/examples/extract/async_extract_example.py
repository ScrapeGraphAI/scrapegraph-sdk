"""Async extract structured data from a page using AI."""

import asyncio

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        result = await client.extract(
            url="https://example.com",
            prompt="Extract the page title and description",
        )
        print(result)


asyncio.run(main())
