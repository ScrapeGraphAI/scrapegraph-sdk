"""Pydantic models for the SGAI v2 monitor endpoints."""

from typing import Any, Dict, List, Optional

from pydantic import Field, model_validator

from scrapegraph_py.utils.payloads import build_single_format_entry

from .shared import CamelModel, FetchConfig


class MonitorCreateRequest(CamelModel):
    """Request model for POST /api/v2/monitor."""

    url: str = Field(..., description="URL to monitor")
    name: Optional[str] = Field(default=None, description="Name of the monitor")
    formats: List[Dict[str, Any]] = Field(
        default_factory=lambda: [build_single_format_entry("markdown")],
        description="Requested output formats for each monitor run",
    )
    webhook_url: Optional[str] = Field(
        default=None, description="Webhook URL invoked when changes are detected"
    )
    interval: str = Field(..., description="Cron expression for scheduling")
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "MonitorCreateRequest":
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if self.name is not None and not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self.formats:
            raise ValueError("formats must contain at least one entry")
        parts = self.interval.strip().split()
        if len(parts) != 5:
            raise ValueError("Interval cron expression must have exactly 5 fields")
        return self
