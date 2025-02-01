import pytest
from pydantic import BaseModel, ValidationError

from scrapegraph_py.models.feedback import FeedbackRequest
from scrapegraph_py.models.markdownify import GetMarkdownifyRequest, MarkdownifyRequest
from scrapegraph_py.models.searchscraper import (
    GetSearchScraperRequest,
    SearchScraperRequest,
)
from scrapegraph_py.models.smartscraper import (
    GetSmartScraperRequest,
    SmartScraperRequest,
)


def test_smartscraper_request_validation():
    class ExampleSchema(BaseModel):
        name: str
        age: int

    # Valid input with website_url
    request = SmartScraperRequest(
        website_url="https://example.com", user_prompt="Describe this page."
    )
    assert request.website_url == "https://example.com"
    assert request.user_prompt == "Describe this page."
    assert request.website_html is None
    assert request.headers is None

    # Valid input with website_html
    request = SmartScraperRequest(
        website_html="<html><body><p>Test content</p></body></html>",
        user_prompt="Extract info",
    )
    assert request.website_url is None
    assert request.website_html == "<html><body><p>Test content</p></body></html>"
    assert request.user_prompt == "Extract info"
    assert request.headers is None

    # Valid input with headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Describe this page.",
        headers=headers,
    )
    assert request.headers == headers

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

    # Invalid HTML
    with pytest.raises(ValidationError):
        SmartScraperRequest(
            website_html="not valid html",
            user_prompt="Extract info",
        )

    # HTML too large (>2MB)
    large_html = "x" * (2 * 1024 * 1024 + 1)
    with pytest.raises(ValidationError):
        SmartScraperRequest(
            website_html=large_html,
            user_prompt="Extract info",
        )

    # Neither URL nor HTML provided
    with pytest.raises(ValidationError):
        SmartScraperRequest(user_prompt="Extract info")


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


def test_markdownify_request_validation():
    # Valid input without headers
    request = MarkdownifyRequest(website_url="https://example.com")
    assert request.website_url == "https://example.com"
    assert request.headers is None

    # Valid input with headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }
    request = MarkdownifyRequest(website_url="https://example.com", headers=headers)
    assert request.website_url == "https://example.com"
    assert request.headers == headers

    # Invalid URL
    with pytest.raises(ValidationError):
        MarkdownifyRequest(website_url="invalid-url")

    # Empty URL
    with pytest.raises(ValidationError):
        MarkdownifyRequest(website_url="")


def test_get_markdownify_request_validation():
    # Valid UUID
    request = GetMarkdownifyRequest(request_id="123e4567-e89b-12d3-a456-426614174000")
    assert request.request_id == "123e4567-e89b-12d3-a456-426614174000"

    # Invalid UUID
    with pytest.raises(ValidationError):
        GetMarkdownifyRequest(request_id="invalid-uuid")


def test_searchscraper_request_validation():
    class ExampleSchema(BaseModel):
        name: str
        age: int

    # Valid input without headers
    request = SearchScraperRequest(user_prompt="What is the latest version of Python?")
    assert request.user_prompt == "What is the latest version of Python?"
    assert request.headers is None
    assert request.output_schema is None

    # Valid input with headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }
    request = SearchScraperRequest(
        user_prompt="What is the latest version of Python?",
        headers=headers,
    )
    assert request.headers == headers

    # Test with output_schema
    request = SearchScraperRequest(
        user_prompt="What is the latest version of Python?",
        output_schema=ExampleSchema,
    )

    # When we dump the model, the output_schema should be converted to a dict
    dumped = request.model_dump()
    assert isinstance(dumped["output_schema"], dict)
    assert "properties" in dumped["output_schema"]
    assert "name" in dumped["output_schema"]["properties"]
    assert "age" in dumped["output_schema"]["properties"]

    # Empty prompt
    with pytest.raises(ValidationError):
        SearchScraperRequest(user_prompt="")

    # Invalid prompt (no alphanumeric characters)
    with pytest.raises(ValidationError):
        SearchScraperRequest(user_prompt="!@#$%^")


def test_get_searchscraper_request_validation():
    # Valid UUID
    request = GetSearchScraperRequest(request_id="123e4567-e89b-12d3-a456-426614174000")
    assert request.request_id == "123e4567-e89b-12d3-a456-426614174000"

    # Invalid UUID
    with pytest.raises(ValidationError):
        GetSearchScraperRequest(request_id="invalid-uuid")
