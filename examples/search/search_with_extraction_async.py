from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from scrapegraph_py import AsyncScrapeGraphAI, SearchRequest

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.search(SearchRequest(
            query="best programming languages 2024",
            num_results=3,
            prompt="Summarize the top programming languages mentioned and why they are recommended",
            schema={
                "type": "object",
                "properties": {
                    "languages": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "reason": {"type": "string"},
                            },
                        },
                    },
                },
            },
        ))

        if res.status == "success":
            print("=== Search Results ===")
            for result in res.data.results:
                print(f"\n{result.title}")
                print(f"URL: {result.url}")

            print("\n=== Extracted Summary ===")
            print(json.dumps(res.data.json_data, indent=2))
        else:
            print("Failed:", res.error)

asyncio.run(main())
