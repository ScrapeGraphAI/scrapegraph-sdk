"""
Pydantic models for the Scrape API endpoint.

This module defines request and response models for the basic Scrape endpoint,
which retrieves raw HTML content from websites.

The Scrape endpoint is useful for:
- Getting clean HTML content from websites
- Handling JavaScript-heavy sites
- Preprocessing before AI extraction
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ScrapeRequest(BaseModel):
    """
    Request model for the Scrape endpoint.

    This model validates and structures requests for basic HTML scraping
    without AI extraction.

    Attributes:
        website_url: URL of the website to scrape
        render_heavy_js: Whether to render heavy JavaScript (default: False)
        headers: Optional HTTP headers including cookies
        mock: Whether to use mock mode for testing

    Example:
        >>> request = ScrapeRequest(
        ...     website_url="https://example.com",
        ...     render_heavy_js=True
        ... )
    """
    website_url: str = Field(..., example="https://scrapegraphai.com/")
    render_heavy_js: bool = Field(
        False,
        description="Whether to render heavy JavaScript (defaults to False)",
    )
    headers: Optional[dict[str, str]] = Field(
        None,
        example={
            "User-Agent": "scrapegraph-py",
            "Cookie": "cookie1=value1; cookie2=value2",
        },
        description="Optional headers to send with the request, including cookies "
        "and user agent",
    ),
    mock: bool = Field(default=False, description="Whether to use mock mode for the request")
    stealth: bool = Field(default=False, description="Enable stealth mode to avoid bot detection")

    @model_validator(mode="after")
    def validate_url(self) -> "ScrapeRequest":
        if self.website_url is None or not self.website_url.strip():
            raise ValueError("Website URL cannot be empty")
        if not (
            self.website_url.startswith("http://")
            or self.website_url.startswith("https://")
        ):
            raise ValueError("Invalid URL")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        # Set exclude_none=True to exclude None values from serialization
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class GetScrapeRequest(BaseModel):
    """Request model for get_scrape endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetScrapeRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self
