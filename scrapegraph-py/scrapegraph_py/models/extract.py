"""Pydantic models for the SGAI v2 extract endpoint."""

from typing import Any, Dict, Optional

from pydantic import Field, model_validator

from .shared import CamelModel, FetchConfig


class ExtractRequest(CamelModel):
    """Request model for POST /api/v2/extract."""

    url: Optional[str] = Field(default=None, description="URL of the page to extract")
    html: Optional[str] = Field(default=None, description="Raw HTML input")
    markdown: Optional[str] = Field(default=None, description="Raw markdown input")
    prompt: str = Field(
        ..., description="Natural language prompt describing what to extract"
    )
    schema_: Optional[Dict[str, Any]] = Field(
        default=None,
        alias="schema",
        serialization_alias="schema",
        validation_alias="schema",
        description="JSON Schema defining the structure of the extracted data",
    )
    mode: str = Field(default="normal", description="HTML processing mode")
    content_type: Optional[str] = Field(
        default=None, description="Optional content type override"
    )
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "ExtractRequest":
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if not any([self.url, self.html, self.markdown]):
            raise ValueError("Either url, html, or markdown is required")
        if self.url and not (
            self.url.startswith("http://") or self.url.startswith("https://")
        ):
            raise ValueError("URL must start with http:// or https://")
        return self
