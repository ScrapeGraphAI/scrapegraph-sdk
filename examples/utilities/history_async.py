from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import AsyncScrapeGraphAI, HistoryFilter

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.history.list(HistoryFilter(limit=5))

        if res.status == "success":
            data = res.data
            print(f"Total: {data.pagination.total}")
            print(f"Page: {data.pagination.page} / {(data.pagination.total // data.pagination.limit) + 1}")

            for entry in data.data:
                print(f"\n  ID: {entry.id}")
                print(f"  Service: {entry.service}")
                print(f"  Status: {entry.status}")
                print(f"  Created: {entry.created_at}")
                print(f"  Elapsed: {entry.elapsed_ms}ms")
        else:
            print("Failed:", res.error)

asyncio.run(main())
