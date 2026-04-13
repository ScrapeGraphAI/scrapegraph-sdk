"""
Shared configuration models for the ScrapeGraphAI v2 API.

These models are used across multiple endpoints for fetch and LLM configuration.
"""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    """Base model that serializes using the API's camelCase field names."""

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        kwargs.setdefault("by_alias", True)
        return super().model_dump(*args, **kwargs)


class FetchMode(str, Enum):
    """Fetch/proxy mode controlling how pages are retrieved.

    - AUTO: Automatically selects the best provider chain.
    - FAST: Direct HTTP fetch via impit (fastest, no JS).
    - JS: Headless browser rendering for JavaScript-heavy pages.
    - DIRECT_STEALTH: Residential proxy with stealth headers (no JS).
    - JS_STEALTH: JS rendering combined with stealth/residential proxy.
    """

    AUTO = "auto"
    FAST = "fast"
    JS = "js"
    DIRECT_STEALTH = "direct+stealth"
    JS_STEALTH = "js+stealth"


class FetchConfig(CamelModel):
    """Configuration for how pages are fetched."""

    mode: FetchMode = Field(
        default=FetchMode.AUTO,
        description="Fetch/proxy mode: 'auto', 'fast', 'js', 'direct+stealth', 'js+stealth'",
    )
    timeout: Optional[int] = Field(
        default=None,
        ge=1000,
        le=60000,
        description="Request timeout in milliseconds (1000-60000)",
    )
    wait: Optional[int] = Field(
        default=None,
        ge=0,
        le=30000,
        description="Milliseconds to wait after page load before scraping (0-30000)",
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Custom HTTP headers to send with the request"
    )
    cookies: Optional[Dict[str, str]] = Field(
        default=None, description="Cookies to send with the request"
    )
    country: Optional[str] = Field(
        default=None,
        description="Two-letter country code for geo-located requests (e.g. 'us')",
    )
    scrolls: Optional[int] = Field(
        default=None, ge=0, le=100, description="Number of scrolls to perform (0-100)"
    )
    mock: bool = Field(default=False, description="Use mock mode for testing")


class LlmConfig(CamelModel):
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
    chunker: Optional[Dict[str, Any]] = Field(
        default=None, description="Chunking strategy for large pages"
    )
