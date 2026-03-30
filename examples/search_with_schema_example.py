"""
Search the web with a Pydantic output schema.

Combine web search with structured extraction to get exactly
the data format you need.
"""

import json
from typing import List

from pydantic import BaseModel, Field

from scrapegraph_py import Client


class SearchResult(BaseModel):
    title: str = Field(description="Result title")
    url: str = Field(description="Result URL")
    summary: str = Field(description="Brief summary of the content")


class SearchResults(BaseModel):
    results: List[SearchResult] = Field(description="List of search results")


client = Client()  # uses SGAI_API_KEY env var

result = client.search(
    query="latest AI news",
    num_results=5,
    output_schema=SearchResults,
)
print(json.dumps(result, indent=2))

client.close()
