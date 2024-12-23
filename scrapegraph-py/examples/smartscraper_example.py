from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

# Set logging to DEBUG level to see all logs
sgai_logger.set_logging(level="DEBUG")

# Initialize the client with explicit API key
sgai_client = Client(api_key="your_api_key")

# SmartScraper request
response = sgai_client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the main heading, description, and summary of the webpage",
)

# Print the response
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

sgai_client.close()
