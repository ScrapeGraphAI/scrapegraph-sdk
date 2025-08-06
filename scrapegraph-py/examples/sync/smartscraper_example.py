import os

from dotenv import load_dotenv

from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

# Load environment variables from .env file
load_dotenv()

sgai_logger.set_logging(level="INFO")

# Initialize the client with API key from environment variable
api_key = os.getenv("SGAI_API_KEY")
if not api_key:
    print("❌ Error: SGAI_API_KEY environment variable not set")
    print("Please either:")
    print("  1. Set environment variable: export SGAI_API_KEY='your-api-key-here'")
    print("  2. Create a .env file with: SGAI_API_KEY=your-api-key-here")
    exit(1)

sgai_client = Client(api_key=api_key)

# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://example.com",
    # website_html="...", # Optional, if you want to pass in HTML content instead of a URL
    user_prompt="Extract the main heading, description, and summary of the webpage",
)


# Print the response
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

sgai_client.close()
