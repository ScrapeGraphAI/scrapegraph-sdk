# Models for searchscraper endpoint

from typing import Optional, Type
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class SearchScraperRequest(BaseModel):
    user_prompt: str = Field(..., example="What is the latest version of Python?")
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
    def validate_user_prompt(self) -> "SearchScraperRequest":
        if self.user_prompt is None or not self.user_prompt.strip():
            raise ValueError("User prompt cannot be empty")
        if not any(c.isalnum() for c in self.user_prompt):
            raise ValueError("User prompt must contain a valid prompt")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
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
