import asyncio
import os

from dotenv import load_dotenv

from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import sgai_logger

# Load environment variables from .env file
load_dotenv()

sgai_logger.set_logging(level="INFO")


async def main():
    # Initialize async client with API key from environment variable
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        print("Please either:")
        print("  1. Set environment variable: export SGAI_API_KEY='your-api-key-here'")
        print("  2. Create a .env file with: SGAI_API_KEY=your-api-key-here")
        return

    sgai_client = AsyncClient(api_key=api_key)

    # AgenticScraper request - automated login example
    response = await sgai_client.agenticscraper(
        url="https://dashboard.scrapegraphai.com/",
        use_session=True,
        steps=[
            "Type email@gmail.com in email input box",
            "Type test-password@123 in password inputbox", 
            "click on login"
        ]
    )

    # Print the response
    print(f"Request ID: {response['request_id']}")
    print(f"Result: {response['result']}")

    await sgai_client.close()


if __name__ == "__main__":
    asyncio.run(main())
