"""
Pydantic models for the v2 Monitor endpoints.

POST   /v2/monitor          - Create a monitor
GET    /v2/monitor           - List monitors
GET    /v2/monitor/:id       - Get a monitor
POST   /v2/monitor/:id/pause  - Pause a monitor
POST   /v2/monitor/:id/resume - Resume a monitor
DELETE /v2/monitor/:id       - Delete a monitor
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator

from .shared import FetchConfig, LlmConfig


class MonitorCreateRequest(BaseModel):
    """Request model for POST /v2/monitor."""

    name: str = Field(..., description="Name of the monitor")
    url: str = Field(..., description="URL to monitor")
    prompt: str = Field(..., description="Prompt for AI extraction")
    cron: str = Field(..., description="Cron expression for scheduling (5 fields)")
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON Schema defining the structure of extracted data",
    )
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )
    llm_config: Optional[LlmConfig] = Field(
        default=None, description="LLM configuration options"
    )

    @model_validator(mode="after")
    def validate_fields(self) -> "MonitorCreateRequest":
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if not self.url or not self.url.strip():
            raise ValueError("URL cannot be empty")
        if not (self.url.startswith("http://") or self.url.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        parts = self.cron.strip().split()
        if len(parts) != 5:
            raise ValueError("Cron expression must have exactly 5 fields")
        return self

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
