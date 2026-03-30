"""
Shared configuration models for the ScrapeGraphAI v2 API.

These models are used across multiple endpoints for fetch and LLM configuration.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class FetchConfig(BaseModel):
    """Configuration for how pages are fetched."""

    mock: bool = Field(default=False, description="Use mock mode for testing")
    stealth: bool = Field(
        default=False, description="Enable stealth mode to avoid bot detection"
    )
    scrolls: Optional[int] = Field(
        default=None, ge=0, le=100, description="Number of scrolls to perform (0-100)"
    )
    country: Optional[str] = Field(
        default=None, description="Country code for geo-located requests (e.g. 'us')"
    )
    cookies: Optional[Dict[str, str]] = Field(
        default=None, description="Cookies to send with the request"
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Custom HTTP headers to send with the request"
    )
    wait_ms: Optional[int] = Field(
        default=None,
        ge=0,
        description="Milliseconds to wait before scraping for JS rendering",
    )
    render_js: bool = Field(
        default=False, description="Whether to render heavy JavaScript"
    )

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)


class LlmConfig(BaseModel):
    """Configuration for the LLM used in extraction."""

    model: Optional[str] = Field(
        default=None, description="LLM model to use for extraction"
    )
    temperature: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0.0-2.0)",
    )
    max_tokens: Optional[int] = Field(
        default=None, ge=1, description="Maximum tokens in the response"
    )
    chunker: Optional[str] = Field(
        default=None, description="Chunking strategy for large pages"
    )

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
