import pytest
from pydantic import BaseModel, ValidationError

from scrapegraph_py.models.crawl import CrawlRequest, GetCrawlRequest
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


def test_crawl_request_validation():
    # Example schema
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Test Schema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
        "required": ["name"],
    }

    # Valid input with all parameters
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract company information",
        data_schema=schema,
        cache_website=True,
        depth=2,
        max_pages=5,
        same_domain_only=True,
        batch_size=1,
    )
    assert request.url == "https://example.com"
    assert request.prompt == "Extract company information"
    assert request.data_schema == schema
    assert request.cache_website is True
    assert request.depth == 2
    assert request.max_pages == 5
    assert request.same_domain_only is True
    assert request.batch_size == 1

    # Valid input with minimal parameters
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract company information",
        data_schema=schema,
    )
    assert request.url == "https://example.com"
    assert request.prompt == "Extract company information"
    assert request.data_schema == schema
    assert request.cache_website is True  # default
    assert request.depth == 2  # default
    assert request.max_pages == 2  # default
    assert request.same_domain_only is True  # default
    assert request.batch_size == 1  # default

    # Invalid URL
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="invalid-url",
            prompt="Extract company information",
            data_schema=schema,
        )

    # Empty URL
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="",
            prompt="Extract company information",
            data_schema=schema,
        )

    # Empty prompt
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="",
            data_schema=schema,
        )

    # Invalid prompt (no alphanumeric characters)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="!@#$%^",
            data_schema=schema,
        )

    # Empty schema
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema={},
        )

    # Invalid schema (not a dict)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema="not a dict",
        )

    # Invalid depth (too low)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            depth=0,
        )

    # Invalid depth (too high)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            depth=11,
        )

    # Invalid max_pages (too low)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            max_pages=0,
        )

    # Invalid max_pages (too high)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            max_pages=101,
        )

    # Invalid batch_size (too low)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            batch_size=0,
        )

    # Invalid batch_size (too high)
    with pytest.raises(ValidationError):
        CrawlRequest(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            batch_size=11,
        )


def test_get_crawl_request_validation():
    # Valid UUID
    request = GetCrawlRequest(crawl_id="123e4567-e89b-12d3-a456-426614174000")
    assert request.crawl_id == "123e4567-e89b-12d3-a456-426614174000"

    # Invalid UUID
    with pytest.raises(ValidationError):
        GetCrawlRequest(crawl_id="invalid-uuid")


def test_smartscraper_request_steps_validation():
    """Test steps validation for SmartScraperRequest."""
    
    # Valid request with steps
    steps = [
        "click on search bar",
        "wait for 500ms",
        "fill email input box with user@example.com",
        "wait a sec",
        "click on the first result"
    ]
    
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Extract user profile",
        steps=steps
    )
    
    assert request.website_url == "https://example.com"
    assert request.user_prompt == "Extract user profile"
    assert request.steps == steps
    assert len(request.steps) == 5
    
    # Valid request without steps (should be None)
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Extract user profile"
    )
    
    assert request.steps is None
    
    # Valid request with empty steps list
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Extract user profile",
        steps=[]
    )
    
    assert request.steps == []
    
    # Test model_dump includes steps
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Extract user profile",
        steps=["click on button", "wait for 1 second"]
    )
    
    dumped = request.model_dump()
    assert "steps" in dumped
    assert dumped["steps"] == ["click on button", "wait for 1 second"]
    
    # Test model_dump excludes None steps
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Extract user profile",
        steps=None
    )
    
    dumped = request.model_dump()
    assert "steps" not in dumped  # Should be excluded due to exclude_none=True


def test_markdownify_request_steps_validation():
    """Test steps validation for MarkdownifyRequest."""
    
    # Valid request with steps
    steps = [
        "click on search bar",
        "wait for 500ms",
        "fill email input box with user@example.com",
        "wait a sec",
        "click on the first result"
    ]
    
    request = MarkdownifyRequest(
        website_url="https://example.com",
        steps=steps
    )
    
    assert request.website_url == "https://example.com"
    assert request.steps == steps
    assert len(request.steps) == 5
    
    # Valid request without steps (should be None)
    request = MarkdownifyRequest(
        website_url="https://example.com"
    )
    
    assert request.steps is None
    
    # Valid request with empty steps list
    request = MarkdownifyRequest(
        website_url="https://example.com",
        steps=[]
    )
    
    assert request.steps == []
    
    # Valid request with steps and headers
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123"
    }
    
    request = MarkdownifyRequest(
        website_url="https://example.com",
        headers=headers,
        steps=["click on menu", "wait for 1 second"]
    )
    
    assert request.website_url == "https://example.com"
    assert request.headers == headers
    assert request.steps == ["click on menu", "wait for 1 second"]
    
    # Test model_dump includes steps
    request = MarkdownifyRequest(
        website_url="https://example.com",
        steps=["click on button", "wait for 1 second"]
    )
    
    dumped = request.model_dump()
    assert "steps" in dumped
    assert dumped["steps"] == ["click on button", "wait for 1 second"]
    
    # Test model_dump excludes None steps
    request = MarkdownifyRequest(
        website_url="https://example.com",
        steps=None
    )
    
    dumped = request.model_dump()
    assert "steps" not in dumped  # Should be excluded due to exclude_none=True


def test_smartscraper_request_steps_with_other_params():
    """Test steps functionality combined with other SmartScraperRequest parameters."""
    
    class ExampleSchema(BaseModel):
        name: str
        age: int
    
    steps = [
        "click on profile section",
        "wait for 2 seconds",
        "scroll to bottom",
        "click on load more"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Authorization": "Bearer token123"
    }
    
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Extract user data",
        headers=headers,
        output_schema=ExampleSchema,
        number_of_scrolls=5,
        steps=steps
    )
    
    assert request.website_url == "https://example.com"
    assert request.user_prompt == "Extract user data"
    assert request.headers == headers
    assert request.output_schema == ExampleSchema
    assert request.number_of_scrolls == 5
    assert request.steps == steps
    
    # Test model_dump with all parameters
    dumped = request.model_dump()
    assert "steps" in dumped
    assert dumped["steps"] == steps
    assert dumped["number_of_scrolls"] == 5
    assert dumped["headers"] == headers
    assert "output_schema" in dumped


def test_markdownify_request_steps_with_headers():
    """Test steps functionality combined with headers in MarkdownifyRequest."""
    
    steps = [
        "click on accept cookies",
        "wait for 1 second",
        "click on main content",
        "scroll to article"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Cookie": "consent=true; session=abc123"
    }
    
    request = MarkdownifyRequest(
        website_url="https://example.com/blog/article",
        headers=headers,
        steps=steps
    )
    
    assert request.website_url == "https://example.com/blog/article"
    assert request.headers == headers
    assert request.steps == steps
    assert len(request.steps) == 4
    
    # Test model_dump with all parameters
    dumped = request.model_dump()
    assert "steps" in dumped
    assert dumped["steps"] == steps
    assert dumped["headers"] == headers
    assert dumped["website_url"] == "https://example.com/blog/article"


def test_steps_field_types():
    """Test that steps field accepts proper types and validates correctly."""
    
    # Test with valid list of strings
    valid_steps = ["step1", "step2", "step3"]
    
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Test prompt",
        steps=valid_steps
    )
    
    assert request.steps == valid_steps
    assert isinstance(request.steps, list)
    assert all(isinstance(step, str) for step in request.steps)
    
    # Test with empty list
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Test prompt",
        steps=[]
    )
    
    assert request.steps == []
    assert isinstance(request.steps, list)
    
    # Test with None (should be accepted)
    request = SmartScraperRequest(
        website_url="https://example.com",
        user_prompt="Test prompt",
        steps=None
    )
    
    assert request.steps is None


def test_steps_common_patterns():
    """Test common step patterns to ensure they work correctly."""
    
    # Authentication flow steps
    auth_steps = [
        "click on login button",
        "wait for 1 second",
        "fill username field with user@example.com",
        "wait for 200ms",
        "fill password field with password123",
        "wait for 300ms",
        "click submit button",
        "wait for 3 seconds"
    ]
    
    request = SmartScraperRequest(
        website_url="https://example.com/login",
        user_prompt="Extract user profile after login",
        steps=auth_steps
    )
    
    assert len(request.steps) == 8
    assert "login" in request.steps[0]
    assert "username" in request.steps[2]
    assert "password" in request.steps[4]
    
    # Navigation flow steps
    nav_steps = [
        "click on menu button",
        "wait for 500ms",
        "click on products section",
        "wait for 1 second",
        "scroll to product list",
        "click on first product",
        "wait for 2 seconds"
    ]
    
    request = MarkdownifyRequest(
        website_url="https://example.com/products",
        steps=nav_steps
    )
    
    assert len(request.steps) == 7
    assert "menu" in request.steps[0]
    assert "products" in request.steps[2]
    assert "scroll" in request.steps[4]
    
    # Form interaction steps
    form_steps = [
        "scroll to contact form",
        "wait for 500ms",
        "fill name field with John Doe",
        "wait for 200ms",
        "fill email field with john@example.com",
        "wait for 200ms",
        "fill message field with Hello World",
        "wait for 300ms",
        "click submit button"
    ]
    
    request = SmartScraperRequest(
        website_url="https://example.com/contact",
        user_prompt="Extract contact form confirmation",
        steps=form_steps
    )
    
    assert len(request.steps) == 9
    assert "contact form" in request.steps[0]
    assert "name field" in request.steps[2]
    assert "email field" in request.steps[4]
    assert "message field" in request.steps[6]
