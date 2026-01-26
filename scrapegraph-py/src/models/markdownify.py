"""
Pydantic models for the Markdownify API endpoint.

This module defines request and response models for the Markdownify endpoint,
which converts web pages into clean markdown format.

The Markdownify endpoint is useful for:
- Converting HTML to markdown for easier processing
- Extracting clean text content from websites
- Preparing content for LLM consumption
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class MarkdownifyRequest(BaseModel):
    """
    Request model for the Markdownify endpoint.

    This model validates and structures requests for converting web pages
    to markdown format.

    Attributes:
        website_url: URL of the website to convert to markdown
        headers: Optional HTTP headers including cookies
        mock: Whether to use mock mode for testing
        render_heavy_js: Whether to render heavy JavaScript on the page
        stealth: Enable stealth mode to avoid bot detection

    Example:
        >>> request = MarkdownifyRequest(website_url="https://example.com")
    """
    website_url: str = Field(..., example="https://scrapegraphai.com/")
    headers: Optional[dict[str, str]] = Field(
        None,
        example={
            "User-Agent": "scrapegraph-py",
            "Cookie": "cookie1=value1; cookie2=value2",
        },
        description="Optional headers to send with the request, including cookies "
        "and user agent",
    )
    mock: bool = Field(default=False, description="Whether to use mock mode for the request")
    render_heavy_js: bool = Field(default=False, description="Whether to render heavy JavaScript on the page")
    stealth: bool = Field(default=False, description="Enable stealth mode to avoid bot detection")

    @model_validator(mode="after")
    def validate_url(self) -> "MarkdownifyRequest":
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


class GetMarkdownifyRequest(BaseModel):
    """Request model for get_markdownify endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetMarkdownifyRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self
