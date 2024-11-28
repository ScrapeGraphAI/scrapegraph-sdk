import asyncio

from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import get_logger

get_logger(level="DEBUG")


async def main():

    # Initialize async client
    sgai_client = AsyncClient(api_key="your-api-key-here")

    # Concurrent scraping requests
    urls = [
        "https://scrapegraphai.com/",
        "https://github.com/ScrapeGraphAI/Scrapegraph-ai",
    ]

    tasks = [
        sgai_client.smartscraper(
            website_url=url, user_prompt="Summarize the main content"
        )
        for url in urls
    ]

    # Execute requests concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for i, response in enumerate(responses):
        if isinstance(response, Exception):
            print(f"\nError for {urls[i]}: {response}")
        else:
            print(f"\nPage {i+1} Summary:")
            print(f"URL: {urls[i]}")
            print(f"Result: {response['result']}")

    await sgai_client.close()


if __name__ == "__main__":
    asyncio.run(main())
