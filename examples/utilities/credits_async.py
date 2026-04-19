from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import AsyncScrapeGraphAI

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.credits()

        if res.status == "success":
            print("Plan:", res.data.plan)
            print("Remaining credits:", res.data.remaining)
            print("Used credits:", res.data.used)
            print("\nJob limits:")
            print("  Crawl:", res.data.jobs.crawl.used, "/", res.data.jobs.crawl.limit)
            print("  Monitor:", res.data.jobs.monitor.used, "/", res.data.jobs.monitor.limit)
        else:
            print("Failed:", res.error)

asyncio.run(main())
