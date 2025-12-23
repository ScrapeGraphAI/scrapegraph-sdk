"""
Example of using the crawl endpoint with path filtering.

This example demonstrates how to use include_paths and exclude_paths
to control which pages are crawled on a website.
"""
import os
from scrapegraph_py import Client
from pydantic import BaseModel, Field


# Define your output schema
class ProductInfo(BaseModel):
    name: str = Field(description="Product name")
    price: str = Field(description="Product price")
    description: str = Field(description="Product description")


class CrawlResult(BaseModel):
    products: list[ProductInfo] = Field(description="List of products found")
    total_products: int = Field(description="Total number of products")


def main():
    # Initialize the client
    sgai_api_key = os.getenv("SGAI_API_KEY")
    client = Client(api_key=sgai_api_key)

    print("🔍 Starting crawl with path filtering...")
    print("=" * 50)

    # Example 1: Include only specific paths
    print("\n📝 Example 1: Crawl only /products/* pages")
    print("-" * 50)

    result = client.crawl(
        url="https://example.com",
        prompt="Extract product information including name, price, and description",
        data_schema=CrawlResult.model_json_schema(),
        extraction_mode=True,
        depth=2,
        max_pages=10,
        include_paths=["/products/*", "/items/*"],  # Only crawl product pages
        exclude_paths=["/products/archived/*"]       # But skip archived products
    )

    print(f"Task ID: {result.get('task_id')}")
    print("\n✅ Crawl job started successfully!")

    # Example 2: Exclude admin and API paths
    print("\n📝 Example 2: Crawl all pages except admin and API")
    print("-" * 50)

    result = client.crawl(
        url="https://example.com",
        prompt="Extract all relevant information",
        data_schema=CrawlResult.model_json_schema(),
        extraction_mode=True,
        depth=2,
        max_pages=20,
        exclude_paths=[
            "/admin/*",      # Skip all admin pages
            "/api/*",        # Skip all API endpoints
            "/private/*",    # Skip private pages
            "/*.json"        # Skip JSON files
        ]
    )

    print(f"Task ID: {result.get('task_id')}")
    print("\n✅ Crawl job started successfully!")

    # Example 3: Complex filtering with wildcards
    print("\n📝 Example 3: Complex path filtering with wildcards")
    print("-" * 50)

    result = client.crawl(
        url="https://example.com",
        prompt="Extract blog content and metadata",
        data_schema=CrawlResult.model_json_schema(),
        extraction_mode=True,
        depth=3,
        max_pages=15,
        include_paths=[
            "/blog/**",           # Include all blog pages (any depth)
            "/articles/*",        # Include top-level articles
            "/news/2024/*"        # Include 2024 news only
        ],
        exclude_paths=[
            "/blog/draft/*",      # Skip draft blog posts
            "/blog/*/comments"    # Skip comment pages
        ]
    )

    print(f"Task ID: {result.get('task_id')}")
    print("\n✅ Crawl job started successfully!")

    print("\n" + "=" * 50)
    print("📚 Path Filtering Guide:")
    print("=" * 50)
    print("• Use '/*' to match a single path segment")
    print("  Example: '/products/*' matches '/products/item1' but not '/products/cat/item1'")
    print("\n• Use '/**' to match any number of path segments")
    print("  Example: '/blog/**' matches '/blog/2024/post' and '/blog/category/2024/post'")
    print("\n• exclude_paths takes precedence over include_paths")
    print("  You can include a broad pattern and exclude specific subsets")
    print("\n• Paths must start with '/'")
    print("  Example: '/products/*' is valid, 'products/*' is not")


if __name__ == "__main__":
    main()
