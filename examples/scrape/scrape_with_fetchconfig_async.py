from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import AsyncScrapeGraphAI, ScrapeRequest, MarkdownFormatConfig, FetchConfig

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.scrape(ScrapeRequest(
            url="https://example.com",
            formats=[MarkdownFormatConfig()],
            fetch_config=FetchConfig(
                mode="js",
                timeout=45000,
                wait=2000,
                stealth=True,
            ),
        ))

        if res.status == "success":
            print("Markdown:", res.data.results.get("markdown", {}).get("data"))
            print(f"\nTook {res.elapsed_ms}ms")
        else:
            print("Failed:", res.error)

asyncio.run(main())
