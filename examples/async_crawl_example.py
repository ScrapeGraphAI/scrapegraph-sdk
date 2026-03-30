"""
Async crawl example.
"""

import asyncio
import json

from scrapegraph_py import AsyncClient


async def main():
    async with AsyncClient() as client:
        # Start crawl
        job = await client.crawl.start(
            "https://example.com",
            depth=2,
            max_pages=5,
        )
        print("Crawl started:", json.dumps(job, indent=2))

        # Poll for completion
        crawl_id = job["id"]
        while True:
            status = await client.crawl.status(crawl_id)
            print(f"Status: {status.get('status')}")
            if status.get("status") in ("completed", "failed"):
                break
            await asyncio.sleep(2)

        print("\nResult:", json.dumps(status, indent=2))


asyncio.run(main())
