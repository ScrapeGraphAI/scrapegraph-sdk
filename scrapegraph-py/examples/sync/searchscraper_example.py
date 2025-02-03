"""
Example of using the searchscraper functionality to search for information.
"""

from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")

# Initialize the client
client = Client(api_key="your-api-key-here")

# Send a searchscraper request
response = client.searchscraper(
    user_prompt="What is the latest version of Python and what are its main features?"
)

# Print the results
print("\nResults:")
print(f"Answer: {response['result']}")
print("\nReference URLs:")
for url in response["reference_urls"]:
    print(f"- {url}")

# Close the client
client.close()
