# Models for feedback endpoint

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class FeedbackRequest(BaseModel):
    """Request model for feedback endpoint"""

    request_id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    rating: int = Field(..., ge=1, le=5, example=5)
    feedback_text: Optional[str] = Field(None, example="Great results!")

    @model_validator(mode="after")
    def validate_request_id(self) -> "FeedbackRequest":
        try:
            UUID(self.request_id)
        except ValueError:
            raise ValueError("request_id must be a valid UUID")
        return self

    def model_dump(self, *args, **kwargs) -> dict:
        # Set exclude_none=True to exclude None values from serialization
        kwargs.setdefault('exclude_none', True)
        return super().model_dump(*args, **kwargs)
