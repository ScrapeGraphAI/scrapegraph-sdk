"""
Pydantic models for the Agentic Scraper API endpoint.

This module defines request and response models for the Agentic Scraper endpoint,
which performs automated browser interactions and optional AI data extraction.

The Agentic Scraper can:
- Execute a sequence of browser actions (click, type, scroll, etc.)
- Handle authentication flows and form submissions
- Optionally extract structured data using AI after interactions
- Maintain browser sessions across multiple steps
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class AgenticScraperRequest(BaseModel):
    """
    Request model for the Agentic Scraper endpoint.

    This model validates and structures requests for automated browser
    interactions with optional AI extraction.

    Attributes:
        url: The starting URL for the scraping session
        use_session: Whether to maintain browser session across steps
        steps: List of actions to perform (e.g., "Type email@example.com in email input")
        user_prompt: Optional prompt for AI extraction (required if ai_extraction=True)
        output_schema: Optional schema for structured data extraction
        ai_extraction: Whether to use AI for data extraction after interactions
        headers: Optional HTTP headers
        mock: Whether to use mock mode for testing
        render_heavy_js: Whether to render heavy JavaScript

    Example:
        >>> request = AgenticScraperRequest(
        ...     url="https://dashboard.example.com",
        ...     steps=[
        ...         "Type user@example.com in email input",
        ...         "Type password123 in password input",
        ...         "Click login button"
        ...     ],
        ...     ai_extraction=True,
        ...     user_prompt="Extract user dashboard information"
        ... )
    """
    url: str = Field(
        ...,
        example="https://dashboard.scrapegraphai.com/",
        description="The URL to scrape"
    )
    use_session: bool = Field(
        default=True,
        description="Whether to use session for the scraping"
    )
    steps: List[str] = Field(
        ...,
        example=[
            "Type email@gmail.com in email input box",
            "Type test-password@123 in password inputbox",
            "click on login"
        ],
        description="List of steps to perform on the webpage"
    )
    user_prompt: Optional[str] = Field(
        default=None,
        example="Extract user information and available dashboard sections",
        description="Prompt for AI extraction (only used when ai_extraction=True)"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        example={
            "user_info": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "email": {"type": "string"},
                    "dashboard_sections": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        description="Schema for structured data extraction (only used when ai_extraction=True)"
    )
    ai_extraction: bool = Field(
        default=False,
        description="Whether to use AI for data extraction from the scraped content"
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
    mock: bool = Field(default=False, description="Whether to use mock mode for the request")
    render_heavy_js: bool = Field(default=False, description="Whether to render heavy JavaScript on the page")
    stealth: bool = Field(default=False, description="Enable stealth mode to avoid bot detection")

    @model_validator(mode="after")
    def validate_url(self) -> "AgenticScraperRequest":
        if not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (
            self.url.startswith("http://")
            or self.url.startswith("https://")
        ):
            raise ValueError("Invalid URL - must start with http:// or https://")
        return self

    @model_validator(mode="after")
    def validate_steps(self) -> "AgenticScraperRequest":
        if not self.steps:
            raise ValueError("Steps cannot be empty")
        if any(not step.strip() for step in self.steps):
            raise ValueError("All steps must contain valid instructions")
        return self

    @model_validator(mode="after")
    def validate_ai_extraction(self) -> "AgenticScraperRequest":
        if self.ai_extraction:
            if not self.user_prompt or not self.user_prompt.strip():
                raise ValueError("user_prompt is required when ai_extraction=True")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        # Set exclude_none=True to exclude None values from serialization
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class GetAgenticScraperRequest(BaseModel):
    """Request model for get_agenticscraper endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetAgenticScraperRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self
