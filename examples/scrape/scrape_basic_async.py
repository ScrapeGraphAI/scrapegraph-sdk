from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import AsyncScrapeGraphAI, ScrapeRequest, MarkdownFormatConfig

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.scrape(ScrapeRequest(
            url="https://example.com",
            formats=[MarkdownFormatConfig()],
        ))

        if res.status == "success":
            print("Markdown:", res.data.results.get("markdown", {}).get("data"))
            print(f"\nTook {res.elapsed_ms}ms")
        else:
            print("Failed:", res.error)

asyncio.run(main())
