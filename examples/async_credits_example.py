"""
Async credits check.
"""

import asyncio
import json

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        credits = await client.credits()
        print(json.dumps(credits, indent=2))


asyncio.run(main())
