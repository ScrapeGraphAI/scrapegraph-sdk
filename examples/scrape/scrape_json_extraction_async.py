from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from scrapegraph_py import AsyncScrapeGraphAI, ScrapeRequest, JsonFormatConfig

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        res = await sgai.scrape(ScrapeRequest(
            url="https://example.com",
            formats=[
                JsonFormatConfig(
                    prompt="Extract the company name, tagline, and list of features",
                    schema={
                        "type": "object",
                        "properties": {
                            "companyName": {"type": "string"},
                            "tagline": {"type": "string"},
                            "features": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["companyName"],
                    },
                ),
            ],
        ))

        if res.status == "success":
            json_result = res.data.results.get("json", {})

            print("=== JSON Extraction ===\n")
            print("Extracted data:")
            print(json.dumps(json_result.get("data"), indent=2))

            chunker = json_result.get("metadata", {}).get("chunker")
            if chunker:
                chunks = chunker.get("chunks", [])
                print("\nChunker info:")
                print("  Chunks:", len(chunks))
                print("  Total size:", sum(c.get("size", 0) for c in chunks), "chars")
        else:
            print("Failed:", res.error)

asyncio.run(main())
