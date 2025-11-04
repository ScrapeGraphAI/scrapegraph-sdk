"""Tests for SmartScraper models"""

import pytest
from pydantic import ValidationError

from scrapegraph_py.models.smartscraper import SmartScraperRequest, GetSmartScraperRequest


class TestSmartScraperRequest:
    """Test SmartScraperRequest model"""

    def test_valid_smartscraper_request_with_url(self):
        """Test valid smartscraper request with URL"""
        request = SmartScraperRequest(
            user_prompt="Extract the main heading",
            website_url="https://example.com",
        )
        assert request.user_prompt == "Extract the main heading"
        assert request.website_url == "https://example.com"
        assert request.render_heavy_js is False  # Default value

    def test_valid_smartscraper_request_with_html(self):
        """Test valid smartscraper request with HTML"""
        html_content = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        request = SmartScraperRequest(
            user_prompt="Extract the title",
            website_html=html_content,
        )
        assert request.user_prompt == "Extract the title"
        assert request.website_html == html_content
        assert request.render_heavy_js is False  # Default value

    def test_render_heavy_js_enabled(self):
        """Test smartscraper request with render_heavy_js enabled"""
        request = SmartScraperRequest(
            user_prompt="Find the CEO of company X and their contact details",
            website_url="https://example.com",
            render_heavy_js=True,
        )
        assert request.user_prompt == "Find the CEO of company X and their contact details"
        assert request.website_url == "https://example.com"
        assert request.render_heavy_js is True

    def test_render_heavy_js_with_other_params(self):
        """Test smartscraper request with render_heavy_js and other parameters"""
        headers = {"User-Agent": "Custom Agent"}
        cookies = {"session": "abc123"}
        request = SmartScraperRequest(
            user_prompt="Extract company information",
            website_url="https://example.com",
            render_heavy_js=True,
            headers=headers,
            cookies=cookies,
            number_of_scrolls=5,
            mock=True,
            plain_text=True,
        )
        assert request.render_heavy_js is True
        assert request.headers == headers
        assert request.cookies == cookies
        assert request.number_of_scrolls == 5
        assert request.mock is True
        assert request.plain_text is True

    def test_serialization_with_render_heavy_js(self):
        """Test smartscraper request serialization with render_heavy_js"""
        request = SmartScraperRequest(
            user_prompt="Extract data",
            website_url="https://example.com",
            render_heavy_js=True,
        )
        data = request.model_dump()
        assert data["render_heavy_js"] is True
        assert data["user_prompt"] == "Extract data"
        assert data["website_url"] == "https://example.com"

    def test_serialization_default_render_heavy_js(self):
        """Test that render_heavy_js=False is excluded from serialization by default"""
        request = SmartScraperRequest(
            user_prompt="Extract data",
            website_url="https://example.com",
            # render_heavy_js defaults to False
        )
        data = request.model_dump()
        # Should be excluded due to exclude_none=True and default False behavior
        assert "render_heavy_js" not in data or data["render_heavy_js"] is False

    def test_serialization_include_all(self):
        """Test serialization including all fields"""
        request = SmartScraperRequest(
            user_prompt="Extract data",
            website_url="https://example.com",
            render_heavy_js=False,
        )
        data = request.model_dump(exclude_none=False)
        assert data["render_heavy_js"] is False

    def test_invalid_empty_prompt(self):
        """Test smartscraper request with empty prompt"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="",
                website_url="https://example.com",
            )

    def test_invalid_none_prompt(self):
        """Test smartscraper request with None prompt"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt=None,
                website_url="https://example.com",
            )

    def test_invalid_whitespace_prompt(self):
        """Test smartscraper request with whitespace-only prompt"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="   ",
                website_url="https://example.com",
            )

    def test_invalid_no_alphanumeric_prompt(self):
        """Test smartscraper request with prompt containing no alphanumeric characters"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="!@#$%^&*()",
                website_url="https://example.com",
            )

    def test_invalid_no_url_or_html(self):
        """Test smartscraper request with neither URL nor HTML"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
            )

    def test_invalid_empty_url(self):
        """Test smartscraper request with empty URL"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_url="",
            )

    def test_invalid_url_protocol(self):
        """Test smartscraper request with invalid URL protocol"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_url="ftp://example.com",
            )

    def test_invalid_html_too_large(self):
        """Test smartscraper request with HTML content too large"""
        large_html = "<html><body>" + "x" * (2 * 1024 * 1024 + 1) + "</body></html>"
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_html=large_html,
            )

    def test_invalid_html_content(self):
        """Test smartscraper request with invalid HTML content"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_html="not html content",
            )

    def test_valid_url_formats(self):
        """Test various valid URL formats"""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://sub.example.com",
            "https://example.com:8080",
            "https://example.com/path",
            "https://example.com/path?param=value",
        ]

        for url in valid_urls:
            request = SmartScraperRequest(
                user_prompt="Extract data",
                website_url=url,
            )
            assert request.website_url == url

    def test_valid_smartscraper_request_with_markdown(self):
        """Test valid smartscraper request with Markdown"""
        markdown_content = "# Title\n\nThis is some markdown content.\n\n- Item 1\n- Item 2"
        request = SmartScraperRequest(
            user_prompt="Extract the title and list items",
            website_markdown=markdown_content,
        )
        assert request.user_prompt == "Extract the title and list items"
        assert request.website_markdown == markdown_content
        assert request.website_url is None
        assert request.website_html is None

    def test_invalid_markdown_too_large(self):
        """Test smartscraper request with Markdown content too large"""
        large_markdown = "# Title\n\n" + "x" * (2 * 1024 * 1024 + 1)
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_markdown=large_markdown,
            )

    def test_invalid_empty_markdown(self):
        """Test smartscraper request with empty Markdown"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_markdown="",
            )

    def test_invalid_whitespace_markdown(self):
        """Test smartscraper request with whitespace-only Markdown"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_markdown="   \n\n   ",
            )

    def test_invalid_both_url_and_markdown(self):
        """Test smartscraper request with both URL and Markdown (should fail)"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_url="https://example.com",
                website_markdown="# Title\n\nContent",
            )

    def test_invalid_both_html_and_markdown(self):
        """Test smartscraper request with both HTML and Markdown (should fail)"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_html="<html><body><h1>Title</h1></body></html>",
                website_markdown="# Title\n\nContent",
            )

    def test_invalid_all_three_inputs(self):
        """Test smartscraper request with URL, HTML, and Markdown (should fail)"""
        with pytest.raises(ValidationError):
            SmartScraperRequest(
                user_prompt="Extract data",
                website_url="https://example.com",
                website_html="<html><body><h1>Title</h1></body></html>",
                website_markdown="# Title\n\nContent",
            )

    def test_serialization_with_markdown(self):
        """Test smartscraper request serialization with Markdown"""
        markdown_content = "# Title\n\nContent"
        request = SmartScraperRequest(
            user_prompt="Extract data",
            website_markdown=markdown_content,
        )
        data = request.model_dump()
        assert data["website_markdown"] == markdown_content
        assert data["user_prompt"] == "Extract data"
        assert "website_url" not in data
        assert "website_html" not in data


class TestGetSmartScraperRequest:
    """Test GetSmartScraperRequest model"""

    def test_valid_get_smartscraper_request(self):
        """Test valid get smartscraper request"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetSmartScraperRequest(request_id=request_id)
        assert request.request_id == request_id

    def test_invalid_uuid_format(self):
        """Test get smartscraper request with invalid UUID format"""
        with pytest.raises(ValidationError):
            GetSmartScraperRequest(request_id="invalid-uuid")

    def test_empty_request_id(self):
        """Test get smartscraper request with empty request ID"""
        with pytest.raises(ValidationError):
            GetSmartScraperRequest(request_id="")

    def test_serialization(self):
        """Test get smartscraper request serialization"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetSmartScraperRequest(request_id=request_id)
        data = request.model_dump()
        assert data["request_id"] == request_id