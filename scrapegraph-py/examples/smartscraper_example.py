from scrapegraph_py import SyncClient
from scrapegraph_py.logger import get_logger

get_logger(level="DEBUG")

# Initialize the client
sgai_client = SyncClient(api_key="your-api-key-here")

# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the main heading, description, and summary of the webpage",
)

# Print the response
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

sgai_client.close()
