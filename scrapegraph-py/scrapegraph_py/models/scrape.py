"""
Pydantic models for the v2 Scrape endpoint.

POST /api/v1/scrape - Fetch a page in a given format (markdown, html, screenshot, branding).
"""

from enum import Enum
from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field, model_validator

from .shared import FetchConfig


class ScrapeFormat(str, Enum):
    """Output format for the scrape endpoint."""

    MARKDOWN = "markdown"
    HTML = "html"
    SCREENSHOT = "screenshot"
    BRANDING = "branding"


class MarkdownConfig(BaseModel):
    """Configuration for markdown output."""

    mode: str = Field(default="normal", description="Markdown mode (normal, etc.)")


class HtmlConfig(BaseModel):
    """Configuration for html output."""

    mode: str = Field(default="normal", description="HTML mode")


class ScreenshotConfig(BaseModel):
    """Configuration for screenshot output."""

    full_page: bool = Field(default=False, description="Capture full page")


class ScrapeRequest(BaseModel):
    """Request model for POST /api/v1/scrape.

    The API expects a format-specific config key in the body, e.g.:
        {"url": "...", "markdown": {"mode": "normal"}}
        {"url": "...", "html": {"mode": "normal"}}
        {"url": "...", "screenshot": {"full_page": false}}
    """

    url: str = Field(..., description="URL of the page to scrape")
    format: ScrapeFormat = Field(
        default=ScrapeFormat.MARKDOWN,
        description="Output format: markdown, html, screenshot, or branding",
        exclude=True,
    )
    markdown: Optional[MarkdownConfig] = Field(default=None)
    html: Optional[HtmlConfig] = Field(default=None)
    screenshot: Optional[ScreenshotConfig] = Field(default=None)
    branding: Optional[Dict[str, Any]] = Field(default=None)
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )

    @model_validator(mode="after")
    def validate_url(self) -> "ScrapeRequest":
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return self

    @model_validator(mode="after")
    def set_format_config(self) -> "ScrapeRequest":
        """Auto-populate the format config key if none were explicitly set."""
        has_any = any([self.markdown, self.html, self.screenshot, self.branding])
        if not has_any:
            if self.format == ScrapeFormat.MARKDOWN:
                self.markdown = MarkdownConfig()
            elif self.format == ScrapeFormat.HTML:
                self.html = HtmlConfig()
            elif self.format == ScrapeFormat.SCREENSHOT:
                self.screenshot = ScreenshotConfig()
            elif self.format == ScrapeFormat.BRANDING:
                self.branding = {}
        return self

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class GetScrapeRequest(BaseModel):
    """Request model for GET /api/v1/scrape/:id."""

    request_id: str = Field(..., description="The request ID to fetch")
