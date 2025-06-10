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

    response1 = sgai_client.smartscraper(
        website_url="https://www.ycombinator.com/companies",
        user_prompt="Extract all the companies and their info",
        infinite_scrolling=True,
        max_pages=10,
    )

    print("\nExample 1 - Basic infinite scrolling:")
    print(f"Request ID: {response1['request_id']}")
    print(f"Result: {response1['result']}")


    # Always close the client when done
    sgai_client.close()

if __name__ == "__main__":
    main()
