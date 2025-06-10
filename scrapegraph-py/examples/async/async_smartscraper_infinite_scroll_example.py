import asyncio
from typing import List
from pydantic import BaseModel

from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")

# Define the output schema
class Company(BaseModel):
    name: str
    category: str
    location: str

class CompaniesResponse(BaseModel):
    companies: List[Company]

async def scrape_companies(client: AsyncClient, url: str, batch: str) -> None:
    """Scrape companies from a specific YC batch with infinite scroll."""
    try:
        response = await client.smartscraper(
            website_url=f"{url}?batch={batch}",
            user_prompt="Extract all company names and their categories from the page",
            output_schema=CompaniesResponse,
            number_of_scrolls=10  # Scroll 10 times to load more companies
        )

        # Parse and print the results
        result = CompaniesResponse.model_validate(response['result'])
        print(f"\nCompanies from {batch} batch:")
        print("=" * 80)
        for company in result.companies:
            print(f"Name: {company.name}")
            print(f"Category: {company.category}")
            print(f"Location: {company.location}")
            print("-" * 80)

    except Exception as e:
        print(f"Error scraping {batch} batch: {e}")

async def main():
    # Initialize async client
    sgai_client = AsyncClient(api_key="your-api-key-here")

    try:
        # Define batches to scrape
        base_url = "https://www.ycombinator.com/companies"
        batches = [
            "Spring%202025",
            "Winter%202025",
            "Summer%202024"
        ]

        # Create tasks for each batch
        tasks = [
            scrape_companies(sgai_client, base_url, batch)
            for batch in batches
        ]

        # Execute all scraping tasks concurrently
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await sgai_client.close()

if __name__ == "__main__":
    asyncio.run(main()) 