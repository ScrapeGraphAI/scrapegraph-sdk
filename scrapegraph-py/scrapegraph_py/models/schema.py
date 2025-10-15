"""
Pydantic models for the Schema Generation API endpoint.

This module defines request and response models for the Schema Generation endpoint,
which uses AI to generate or refine JSON schemas based on user prompts.

The Schema Generation endpoint can:
- Generate new schemas from natural language descriptions
- Refine and extend existing schemas
- Create structured data models for web scraping
"""

from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class GenerateSchemaRequest(BaseModel):
    """Request model for generate_schema endpoint"""
    
    user_prompt: str = Field(
        ...,
        example="Find laptops with specifications like brand, processor, RAM, storage, and price",
        description="The user's search query to be refined into a schema"
    )
    existing_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        example={
            "$defs": {
                "ProductSchema": {
                    "title": "ProductSchema",
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "price": {"title": "Price", "type": "number"},
                    },
                    "required": ["name", "price"],
                }
            }
        },
        description="Optional existing JSON schema to modify/extend"
    )

    @model_validator(mode="after")
    def validate_user_prompt(self) -> "GenerateSchemaRequest":
        if not self.user_prompt or not self.user_prompt.strip():
            raise ValueError("user_prompt cannot be empty")
        return self


class GetSchemaStatusRequest(BaseModel):
    """Request model for get_schema_status endpoint"""
    
    request_id: str = Field(
        ..., 
        example="123e4567-e89b-12d3-a456-426614174000",
        description="The request ID returned from generate_schema"
    )

    @model_validator(mode="after")
    def validate_request_id(self) -> "GetSchemaStatusRequest":
        try:
            # Validate the request_id is a valid UUID
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self


class SchemaGenerationResponse(BaseModel):
    """Response model for schema generation endpoints"""
    
    request_id: str = Field(
        ...,
        description="Unique identifier for the schema generation request"
    )
    status: str = Field(
        ...,
        example="completed",
        description="Status of the schema generation (pending, processing, completed, failed)"
    )
    user_prompt: str = Field(
        ...,
        description="The original user prompt that was processed"
    )
    refined_prompt: Optional[str] = Field(
        default=None,
        description="AI-refined version of the user prompt"
    )
    generated_schema: Optional[Dict[str, Any]] = Field(
        default=None,
        description="The generated JSON schema"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if the request failed"
    )
    created_at: Optional[str] = Field(
        default=None,
        description="Timestamp when the request was created"
    )
    updated_at: Optional[str] = Field(
        default=None,
        description="Timestamp when the request was last updated"
    )

    def model_dump(self, *args, **kwargs) -> dict:
        # Set exclude_none=True to exclude None values from serialization
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(*args, **kwargs)
