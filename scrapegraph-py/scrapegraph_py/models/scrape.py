"""Pydantic models for the SGAI v2 scrape endpoint."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, model_validator

from scrapegraph_py.utils.payloads import build_single_format_entry

from .shared import CamelModel, FetchConfig


class ScrapeFormat(str, Enum):
    """Supported scrape format types in SGAI v2."""

    MARKDOWN = "markdown"
    HTML = "html"
    LINKS = "links"
    IMAGES = "images"
    SUMMARY = "summary"
    JSON = "json"
    BRANDING = "branding"
    SCREENSHOT = "screenshot"


class ScrapeRequest(CamelModel):
    """Request model for POST /api/v2/scrape."""

    url: str = Field(..., description="URL of the page to scrape")
    formats: List[Dict[str, Any]] = Field(
        default_factory=lambda: [build_single_format_entry("markdown")],
        description="Requested output formats for the scrape job",
    )
    content_type: Optional[str] = Field(
        default=None, description="Optional content type override"
    )
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "ScrapeRequest":
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if not self.formats:
            raise ValueError("formats must contain at least one entry")
        return self


class GetScrapeRequest(CamelModel):
    """Request model for GET /api/v2/scrape/:id."""

    request_id: str = Field(..., description="The request ID to fetch")
