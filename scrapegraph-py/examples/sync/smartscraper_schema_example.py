from pydantic import BaseModel, Field

from scrapegraph_py import Client


# Define a Pydantic model for the output schema
class WebpageSchema(BaseModel):
    title: str = Field(description="The title of the webpage")
    description: str = Field(description="The description of the webpage")
    summary: str = Field(description="A brief summary of the webpage")


# Initialize the client
sgai_client = Client(api_key="your-api-key-here")

# SmartScraper request with output schema
response = sgai_client.smartscraper(
    website_url="https://example.com",
    # website_html="...", # Optional, if you want to pass in HTML content instead of a URL
    user_prompt="Extract webpage information",
    output_schema=WebpageSchema,
)

# Print the response
print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

sgai_client.close()
