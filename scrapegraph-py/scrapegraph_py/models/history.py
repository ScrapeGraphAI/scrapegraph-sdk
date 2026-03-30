"""
Pydantic models for the v2 History endpoint.

GET /v2/history - Retrieve request history with optional filters.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class HistoryFilter(BaseModel):
    """Query parameters for GET /v2/history."""

    endpoint: Optional[str] = Field(
        default=None, description="Filter by endpoint name (e.g. 'scrape', 'extract')"
    )
    status: Optional[str] = Field(
        default=None, description="Filter by request status"
    )
    limit: Optional[int] = Field(
        default=None, ge=1, le=100, description="Maximum number of results (1-100)"
    )
    offset: Optional[int] = Field(
        default=None, ge=0, description="Number of results to skip"
    )

    def to_params(self) -> Dict[str, Any]:
        """Convert to query parameter dict, excluding None values."""
        return {k: v for k, v in self.model_dump().items() if v is not None}
