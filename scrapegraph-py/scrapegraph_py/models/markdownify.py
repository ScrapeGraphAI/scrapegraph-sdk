# Models for markdownify endpoint

from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class MarkdownifyRequest(BaseModel):
    website_url: str = Field(..., example="https://scrapegraphai.com/")

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
