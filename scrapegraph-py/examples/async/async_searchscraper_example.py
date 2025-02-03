"""
Example of using the async searchscraper functionality to search for information concurrently.
"""

import asyncio

from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")


async def main():
    # Initialize async client
    sgai_client = AsyncClient(api_key="your-api-key-here")

    # List of search queries
    queries = [
        "What is the latest version of Python and what are its main features?",
        "What are the key differences between Python 2 and Python 3?",
        "What is Python's GIL and how does it work?",
    ]

    # Create tasks for concurrent execution
    tasks = [sgai_client.searchscraper(user_prompt=query) for query in queries]

    # Execute requests concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for i, response in enumerate(responses):
        if isinstance(response, Exception):
            print(f"\nError for query {i+1}: {response}")
        else:
            print(f"\nSearch {i+1}:")
            print(f"Query: {queries[i]}")
            print(f"Result: {response['result']}")
            print("Reference URLs:")
            for url in response["reference_urls"]:
                print(f"- {url}")

    await sgai_client.close()


if __name__ == "__main__":
    asyncio.run(main())
