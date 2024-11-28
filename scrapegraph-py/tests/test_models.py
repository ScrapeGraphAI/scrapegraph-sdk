import pytest
from pydantic import BaseModel, ValidationError

from scrapegraph_py.models.feedback import FeedbackRequest
from scrapegraph_py.models.smartscraper import (
    GetSmartScraperRequest,
    SmartScraperRequest,
)


def test_smartscraper_request_validation():

    class ExampleSchema(BaseModel):
        name: str
        age: int

    # Valid input
    request = SmartScraperRequest(
        website_url="https://example.com", user_prompt="Describe this page."
    )
    assert request.website_url == "https://example.com"
    assert request.user_prompt == "Describe this page."

    # Test with output_schema
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Describe this page.",
        output_schema=ExampleSchema,
    )

    # When we dump the model, the output_schema should be converted to a dict
    dumped = request.model_dump()
    assert isinstance(dumped["output_schema"], dict)
    assert "properties" in dumped["output_schema"]
    assert "name" in dumped["output_schema"]["properties"]
    assert "age" in dumped["output_schema"]["properties"]

    # Invalid URL
    with pytest.raises(ValidationError):
        SmartScraperRequest(
            website_url="invalid-url", user_prompt="Describe this page."
        )

    # Empty prompt
    with pytest.raises(ValidationError):
        SmartScraperRequest(website_url="https://example.com", user_prompt="")


def test_get_smartscraper_request_validation():
    # Valid UUID
    request = GetSmartScraperRequest(request_id="123e4567-e89b-12d3-a456-426614174000")
    assert request.request_id == "123e4567-e89b-12d3-a456-426614174000"

    # Invalid UUID
    with pytest.raises(ValidationError):
        GetSmartScraperRequest(request_id="invalid-uuid")


def test_feedback_request_validation():
    # Valid input
    request = FeedbackRequest(
        request_id="123e4567-e89b-12d3-a456-426614174000",
        rating=5,
        feedback_text="Great service!",
    )
    assert request.request_id == "123e4567-e89b-12d3-a456-426614174000"
    assert request.rating == 5
    assert request.feedback_text == "Great service!"

    # Invalid rating
    with pytest.raises(ValidationError):
        FeedbackRequest(
            request_id="123e4567-e89b-12d3-a456-426614174000",
            rating=6,
            feedback_text="Great service!",
        )

    # Invalid UUID
    with pytest.raises(ValidationError):
        FeedbackRequest(
            request_id="invalid-uuid", rating=5, feedback_text="Great service!"
        )
