"""
Pydantic models for the v2 Search endpoint.

POST /v2/search - Web search with AI extraction (replaces SearchScraper).
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, conint, model_validator

from .shared import LlmConfig


class SearchRequest(BaseModel):
    """Request model for POST /v2/search."""

    query: str = Field(..., description="The search query")
    num_results: conint(ge=3, le=20) = Field(
        default=5, description="Number of results to return (3-20)"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="JSON Schema defining the structure of the extracted data",
    )
    llm_config: Optional[LlmConfig] = Field(
        default=None, description="LLM configuration options"
    )

    @model_validator(mode="after")
    def validate_query(self) -> "SearchRequest":
        if not self.query or not self.query.strip():
            raise ValueError("Query cannot be empty")
        return self

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
