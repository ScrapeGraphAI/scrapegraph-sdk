"""Pydantic models for the SGAI v2 history endpoint."""

from typing import Any, Dict, Optional

from pydantic import Field

from .shared import CamelModel


class HistoryFilter(CamelModel):
    """Query parameters for GET /api/v2/history."""

    page: Optional[int] = Field(
        default=None, ge=1, description="One-based results page"
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=100, description="Maximum number of results (1-100)"
    )
    service: Optional[str] = Field(
        default=None, description="Filter by service name (e.g. 'scrape', 'extract')"
    )

    def to_params(self) -> Dict[str, Any]:
        """Convert to query parameter dict, excluding None values."""
        return {k: v for k, v in self.model_dump().items() if v is not None}
