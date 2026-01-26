# Models for crawl endpoint

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, conint, model_validator


class CrawlRequest(BaseModel):
    """
    Request model for the crawl endpoint.

    The crawl endpoint supports two modes:
    1. AI Extraction Mode (extraction_mode=True): Uses AI to extract structured data
    2. Markdown Conversion Mode (extraction_mode=False): Converts pages to markdown (80% cheaper)

    Sitemap Support:
    - When sitemap=True, the crawler uses sitemap.xml for better page discovery
    - Recommended for structured websites (e-commerce, news sites, blogs)
    - Provides more comprehensive crawling coverage
    - Works with both AI extraction and markdown conversion modes

    Path Filtering:
    - include_paths: Specify which paths to crawl (e.g., ['/products/*', '/blog/**'])
    - exclude_paths: Specify which paths to skip (e.g., ['/admin/*', '/api/*'])
    - Supports wildcards: * (any characters), ** (any path segments)
    - exclude_paths takes precedence over include_paths
    """
    url: str = Field(
        ...,
        example="https://scrapegraphai.com/",
        description="The starting URL for the crawl",
    )
    extraction_mode: bool = Field(
        default=True,
        description="True for AI extraction mode, False for markdown conversion "
        "mode (no AI/LLM processing)",
    )
    prompt: Optional[str] = Field(
        default=None,
        example="What does the company do? and I need text content from there "
        "privacy and terms",
        description="The prompt to guide the crawl and extraction (required when "
        "extraction_mode=True)",
    )
    data_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON schema defining the structure of the extracted data "
        "(required when extraction_mode=True)",
    )
    cache_website: bool = Field(
        default=True, description="Whether to cache the website content"
    )
    depth: conint(ge=1, le=10) = Field(
        default=2, description="Maximum depth of the crawl (1-10)"
    )
    breadth: Optional[conint(ge=1)] = Field(
        default=None,
        description="Maximum number of links to crawl per depth level. "
        "If None, unlimited (default). Controls the 'width' of exploration at each depth. "
        "Useful for limiting crawl scope on large sites. Note: max_pages always takes priority - "
        "the total crawled pages will never exceed max_pages regardless of breadth setting. "
        "Ignored when sitemap=True (sitemap mode uses sitemap URLs directly instead of link discovery).",
    )
    max_pages: conint(ge=1, le=100) = Field(
        default=2, description="Maximum number of pages to crawl (1-100)"
    )
    same_domain_only: bool = Field(
        default=True, description="Whether to only crawl pages from the same domain"
    )
    batch_size: Optional[conint(ge=1, le=10)] = Field(
        default=None, description="Batch size for processing pages (1-10)"
    )
    sitemap: bool = Field(
        default=False, 
        description="Whether to use sitemap.xml for better page discovery and more comprehensive crawling. "
        "When enabled, the crawler will use the website's sitemap.xml to discover pages more efficiently, "
        "providing better coverage for structured websites like e-commerce sites, news portals, and content-heavy websites."
    )
    headers: Optional[dict[str, str]] = Field(
        None,
        example={
            "User-Agent": "scrapegraph-py",
            "Cookie": "cookie1=value1; cookie2=value2",
        },
        description="Optional headers to send with the request, including cookies "
        "and user agent",
    )
    render_heavy_js: bool = Field(default=False, description="Whether to render heavy JavaScript on the page")
    stealth: bool = Field(default=False, description="Enable stealth mode to avoid bot detection")
    include_paths: Optional[list[str]] = Field(
        default=None,
        description="List of path patterns to include (e.g., ['/products/*', '/blog/**']). "
        "Supports wildcards: * matches any characters, ** matches any path segments. "
        "If empty, all paths are included.",
        example=["/products/*", "/blog/**"]
    )
    exclude_paths: Optional[list[str]] = Field(
        default=None,
        description="List of path patterns to exclude (e.g., ['/admin/*', '/api/*']). "
        "Supports wildcards: * matches any characters, ** matches any path segments. "
        "Takes precedence over include_paths.",
        example=["/admin/*", "/api/**"]
    )
    webhook_url: Optional[str] = Field(
        default=None,
        description="URL to receive webhook notifications when the crawl job completes. "
        "The webhook will receive a POST request with the crawl results.",
        example="https://example.com/webhook"
    )

    @model_validator(mode="after")
    def validate_url(self) -> "CrawlRequest":
        if not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("Invalid URL - must start with http:// or https://")
        return self

    @model_validator(mode="after")
    def validate_extraction_mode_requirements(self) -> "CrawlRequest":
        """Validate requirements based on extraction mode"""
        if self.extraction_mode:
            # AI extraction mode - require prompt and data_schema
            if not self.prompt:
                raise ValueError("Prompt is required when extraction_mode=True")
            if not self.prompt.strip():
                raise ValueError("Prompt cannot be empty")
            if not any(c.isalnum() for c in self.prompt):
                raise ValueError("Prompt must contain valid content")

            if not self.data_schema:
                raise ValueError("Data schema is required when extraction_mode=True")
            if not isinstance(self.data_schema, dict):
                raise ValueError("Data schema must be a dictionary")
            if not self.data_schema:
                raise ValueError("Data schema cannot be empty")
        else:
            # Markdown conversion mode - prompt and data_schema should be None
            if self.prompt is not None:
                raise ValueError(
                    "Prompt should not be provided when extraction_mode=False "
                    "(markdown mode)"
                )
            if self.data_schema is not None:
                raise ValueError(
                    "Data schema should not be provided when extraction_mode=False "
                    "(markdown mode)"
                )

        return self

    @model_validator(mode="after")
    def validate_batch_size(self) -> "CrawlRequest":
        if self.batch_size is not None and (
            self.batch_size < 1 or self.batch_size > 10
        ):
            raise ValueError("Batch size must be between 1 and 10")
        return self

    @model_validator(mode="after")
    def validate_sitemap_usage(self) -> "CrawlRequest":
        """Validate sitemap usage and provide recommendations"""
        if self.sitemap:
            # Log recommendation for sitemap usage
            if self.max_pages < 5:
                # This is just a recommendation, not an error
                pass  # Could add logging here if needed
        return self

    @model_validator(mode="after")
    def validate_path_patterns(self) -> "CrawlRequest":
        """Validate path patterns start with '/'"""
        if self.include_paths:
            for path in self.include_paths:
                if not path.startswith("/"):
                    raise ValueError(f"Include path must start with '/': {path}")

        if self.exclude_paths:
            for path in self.exclude_paths:
                if not path.startswith("/"):
                    raise ValueError(f"Exclude path must start with '/': {path}")

        return self

    @model_validator(mode="after")
    def validate_webhook_url(self) -> "CrawlRequest":
        """Validate webhook URL format if provided"""
        if self.webhook_url is not None:
            if not self.webhook_url.strip():
                raise ValueError("Webhook URL cannot be empty")
            if not (
                self.webhook_url.startswith("http://")
                or self.webhook_url.startswith("https://")
            ):
                raise ValueError(
                    "Invalid webhook URL - must start with http:// or https://"
                )
        return self


class GetCrawlRequest(BaseModel):
    """Request model for get_crawl endpoint"""

    crawl_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")

    @model_validator(mode="after")
    def validate_crawl_id(self) -> "GetCrawlRequest":
        try:
            # Validate the crawl_id is a valid UUID
            UUID(self.crawl_id)
        except ValueError:
            raise ValueError("crawl_id must be a valid UUID")
        return self
