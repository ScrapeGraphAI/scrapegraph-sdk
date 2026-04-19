from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import AsyncScrapeGraphAI, SearchRequest

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.search(SearchRequest(
            query="best programming languages 2024",
            num_results=3,
        ))

        if res.status == "success":
            for result in res.data.results:
                print(f"\n{result.title}")
                print(f"URL: {result.url}")
                print(f"Content: {result.content[:200]}...")
        else:
            print("Failed:", res.error)

asyncio.run(main())
