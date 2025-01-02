from llama_index.tools.scrapegraph.base import ScrapegraphToolSpec
from pydantic import BaseModel, Field
from typing import List
import os

# Initialize the ScrapegraphToolSpec
scrapegraph_tool = ScrapegraphToolSpec()

# Schema for a single news item
class NewsItemSchema(BaseModel):
    category: str = Field(description="Category of the news (e.g., 'Health', 'Environment')")
    title: str = Field(description="Title of the news article")
    link: str = Field(description="URL to the news article")
    author: str = Field(description="Author of the news article")

# Schema containing a list of news items
class ListNewsSchema(BaseModel):
    news: List[NewsItemSchema] = Field(description="List of news articles with their details")

# Make the API call to scrape news articles
response = scrapegraph_tool.scrapegraph_smartscraper(
    prompt="Extract information about science news articles",
    url="https://www.wired.com/tag/science/",
    api_key="sgai-cd497c94-9ac5-4259-b7b5-f3283affe481",
    schema=ListNewsSchema,
)

# Get the result and print each news article
result = response["result"]
print("\nWired Science News Articles:")
for article in result["news"]:
    print(f"\nCategory: {article['category']}")
    print(f"Title: {article['title']}")
    print(f"Author: {article['author']}")
    print(f"Link: {article['link']}")

# Save to CSV (optional)
import pandas as pd
df = pd.DataFrame(result["news"])
df.to_csv("wired_news.csv", index=False)
print("\nData saved to wired_news.csv")
