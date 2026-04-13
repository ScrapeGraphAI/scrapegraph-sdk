"""Pydantic models for the SGAI v2 crawl endpoints."""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field, conint, model_validator

from scrapegraph_py.utils.payloads import build_single_format_entry

from .shared import CamelModel, FetchConfig


class CrawlFormat(str, Enum):
    """Supported crawl format types in SGAI v2."""

    MARKDOWN = "markdown"
    HTML = "html"
    LINKS = "links"
    IMAGES = "images"
    SUMMARY = "summary"
    JSON = "json"
    BRANDING = "branding"
    SCREENSHOT = "screenshot"


class CrawlRequest(CamelModel):
    """Request model for POST /api/v2/crawl."""

    url: str = Field(..., description="The starting URL for the crawl")
    formats: List[Dict[str, Any]] = Field(
        default_factory=lambda: [build_single_format_entry("markdown")],
        description="Requested output formats for crawled pages",
    )
    max_depth: conint(ge=0) = Field(default=2, description="Maximum crawl depth")
    max_pages: conint(ge=1, le=1000) = Field(
        default=10, description="Maximum number of pages to crawl"
    )
    max_links_per_page: conint(ge=1) = Field(
        default=10, description="Maximum number of links to follow per page"
    )
    allow_external: bool = Field(
        default=False, description="Whether the crawler can cross domains"
    )
    include_patterns: Optional[List[str]] = Field(
        default=None, description="URL patterns to include"
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None, description="URL patterns to exclude"
    )
    content_types: Optional[List[str]] = Field(
        default=None, description="Allowed content types for crawl pages"
    )
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "CrawlRequest":
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if not self.formats:
            raise ValueError("formats must contain at least one entry")
        return self
