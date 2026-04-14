"""Pydantic models for the SGAI v2 search endpoint."""

from typing import Any, Dict, Optional

from pydantic import Field, conint, model_validator

from .shared import CamelModel, FetchConfig


class SearchRequest(CamelModel):
    """Request model for POST /api/v2/search."""

    query: str = Field(..., description="The search query")
    num_results: conint(ge=1, le=20) = Field(
        default=3, description="Number of results to return (1-20)"
    )
    format: str = Field(default="markdown", description="Search scrape format")
    mode: str = Field(default="prune", description="HTML processing mode")
    fetch_config: Optional[FetchConfig] = Field(
        default=None, description="Fetch configuration options"
    )
    prompt: Optional[str] = Field(
        default=None,
        description="Prompt used when extracting structured results from search pages",
    )
    schema_: Optional[Dict[str, Any]] = Field(
        default=None,
        alias="schema",
        serialization_alias="schema",
        validation_alias="schema",
        description="JSON Schema defining the structure of extracted search data",
    )
    country: Optional[str] = Field(
        default=None,
        max_length=10,
        serialization_alias="locationGeoCode",
        description="Two-letter country code for geo-targeted results (e.g. 'us', 'it')",
    )
    time_range: Optional[str] = Field(
        default=None,
        description="Relative recency filter for search results",
    )

    @model_validator(mode="after")
    def validate_query(self) -> "SearchRequest":
        if not self.query or not self.query.strip():
            raise ValueError("Query cannot be empty")
        if self.schema_ is not None and not self.prompt:
            raise ValueError("schema requires prompt")
        return self
