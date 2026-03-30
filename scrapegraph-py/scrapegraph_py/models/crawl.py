"""
Pydantic models for the v2 Crawl endpoints.

POST /v2/crawl         - Start a crawl job
GET  /v2/crawl/:id     - Get crawl status/results
POST /v2/crawl/:id/stop   - Stop a running crawl
POST /v2/crawl/:id/resume - Resume a stopped crawl
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, conint, model_validator

from .shared import FetchConfig


class CrawlFormat(str, Enum):
    """Output format for crawled pages."""

    MARKDOWN = "markdown"
    HTML = "html"


class CrawlRequest(BaseModel):
    """Request model for POST /v2/crawl."""

    url: str = Field(..., description="The starting URL for the crawl")
    depth: conint(ge=1, le=10) = Field(
        default=2, description="Maximum crawl depth (1-10)"
    )
    max_pages: conint(ge=1, le=100) = Field(
        default=10, description="Maximum number of pages to crawl (1-100)"
    )
    format: CrawlFormat = Field(
        default=CrawlFormat.MARKDOWN,
        description="Output format: markdown or html",
    )
    include_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to include (e.g. ['/products/*', '/blog/**'])",
    )
    exclude_patterns: Optional[List[str]] = Field(
        default=None,
        description="URL patterns to exclude (e.g. ['/admin/*', '/api/*'])",
    )
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )

    @model_validator(mode="after")
    def validate_url(self) -> "CrawlRequest":
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return self

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
