from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import AsyncScrapeGraphAI

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.health()

        if res.status == "success":
            print("Status:", res.data.status)
            print("Uptime:", res.data.uptime, "seconds")
            if res.data.services:
                print("Services:")
                print("  Redis:", res.data.services.redis)
                print("  DB:", res.data.services.db)
        else:
            print("Failed:", res.error)

asyncio.run(main())
