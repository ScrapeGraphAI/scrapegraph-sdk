from dotenv import load_dotenv
load_dotenv()

import asyncio
from scrapegraph_py import (
    AsyncScrapeGraphAI,
    CrawlRequest,
    MarkdownFormatConfig,
    LinksFormatConfig,
)

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        start_res = await sgai.crawl.start(CrawlRequest(
            url="https://scrapegraphai.com/",
            max_pages=3,
            max_depth=1,
            formats=[
                MarkdownFormatConfig(),
                LinksFormatConfig(),
            ],
        ))

        if start_res.status != "success" or not start_res.data:
            print("Failed to start:", start_res.error)
        else:
            crawl_id = start_res.data.id
            print("Crawl started:", crawl_id)

            status = start_res.data.status
            while status == "running":
                await asyncio.sleep(2)
                get_res = await sgai.crawl.get(crawl_id)
                if get_res.status != "success" or not get_res.data:
                    print("Failed to get status:", get_res.error)
                    break
                status = get_res.data.status
                print(f"Progress: {get_res.data.finished}/{get_res.data.total} - {status}")

                if status in ("completed", "failed"):
                    print("\nPages crawled:")
                    for page in get_res.data.pages:
                        print(f"\n  Page: {page.url}")
                        print(f"  Status: {page.status}")
                        print(f"  Depth: {page.depth}")

asyncio.run(main())
