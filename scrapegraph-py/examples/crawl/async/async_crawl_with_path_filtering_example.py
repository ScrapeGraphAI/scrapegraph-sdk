"""
Example of using the async crawl endpoint with path filtering.

This example demonstrates how to use include_paths and exclude_paths
to control which pages are crawled on a website (async version).
"""
import asyncio
import os
from scrapegraph_py import AsyncClient
from pydantic import BaseModel, Field


# Define your output schema
class ProductInfo(BaseModel):
    name: str = Field(description="Product name")
    price: str = Field(description="Product price")
    category: str = Field(description="Product category")


class CrawlResult(BaseModel):
    products: list[ProductInfo] = Field(description="List of products found")
    categories: list[str] = Field(description="List of product categories")


async def main():
    # Initialize the async client
    sgai_api_key = os.getenv("SGAI_API_KEY")

    async with AsyncClient(api_key=sgai_api_key) as client:
        print("🔍 Starting async crawl with path filtering...")
        print("=" * 50)

        # Example: Crawl only product pages, excluding certain sections
        print("\n📝 Crawling e-commerce site with smart path filtering")
        print("-" * 50)

        result = await client.crawl(
            url="https://example-shop.com",
            prompt="Extract all products with their names, prices, and categories",
            data_schema=CrawlResult.model_json_schema(),
            extraction_mode=True,
            depth=3,
            max_pages=50,
            sitemap=True,  # Use sitemap for better coverage
            include_paths=[
                "/products/**",          # Include all product pages
                "/categories/*",         # Include category listings
                "/collections/*"         # Include collection pages
            ],
            exclude_paths=[
                "/products/out-of-stock/*",  # Skip out-of-stock items
                "/products/*/reviews",       # Skip review pages
                "/admin/**",                 # Skip admin pages
                "/api/**",                   # Skip API endpoints
                "/*.pdf"                     # Skip PDF files
            ]
        )

        print(f"Task ID: {result.get('task_id')}")
        print("\n✅ Async crawl job started successfully!")

        # You can then poll for results using get_crawl
        task_id = result.get('task_id')
        if task_id:
            print(f"\n⏳ Polling for results (task: {task_id})...")

            # Poll every 5 seconds until complete
            max_attempts = 60  # 5 minutes max
            for attempt in range(max_attempts):
                await asyncio.sleep(5)
                status = await client.get_crawl(task_id)

                state = status.get('state', 'UNKNOWN')
                print(f"Attempt {attempt + 1}: Status = {state}")

                if state == 'SUCCESS':
                    print("\n✨ Crawl completed successfully!")
                    result_data = status.get('result', {})
                    print(f"Found {len(result_data.get('products', []))} products")
                    break
                elif state in ['FAILURE', 'REVOKED']:
                    print(f"\n❌ Crawl failed with status: {state}")
                    break
            else:
                print("\n⏰ Timeout: Crawl took too long")

        print("\n" + "=" * 50)
        print("💡 Tips for effective path filtering:")
        print("=" * 50)
        print("• Combine with sitemap=True for better page discovery")
        print("• Use include_paths to focus on content-rich sections")
        print("• Use exclude_paths to skip pages with duplicate content")
        print("• Test your patterns on a small max_pages first")
        print("• Remember: exclude_paths overrides include_paths")


if __name__ == "__main__":
    asyncio.run(main())
