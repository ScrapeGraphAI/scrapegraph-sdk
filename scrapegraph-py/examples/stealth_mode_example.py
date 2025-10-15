"""
Stealth Mode Examples for ScrapeGraph AI Python SDK

This file demonstrates how to use stealth mode with various endpoints
to avoid bot detection when scraping websites.

Stealth mode enables advanced techniques to make requests appear more
like those from a real browser, helping to bypass basic bot detection.
"""

import os
from scrapegraph_py import Client
from pydantic import BaseModel, Field

# Get API key from environment variable
API_KEY = os.getenv("SGAI_API_KEY", "your-api-key-here")


# ============================================================================
# EXAMPLE 1: SmartScraper with Stealth Mode
# ============================================================================


def example_smartscraper_with_stealth():
    """
    Extract structured data from a webpage using stealth mode.
    Useful for websites with bot detection.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 1: SmartScraper with Stealth Mode")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.smartscraper(
                website_url="https://www.scrapethissite.com/pages/simple/",
                user_prompt="Extract country names and capitals",
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")
            print(f"Result: {response['result']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 2: SmartScraper with Stealth Mode and Output Schema
# ============================================================================


def example_smartscraper_with_stealth_and_schema():
    """
    Use stealth mode with a structured output schema to extract data
    from websites that might detect bots.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: SmartScraper with Stealth Mode and Schema")
    print("=" * 60)

    # Define output schema using Pydantic
    class Product(BaseModel):
        name: str = Field(description="Product name")
        price: str = Field(description="Product price")
        rating: float = Field(description="Product rating (0-5)")

    with Client(api_key=API_KEY) as client:
        try:
            response = client.smartscraper(
                website_url="https://example.com/products",
                user_prompt="Extract product information including name, price, and rating",
                output_schema=Product,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")
            print(f"Result: {response['result']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 3: SearchScraper with Stealth Mode
# ============================================================================


def example_searchscraper_with_stealth():
    """
    Search and extract information from multiple sources using stealth mode.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: SearchScraper with Stealth Mode")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.searchscraper(
                user_prompt="What are the latest developments in AI technology?",
                num_results=5,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")
            print(f"Result: {response['result']}")
            if "reference_urls" in response:
                print(f"Reference URLs: {response['reference_urls']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 4: Markdownify with Stealth Mode
# ============================================================================


def example_markdownify_with_stealth():
    """
    Convert a webpage to markdown format using stealth mode.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Markdownify with Stealth Mode")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.markdownify(
                website_url="https://www.example.com",
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")
            print(f"Markdown Preview (first 500 chars):")
            print(response["result"][:500])

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 5: Scrape with Stealth Mode
# ============================================================================


def example_scrape_with_stealth():
    """
    Get raw HTML from a webpage using stealth mode.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Scrape with Stealth Mode")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.scrape(
                website_url="https://www.example.com",
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Scrape Request ID: {response['scrape_request_id']}")
            print(f"HTML Preview (first 500 chars):")
            print(response["html"][:500])

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 6: Scrape with Stealth Mode and Heavy JS Rendering
# ============================================================================


def example_scrape_with_stealth_and_js():
    """
    Scrape a JavaScript-heavy website using stealth mode.
    Combines JavaScript rendering with stealth techniques.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Scrape with Stealth Mode and Heavy JS")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.scrape(
                website_url="https://www.example.com",
                render_heavy_js=True,  # Enable JavaScript rendering
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Scrape Request ID: {response['scrape_request_id']}")
            print(f"HTML Preview (first 500 chars):")
            print(response["html"][:500])

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 7: Agentic Scraper with Stealth Mode
# ============================================================================


def example_agenticscraper_with_stealth():
    """
    Perform automated browser actions using stealth mode.
    Ideal for interacting with protected forms or multi-step workflows.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Agentic Scraper with Stealth Mode")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.agenticscraper(
                url="https://dashboard.example.com/login",
                steps=[
                    "Type user@example.com in email input box",
                    "Type password123 in password input box",
                    "Click on login button",
                ],
                use_session=True,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 8: Agentic Scraper with Stealth Mode and AI Extraction
# ============================================================================


def example_agenticscraper_with_stealth_and_ai():
    """
    Combine stealth mode with AI extraction in agentic scraping.
    Performs actions and then extracts structured data.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Agentic Scraper with Stealth and AI Extraction")
    print("=" * 60)

    with Client(api_key=API_KEY) as client:
        try:
            response = client.agenticscraper(
                url="https://dashboard.example.com",
                steps=[
                    "Navigate to user profile section",
                    "Click on settings tab",
                ],
                use_session=True,
                user_prompt="Extract user profile information and settings",
                ai_extraction=True,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 9: Crawl with Stealth Mode
# ============================================================================


def example_crawl_with_stealth():
    """
    Crawl an entire website using stealth mode.
    Useful for comprehensive data extraction from protected sites.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 9: Crawl with Stealth Mode")
    print("=" * 60)

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Website Content",
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Page title"},
            "content": {"type": "string", "description": "Main content"},
        },
        "required": ["title"],
    }

    with Client(api_key=API_KEY) as client:
        try:
            response = client.crawl(
                url="https://www.example.com",
                prompt="Extract page titles and main content",
                data_schema=schema,
                depth=2,
                max_pages=5,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Crawl ID: {response['id']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 10: Crawl with Stealth Mode and Sitemap
# ============================================================================


def example_crawl_with_stealth_and_sitemap():
    """
    Use sitemap for efficient crawling with stealth mode enabled.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 10: Crawl with Stealth Mode and Sitemap")
    print("=" * 60)

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Product Information",
        "type": "object",
        "properties": {
            "product_name": {"type": "string"},
            "price": {"type": "string"},
            "description": {"type": "string"},
        },
        "required": ["product_name"],
    }

    with Client(api_key=API_KEY) as client:
        try:
            response = client.crawl(
                url="https://www.example-shop.com",
                prompt="Extract product information from all pages",
                data_schema=schema,
                sitemap=True,  # Use sitemap for better page discovery
                depth=3,
                max_pages=10,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Crawl ID: {response['id']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 11: SmartScraper with Stealth, Custom Headers, and Pagination
# ============================================================================


def example_smartscraper_advanced_stealth():
    """
    Advanced example combining stealth mode with custom headers and pagination.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 11: SmartScraper Advanced with Stealth")
    print("=" * 60)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    with Client(api_key=API_KEY) as client:
        try:
            response = client.smartscraper(
                website_url="https://www.example-marketplace.com/products",
                user_prompt="Extract all product listings from multiple pages",
                headers=headers,
                number_of_scrolls=10,
                total_pages=5,
                render_heavy_js=True,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")
            print(f"Result: {response['result']}")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# EXAMPLE 12: Using Stealth Mode with Custom Headers
# ============================================================================


def example_stealth_with_custom_headers():
    """
    Demonstrate using stealth mode together with custom headers
    for maximum control over request appearance.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 12: Stealth Mode with Custom Headers")
    print("=" * 60)

    # Custom headers to simulate a real browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
    }

    with Client(api_key=API_KEY) as client:
        try:
            # Using with markdownify
            response = client.markdownify(
                website_url="https://www.protected-site.com",
                headers=headers,
                stealth=True,  # Enable stealth mode
            )

            print(f"Status: {response['status']}")
            print(f"Request ID: {response['request_id']}")
            print(f"Success! Stealth mode + custom headers bypassed detection.")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================================
# RUN ALL EXAMPLES
# ============================================================================


def run_all_examples():
    """Run all stealth mode examples"""
    print("\n")
    print("=" * 60)
    print("STEALTH MODE EXAMPLES FOR SCRAPEGRAPH AI PYTHON SDK")
    print("=" * 60)
    print("\nThese examples demonstrate how to use stealth mode")
    print("to avoid bot detection when scraping websites.")
    print("\nStealth mode is available for all major endpoints:")
    print("- SmartScraper")
    print("- SearchScraper")
    print("- Markdownify")
    print("- Scrape")
    print("- Agentic Scraper")
    print("- Crawl")

    examples = [
        example_smartscraper_with_stealth,
        example_smartscraper_with_stealth_and_schema,
        example_searchscraper_with_stealth,
        example_markdownify_with_stealth,
        example_scrape_with_stealth,
        example_scrape_with_stealth_and_js,
        example_agenticscraper_with_stealth,
        example_agenticscraper_with_stealth_and_ai,
        example_crawl_with_stealth,
        example_crawl_with_stealth_and_sitemap,
        example_smartscraper_advanced_stealth,
        example_stealth_with_custom_headers,
    ]

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\nExample {i} failed: {e}")

    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    # You can run all examples or specific ones
    run_all_examples()

    # Or run individual examples:
    # example_smartscraper_with_stealth()
    # example_searchscraper_with_stealth()
    # example_crawl_with_stealth()
