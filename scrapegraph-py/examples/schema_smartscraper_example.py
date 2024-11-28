from scrapegraph_py import SyncClient
from scrapegraph_py.exceptions import APIError
from pydantic import BaseModel, Field

# Define a Pydantic model for the output schema
class WebpageSchema(BaseModel):
    title: str = Field(description="The title of the webpage")
    description: str = Field(description="The description of the webpage")
    summary: str = Field(description="A brief summary of the webpage")

# Initialize the client
sgai_client = SyncClient(api_key="sgai-your-api-key-here")

try:
    # SmartScraper request with output schema
    response = sgai_client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract webpage information",
        output_schema=WebpageSchema
    )

    # Print the response
    print(f"Request ID: {response['request_id']}")
    print(f"Result: {response['result']}")

    # Check remaining credits
    credits = sgai_client.get_credits()
    print(f"\nCredits Info: {credits}")

    # Submit feedback
    # feedback = sgai_client.submit_feedback(
    #     request_id=response['request_id'],
    #     rating=5,
    #     feedback_text="Great results!"
    # )
    # print(f"\nFeedback Response: {feedback}")

    # Get previous results using get_smartscraper
    # result = sgai_client.get_smartscraper(request_id=response['request_id'])
    # print(f"\nRetrieved Result: {result}")

except APIError as e:
    print(f"API Error: {e}")

finally:
    sgai_client.close()  # Optional cleanup