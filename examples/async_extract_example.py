"""
Async extract example - extract data from multiple pages concurrently.
"""

import asyncio
import json

from pydantic import BaseModel, Field

from scrapegraph_py import AsyncClient


class PageInfo(BaseModel):
    title: str = Field(description="Page title")
    description: str = Field(description="Brief description of the page content")


async def main():
    async with AsyncClient() as client:
        urls = [
            "https://example.com",
            "https://httpbin.org/html",
        ]

        tasks = [
            client.extract(
                url=url,
                prompt="Extract the page title and a brief description",
                output_schema=PageInfo,
            )
            for url in urls
        ]
        results = await asyncio.gather(*tasks)

        for url, result in zip(urls, results):
            print(f"\n=== {url} ===")
            print(json.dumps(result, indent=2))


asyncio.run(main())
