"""
Pydantic models for the v2 Extract endpoint.

POST /v2/extract - AI-powered data extraction (replaces SmartScraper).
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator

from .shared import FetchConfig, LlmConfig


class ExtractRequest(BaseModel):
    """Request model for POST /v2/extract."""

    url: str = Field(..., description="URL of the page to extract data from")
    prompt: str = Field(..., description="Natural language prompt describing what to extract")
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON Schema defining the structure of the extracted data",
    )
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )
    llm_config: Optional[LlmConfig] = Field(
        default=None, description="LLM configuration options"
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "ExtractRequest":
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        return self

    def to_api_payload(self) -> Dict[str, Any]:
        """Convert to API payload, handling Pydantic BaseModel output_schema."""
        data = self.model_dump(exclude_none=True)
        return data

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
