# Models for smartscraper endpoint

from typing import Optional, Type
from uuid import UUID

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, model_validator


class SmartScraperRequest(BaseModel):
    user_prompt: str = Field(
        ...,
        example="Extract info about the company",
    )
    website_url: Optional[str] = Field(
        default=None, example="https://scrapegraphai.com/"
    )
    website_html: Optional[str] = Field(
        default=None,
        example="<html><body><h1>Title</h1><p>Content</p></body></html>",
        description="HTML content, maximum size 2MB",
    )
    headers: Optional[dict[str, str]] = Field(
        None,
        example={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": "cookie1=value1; cookie2=value2",
        },
        description="Optional headers to send with the request, including cookies and user agent",
    )
    output_schema: Optional[Type[BaseModel]] = None

    @model_validator(mode="after")
    def validate_user_prompt(self) -> "SmartScraperRequest":
        if self.user_prompt is None or not self.user_prompt.strip():
            raise ValueError("User prompt cannot be empty")
        if not any(c.isalnum() for c in self.user_prompt):
            raise ValueError("User prompt must contain a valid prompt")
        return self

    @model_validator(mode="after")
    def validate_url_and_html(self) -> "SmartScraperRequest":
        if self.website_html is not None:
            if len(self.website_html.encode("utf-8")) > 2 * 1024 * 1024:
                raise ValueError("Website HTML content exceeds maximum size of 2MB")
            try:
                soup = BeautifulSoup(self.website_html, "html.parser")
                if not soup.find():
                    raise ValueError("Invalid HTML - no parseable content found")
            except Exception as e:
                raise ValueError(f"Invalid HTML structure: {str(e)}")
        elif self.website_url is not None:
            if not self.website_url.strip():
                raise ValueError("Website URL cannot be empty")
            if not (
                self.website_url.startswith("http://")
                or self.website_url.startswith("https://")
            ):
                raise ValueError("Invalid URL")
        else:
            raise ValueError("Either website_url or website_html must be provided")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        data = super().model_dump(*args, **kwargs)
        # Convert the Pydantic model schema to dict if present
        if self.output_schema is not None:
            data["output_schema"] = self.output_schema.model_json_schema()
        return data


class GetSmartScraperRequest(BaseModel):
    """Request model for get_smartscraper endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetSmartScraperRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self
