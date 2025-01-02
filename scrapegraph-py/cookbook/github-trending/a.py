from llama_index.tools.scrapegraph.base import ScrapegraphToolSpec
from pydantic import BaseModel, Field
from typing import List
import os

# Initialize the ScrapegraphToolSpec
scrapegraph_tool = ScrapegraphToolSpec()

# Define the schema for a single repository
class RepositorySchema(BaseModel):
    name: str = Field(description="Name of the repository (e.g., 'owner/repo')")
    description: str = Field(description="Description of the repository")
    stars: int = Field(description="Star count of the repository")
    forks: int = Field(description="Fork count of the repository")
    today_stars: int = Field(description="Stars gained today")
    language: str = Field(description="Programming language used")

# Define the schema for a list of repositories
class ListRepositoriesSchema(BaseModel):
    repositories: List[RepositorySchema] = Field(description="List of GitHub trending repositories")

# Make the API call to scrape GitHub trending repositories
response = scrapegraph_tool.scrapegraph_smartscraper(
    prompt="Extract information about trending GitHub repositories",
    url="https://github.com/trending",
    api_key="sgai-cd497c94-9ac5-4259-b7b5-f3283affe481",
    schema=ListRepositoriesSchema,
)

# Get the result and print each repository
result = response["result"]
print("\nTrending Repositories:")
for repo in result["repositories"]:
    print(f"\nRepository: {repo['name']}")
    print(f"Description: {repo['description']}")
    print(f"Stars: {repo['stars']}")
    print(f"Forks: {repo['forks']}")
    print(f"Today's Stars: {repo['today_stars']}")
    print(f"Language: {repo['language']}")
