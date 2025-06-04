"""
Example of using SmartScraper with infinite scrolling in asynchronous mode.
This example demonstrates how to scrape content from multiple webpages concurrently using infinite scrolling.
"""

import asyncio
from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import sgai_logger

# Set up logging
sgai_logger.set_logging(level="INFO")

async def scrape_with_infinite_scroll(client: AsyncClient, url: str, prompt: str, max_pages: int = 10):
    """Helper function to perform a single scraping task with infinite scrolling"""
    response = await client.smartscraper(
        website_url=url,
        user_prompt=prompt,
        infinite_scrolling=True,
        max_pages=max_pages
    )
    return response

async def main():
    # Initialize the async client with your API key
    async with AsyncClient(api_key="your-api-key-here") as sgai_client:
        # Example 1: Scrape multiple pages concurrently
        tasks = [
            scrape_with_infinite_scroll(
                sgai_client,
                "https://example.com/products",
                "Extract all product names and prices",
                max_pages=20
            ),
            scrape_with_infinite_scroll(
                sgai_client,
                "https://example.com/articles",
                "Extract all article titles and authors",
                max_pages=15
            ),
            scrape_with_infinite_scroll(
                sgai_client,
                "https://example.com/news",
                "Extract all news headlines and dates",
                max_pages=10
            )
        ]

        # Wait for all scraping tasks to complete
        results = await asyncio.gather(*tasks)

        # Process and print results
        for i, result in enumerate(results, 1):
            print(f"\nExample {i} Results:")
            print(f"Request ID: {result['request_id']}")
            print(f"Result: {result['result']}")

        # Example 2: Single page without infinite scrolling
        response = await sgai_client.smartscraper(
            website_url="https://example.com/static-page",
            user_prompt="Extract the main heading and first paragraph",
            infinite_scrolling=False
        )
        print("\nExample 4 - Without infinite scrolling:")
        print(f"Request ID: {response['request_id']}")
        print(f"Result: {response['result']}")

if __name__ == "__main__":
    asyncio.run(main()) 