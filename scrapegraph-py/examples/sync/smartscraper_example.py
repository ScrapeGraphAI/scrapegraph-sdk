from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")

# Initialize the client with explicit API key
sgai_client = Client(api_key="your-api-key-here")

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
