"""
Example of using the async searchscraper functionality with output schemas for extraction.
"""

import asyncio
from typing import List

from pydantic import BaseModel

from scrapegraph_py import AsyncClient
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")


# Define schemas for extracting structured data
class PythonVersionInfo(BaseModel):
    version: str
    release_date: str
    major_features: List[str]


class PythonComparison(BaseModel):
    key_differences: List[str]
    backward_compatible: bool
    migration_difficulty: str


class GILInfo(BaseModel):
    definition: str
    purpose: str
    limitations: List[str]
    workarounds: List[str]


async def main():
    # Initialize async client
    sgai_client = AsyncClient(api_key="your-api-key-here")

    # Define search queries with their corresponding schemas
    searches = [
        {
            "prompt": "What is the latest version of Python? Include the release date and main features.",
            "schema": PythonVersionInfo,
        },
        {
            "prompt": "Compare Python 2 and Python 3, including backward compatibility and migration difficulty.",
            "schema": PythonComparison,
        },
        {
            "prompt": "Explain Python's GIL, its purpose, limitations, and possible workarounds.",
            "schema": GILInfo,
        },
    ]

    # Create tasks for concurrent execution
    tasks = [
        sgai_client.searchscraper(
            user_prompt=search["prompt"],
            output_schema=search["schema"],
        )
        for search in searches
    ]

    # Execute requests concurrently
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    # Process results
    for i, response in enumerate(responses):
        if isinstance(response, Exception):
            print(f"\nError for search {i+1}: {response}")
        else:
            print(f"\nSearch {i+1}:")
            print(f"Query: {searches[i]['prompt']}")
            # print(f"Raw Result: {response['result']}")

            try:
                # Try to extract structured data using the schema
                result = searches[i]["schema"].model_validate(response["result"])

                # Print extracted structured data
                if isinstance(result, PythonVersionInfo):
                    print("\nExtracted Data:")
                    print(f"Python Version: {result.version}")
                    print(f"Release Date: {result.release_date}")
                    print("Major Features:")
                    for feature in result.major_features:
                        print(f"- {feature}")

                elif isinstance(result, PythonComparison):
                    print("\nExtracted Data:")
                    print("Key Differences:")
                    for diff in result.key_differences:
                        print(f"- {diff}")
                    print(f"Backward Compatible: {result.backward_compatible}")
                    print(f"Migration Difficulty: {result.migration_difficulty}")

                elif isinstance(result, GILInfo):
                    print("\nExtracted Data:")
                    print(f"Definition: {result.definition}")
                    print(f"Purpose: {result.purpose}")
                    print("Limitations:")
                    for limit in result.limitations:
                        print(f"- {limit}")
                    print("Workarounds:")
                    for workaround in result.workarounds:
                        print(f"- {workaround}")
            except Exception as e:
                print(f"\nCould not extract structured data: {e}")

            print("\nReference URLs:")
            for url in response["reference_urls"]:
                print(f"- {url}")

    await sgai_client.close()


if __name__ == "__main__":
    asyncio.run(main())
