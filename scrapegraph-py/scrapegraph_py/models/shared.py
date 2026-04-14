"""
Shared configuration models for the ScrapeGraphAI v2 API.

These models are used across multiple endpoints for fetch configuration.
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
    """

    AUTO = "auto"
    FAST = "fast"
    JS = "js"


class FetchConfig(CamelModel):
    """Configuration for how pages are fetched."""

    mode: FetchMode = Field(
        default=FetchMode.AUTO,
        description="Fetch/proxy mode: 'auto', 'fast', or 'js'",
    )
    stealth: bool = Field(
        default=False,
        description="Use residential proxies to bypass bot detection (+5 credits)",
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
