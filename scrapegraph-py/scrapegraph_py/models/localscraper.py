# Models for localscraper endpoint

from typing import Optional, Type
from uuid import UUID

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, model_validator


class LocalScraperRequest(BaseModel):
    user_prompt: str = Field(
        ...,
        example="Extract info about the company",
    )
    website_html: str = Field(
        ...,
        example="<html><body><h1>Title</h1><p>Content</p></body></html>",
        description="HTML content, maximum size 2MB",
    )
    output_schema: Optional[Type[BaseModel]] = None

    @model_validator(mode="after")
    def validate_user_prompt(self) -> "LocalScraperRequest":
        if self.user_prompt is None or not self.user_prompt.strip():
            raise ValueError("User prompt cannot be empty")
        if not any(c.isalnum() for c in self.user_prompt):
            raise ValueError("User prompt must contain a valid prompt")
        return self

    @model_validator(mode="after")
    def validate_website_html(self) -> "LocalScraperRequest":
        if self.website_html is None or not self.website_html.strip():
            raise ValueError("Website HTML cannot be empty")

        if len(self.website_html.encode("utf-8")) > 2 * 1024 * 1024:
            raise ValueError("Website HTML content exceeds maximum size of 2MB")

        try:
            soup = BeautifulSoup(self.website_html, "html.parser")
            if not soup.find():
                raise ValueError("Invalid HTML - no parseable content found")
        except Exception as e:
            raise ValueError(f"Invalid HTML structure: {str(e)}")

        return self

    def model_dump(self, *args, **kwargs) -> dict:
        data = super().model_dump(*args, **kwargs)
        # Convert the Pydantic model schema to dict if present
        if self.output_schema is not None:
            data["output_schema"] = self.output_schema.model_json_schema()
        return data


class GetLocalScraperRequest(BaseModel):
    """Request model for get_localscraper endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetLocalScraperRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self
