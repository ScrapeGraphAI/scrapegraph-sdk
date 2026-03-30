"""
Async search example - run multiple searches concurrently.
"""

import asyncio
import json

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        queries = [
            "best python frameworks 2025",
            "top javascript libraries 2025",
        ]

        tasks = [client.search(q, num_results=3) for q in queries]
        results = await asyncio.gather(*tasks)

        for query, result in zip(queries, results):
            print(f"\n=== {query} ===")
            print(json.dumps(result, indent=2))


asyncio.run(main())
