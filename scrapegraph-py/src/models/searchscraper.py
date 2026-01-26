"""
Pydantic models for the SearchScraper API endpoint.

This module defines request and response models for the SearchScraper endpoint,
which performs AI-powered web research by searching, scraping, and synthesizing
information from multiple sources.

The SearchScraper:
- Searches the web for relevant pages based on a query
- Scrapes multiple websites (3-20 configurable)
- Extracts and synthesizes information using AI
- Supports both AI extraction and markdown conversion modes
"""

from typing import Optional, Type
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class SearchScraperRequest(BaseModel):
    """
    Request model for the SearchScraper endpoint.

    This model validates and structures requests for web research and scraping
    across multiple search results.

    Attributes:
        user_prompt: The search query/prompt
        num_results: Number of websites to scrape (3-20, default 3)
        headers: Optional HTTP headers
        output_schema: Optional Pydantic model for structured extraction
        extraction_mode: Use AI extraction (True) or markdown (False)
        mock: Whether to use mock mode for testing
        render_heavy_js: Whether to render heavy JavaScript

    Example:
        >>> request = SearchScraperRequest(
        ...     user_prompt="What is the latest version of Python?",
        ...     num_results=5,
        ...     extraction_mode=True
        ... )
    """
    user_prompt: str = Field(..., example="What is the latest version of Python?")
    num_results: Optional[int] = Field(
        default=3,
        ge=3,
        le=20,
        example=5,
        description="Number of websites to scrape (3-20). Default is 3. More "
        "websites provide better research depth but cost more credits.",
    )
    headers: Optional[dict[str, str]] = Field(
        None,
        example={
            "User-Agent": "scrapegraph-py",
            "Cookie": "cookie1=value1; cookie2=value2",
        },
        description="Optional headers to send with the request, including cookies "
        "and user agent",
    )
    output_schema: Optional[Type[BaseModel]] = None
    extraction_mode: bool = Field(
        default=True,
        description="Whether to use AI extraction (True) or markdown conversion (False). "
        "AI extraction costs 10 credits per page, markdown conversion costs 2 credits per page.",
    )
    mock: bool = Field(default=False, description="Whether to use mock mode for the request")
    render_heavy_js: bool = Field(default=False, description="Whether to render heavy JavaScript on the page")
    stealth: bool = Field(default=False, description="Enable stealth mode to avoid bot detection")

    @model_validator(mode="after")
    def validate_user_prompt(self) -> "SearchScraperRequest":
        if self.user_prompt is None or not self.user_prompt.strip():
            raise ValueError("User prompt cannot be empty")
        if not any(c.isalnum() for c in self.user_prompt):
            raise ValueError("User prompt must contain a valid prompt")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        # Set exclude_none=True to exclude None values from serialization
        kwargs.setdefault("exclude_none", True)
        data = super().model_dump(*args, **kwargs)
        # Convert the Pydantic model schema to dict if present
        if self.output_schema is not None:
            data["output_schema"] = self.output_schema.model_json_schema()
        return data


class GetSearchScraperRequest(BaseModel):
    """Request model for get_searchscraper endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetSearchScraperRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self
