"""
Example of using the searchscraper functionality with a custom output schema.
"""

from typing import List

from pydantic import BaseModel

from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")


# Define a custom schema for the output
class PythonVersionInfo(BaseModel):
    version: str
    release_date: str
    major_features: List[str]
    is_latest: bool


# Initialize the client
client = Client(api_key="your-api-key-here")

# Send a searchscraper request with schema
response = client.searchscraper(
    user_prompt="What is the latest version of Python? Include the release date and main features.",
    output_schema=PythonVersionInfo,
)

# The result will be structured according to our schema
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

print("\nReference URLs:")
for url in response["reference_urls"]:
    print(f"- {url}")

# Close the client
client.close()
