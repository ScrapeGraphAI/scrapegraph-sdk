# Models for agentic scraper endpoint

from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class AgenticScraperRequest(BaseModel):
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
