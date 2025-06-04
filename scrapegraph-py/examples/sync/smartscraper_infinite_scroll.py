"""
Example of using SmartScraper with infinite scrolling in synchronous mode.
This example demonstrates how to scrape content from a webpage that requires scrolling to load more content.
"""

from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger
import time

# Set up logging
sgai_logger.set_logging(level="INFO")

def main():
    # Initialize the client with your API key
    sgai_client = Client(api_key="your-api-key-here")

    try:
        # Example 1: Basic infinite scrolling with default settings
        response1 = sgai_client.smartscraper(
            website_url="https://example.com/infinite-scroll",
            user_prompt="Extract all product names and prices from the page",
            infinite_scrolling=True  # Uses default max_pages=10
        )
        print("\nExample 1 - Basic infinite scrolling:")
        print(f"Request ID: {response1['request_id']}")
        print(f"Result: {response1['result']}")

        # Example 2: Custom infinite scrolling with specific max pages
        response2 = sgai_client.smartscraper(
            website_url="https://example.com/long-list",
            user_prompt="Extract all article titles and their publication dates",
            infinite_scrolling=True,
            max_pages=50  # Custom maximum number of pages to scroll
        )
        print("\nExample 2 - Custom max pages:")
        print(f"Request ID: {response2['request_id']}")
        print(f"Result: {response2['result']}")

        # Example 3: Without infinite scrolling (for comparison)
        response3 = sgai_client.smartscraper(
            website_url="https://example.com/static-page",
            user_prompt="Extract the main heading and first paragraph",
            infinite_scrolling=False
        )
        print("\nExample 3 - Without infinite scrolling:")
        print(f"Request ID: {response3['request_id']}")
        print(f"Result: {response3['result']}")

    finally:
        # Always close the client when done
        sgai_client.close()

if __name__ == "__main__":
    main() 