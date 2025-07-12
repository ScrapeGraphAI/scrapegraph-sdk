# Models for crawl endpoint

from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field, model_validator, conint


class CrawlRequest(BaseModel):
    url: str = Field(
        ...,
        example="https://scrapegraphai.com/",
        description="The starting URL for the crawl"
    )
    prompt: str = Field(
        ...,
        example="What does the company do? and I need text content from there privacy and terms",
        description="The prompt to guide the crawl and extraction"
    )
    data_schema: Dict[str, Any] = Field(
        ...,
        description="JSON schema defining the structure of the extracted data"
    )
    cache_website: bool = Field(
        default=True,
        description="Whether to cache the website content"
    )
    depth: conint(ge=1, le=10) = Field(
        default=2,
        description="Maximum depth of the crawl (1-10)"
    )
    max_pages: conint(ge=1, le=100) = Field(
        default=2,
        description="Maximum number of pages to crawl (1-100)"
    )
    same_domain_only: bool = Field(
        default=True,
        description="Whether to only crawl pages from the same domain"
    )
    batch_size: conint(ge=1, le=10) = Field(
        default=1,
        description="Batch size for processing pages (1-10)"
    )

    @model_validator(mode="after")
    def validate_url(self) -> "CrawlRequest":
        if not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (
            self.url.startswith("http://")
            or self.url.startswith("https://")
        ):
            raise ValueError("Invalid URL - must start with http:// or https://")
        return self

    @model_validator(mode="after")
    def validate_prompt(self) -> "CrawlRequest":
        if not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if not any(c.isalnum() for c in self.prompt):
            raise ValueError("Prompt must contain valid content")
        return self

    @model_validator(mode="after")
    def validate_data_schema(self) -> "CrawlRequest":
        if not isinstance(self.data_schema, dict):
            raise ValueError("Data schema must be a dictionary")
        if not self.data_schema:
            raise ValueError("Data schema cannot be empty")
        return self


class GetCrawlRequest(BaseModel):
    """Request model for get_crawl endpoint"""

    crawl_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_crawl_id(self) -> "GetCrawlRequest":
        try:
            # Validate the crawl_id is a valid UUID
            UUID(self.crawl_id)
        except ValueError:
            raise ValueError("crawl_id must be a valid UUID")
        return self 