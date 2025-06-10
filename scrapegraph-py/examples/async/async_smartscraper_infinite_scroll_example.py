import asyncio
from typing import List, Dict, Any

from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")


async def scrape_companies(client: AsyncClient, url: str, batch: str) -> None:
    """Scrape companies from a specific YC batch with infinite scroll."""
    try:
        # Initial scrape with infinite scroll enabled
        response = await client.smartscraper(
            website_url=url,
            user_prompt="Extract all company information from this page, including name, description, and website",
            infinite_scroll=True,
            scroll_options={
                "max_scrolls": 10,  # Adjust based on page size
                "scroll_delay": 2,  # Seconds between scrolls
                "scroll_to_bottom": True
            }
        )
        
        # Process the results
        companies = response.get("result", [])
        if not companies:
            print(f"No companies found for batch {batch}")
            return
            
        # Save or process the companies data
        print(f"Found {len(companies)} companies in batch {batch}")
        for company in companies:
            print(f"Company: {company.get('name', 'N/A')}")
            print(f"Description: {company.get('description', 'N/A')}")
            print(f"Website: {company.get('website', 'N/A')}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error scraping batch {batch}: {str(e)}")


async def main():
    # Initialize async client
    client = AsyncClient(api_key="your-api-key-here")
    
    try:
        # Example YC batch URLs
        batch_urls = {
            "W24": "https://www.ycombinator.com/companies?batch=W24",
            "S23": "https://www.ycombinator.com/companies?batch=S23"
        }
        
        # Create tasks for each batch
        tasks = [
            scrape_companies(client, url, batch)
            for batch, url in batch_urls.items()
        ]
        
        # Execute all batch scraping concurrently
        await asyncio.gather(*tasks)
        
    finally:
        # Ensure client is properly closed
        await client.close()


if __name__ == "__main__":
    asyncio.run(main()) 