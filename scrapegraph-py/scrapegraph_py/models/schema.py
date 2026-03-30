"""
Pydantic models for the v2 Schema endpoint.

POST /v2/schema - AI-powered JSON schema generation.
"""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, model_validator


class SchemaRequest(BaseModel):
    """Request model for POST /v2/schema."""

    prompt: str = Field(
        ..., description="Natural language description of the schema to generate"
    )
    existing_schema: Optional[Dict[str, Any]] = Field(
        default=None, description="Existing JSON schema to modify or extend"
    )

    @model_validator(mode="after")
    def validate_prompt(self) -> "SchemaRequest":
        if not self.prompt or not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        return self

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
