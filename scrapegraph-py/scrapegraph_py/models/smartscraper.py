# Models for smartscraper endpoint

from typing import Optional, Type
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class SmartScraperRequest(BaseModel):
    user_prompt: str = Field(
        ...,
        example="Extract info about the company",
    )
    website_url: str = Field(..., example="https://scrapegraphai.com/")
    output_schema: Optional[Type[BaseModel]] = None

    @model_validator(mode="after")
    def validate_user_prompt(self) -> "SmartScraperRequest":
        if self.user_prompt is None or not self.user_prompt.strip():
            raise ValueError("User prompt cannot be empty")
        if not any(c.isalnum() for c in self.user_prompt):
            raise ValueError("User prompt must contain a valid prompt")
        return self

    @model_validator(mode="after")
    def validate_url(self) -> "SmartScraperRequest":
        if self.website_url is None or not self.website_url.strip():
            raise ValueError("Website URL cannot be empty")
        if not (
            self.website_url.startswith("http://")
            or self.website_url.startswith("https://")
        ):
            raise ValueError("Invalid URL")
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
