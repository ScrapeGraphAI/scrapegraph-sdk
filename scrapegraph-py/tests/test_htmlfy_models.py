"""
Tests for HTMLfy models
"""

import pytest
from pydantic import ValidationError

from scrapegraph_py.models.htmlfy import HtmlfyRequest, GetHtmlfyRequest


class TestHtmlfyRequest:
    """Test HtmlfyRequest model"""

    def test_valid_request(self):
        """Test valid HTMLfy request"""
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        
        assert request.website_url == "https://example.com"
        assert request.render_heavy_js is False
        assert request.headers is None

    def test_valid_request_with_headers(self):
        """Test valid HTMLfy request with headers"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": "session=123"
        }
        
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=True,
            headers=headers
        )
        
        assert request.website_url == "https://example.com"
        assert request.render_heavy_js is True
        assert request.headers == headers

    def test_valid_request_with_https(self):
        """Test valid HTMLfy request with HTTPS URL"""
        request = HtmlfyRequest(
            website_url="https://scrapegraphai.com/",
            render_heavy_js=False
        )
        
        assert request.website_url == "https://scrapegraphai.com/"

    def test_valid_request_with_http(self):
        """Test valid HTMLfy request with HTTP URL"""
        request = HtmlfyRequest(
            website_url="http://localhost:8000",
            render_heavy_js=False
        )
        
        assert request.website_url == "http://localhost:8000"

    def test_invalid_empty_url(self):
        """Test invalid request with empty URL"""
        with pytest.raises(ValidationError) as exc_info:
            HtmlfyRequest(website_url="")
        
        assert "Website URL cannot be empty" in str(exc_info.value)

    def test_invalid_none_url(self):
        """Test invalid request with None URL"""
        with pytest.raises(ValidationError) as exc_info:
            HtmlfyRequest(website_url=None)
        
        assert "Website URL cannot be empty" in str(exc_info.value)

    def test_invalid_whitespace_url(self):
        """Test invalid request with whitespace-only URL"""
        with pytest.raises(ValidationError) as exc_info:
            HtmlfyRequest(website_url="   ")
        
        assert "Website URL cannot be empty" in str(exc_info.value)

    def test_invalid_url_scheme(self):
        """Test invalid request with invalid URL scheme"""
        with pytest.raises(ValidationError) as exc_info:
            HtmlfyRequest(website_url="ftp://example.com")
        
        assert "Invalid URL" in str(exc_info.value)

    def test_invalid_url_no_scheme(self):
        """Test invalid request with URL without scheme"""
        with pytest.raises(ValidationError) as exc_info:
            HtmlfyRequest(website_url="example.com")
        
        assert "Invalid URL" in str(exc_info.value)

    def test_invalid_url_relative_path(self):
        """Test invalid request with relative path"""
        with pytest.raises(ValidationError) as exc_info:
            HtmlfyRequest(website_url="/path/to/page")
        
        assert "Invalid URL" in str(exc_info.value)

    def test_model_dump_excludes_none(self):
        """Test that model_dump excludes None values by default"""
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        
        data = request.model_dump()
        assert "website_url" in data
        assert "render_heavy_js" in data
        assert "headers" not in data  # Should be excluded as it's None

    def test_model_dump_includes_headers_when_present(self):
        """Test that model_dump includes headers when they are present"""
        headers = {"User-Agent": "Test Agent"}
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=False,
            headers=headers
        )
        
        data = request.model_dump()
        assert data["headers"] == headers

    def test_default_values(self):
        """Test default values"""
        request = HtmlfyRequest(website_url="https://example.com")
        
        assert request.render_heavy_js is False
        assert request.headers is None

    def test_render_heavy_js_true(self):
        """Test render_heavy_js set to True"""
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=True
        )
        
        assert request.render_heavy_js is True

    def test_complex_headers(self):
        """Test complex headers structure"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=False,
            headers=headers
        )
        
        assert request.headers == headers

    def test_url_with_query_params(self):
        """Test URL with query parameters"""
        url = "https://example.com/page?param1=value1&param2=value2"
        request = HtmlfyRequest(website_url=url)
        
        assert request.website_url == url

    def test_url_with_fragments(self):
        """Test URL with fragments"""
        url = "https://example.com/page#section1"
        request = HtmlfyRequest(website_url=url)
        
        assert request.website_url == url

    def test_url_with_port(self):
        """Test URL with port number"""
        url = "https://example.com:8080/page"
        request = HtmlfyRequest(website_url=url)
        
        assert request.website_url == url


class TestGetHtmlfyRequest:
    """Test GetHtmlfyRequest model"""

    def test_valid_request_id(self):
        """Test valid request ID"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetHtmlfyRequest(request_id=request_id)
        
        assert request.request_id == request_id

    def test_invalid_request_id_format(self):
        """Test invalid request ID format"""
        with pytest.raises(ValidationError) as exc_info:
            GetHtmlfyRequest(request_id="invalid-uuid")
        
        assert "request_id must be a valid UUID" in str(exc_info.value)

    def test_invalid_request_id_empty(self):
        """Test invalid request ID - empty string"""
        with pytest.raises(ValidationError) as exc_info:
            GetHtmlfyRequest(request_id="")
        
        assert "request_id must be a valid UUID" in str(exc_info.value)

    def test_invalid_request_id_none(self):
        """Test invalid request ID - None"""
        with pytest.raises(ValidationError) as exc_info:
            GetHtmlfyRequest(request_id=None)
        
        assert "request_id must be a valid UUID" in str(exc_info.value)

    def test_invalid_request_id_wrong_length(self):
        """Test invalid request ID - wrong length"""
        with pytest.raises(ValidationError) as exc_info:
            GetHtmlfyRequest(request_id="123")
        
        assert "request_id must be a valid UUID" in str(exc_info.value)

    def test_invalid_request_id_malformed(self):
        """Test invalid request ID - malformed UUID"""
        with pytest.raises(ValidationError) as exc_info:
            GetHtmlfyRequest(request_id="123e4567-e89b-12d3-a456-42661417400")
        
        assert "request_id must be a valid UUID" in str(exc_info.value)

    def test_valid_uuid_v4(self):
        """Test valid UUID v4"""
        import uuid
        request_id = str(uuid.uuid4())
        request = GetHtmlfyRequest(request_id=request_id)
        
        assert request.request_id == request_id

    def test_valid_uuid_v1(self):
        """Test valid UUID v1"""
        import uuid
        request_id = str(uuid.uuid1())
        request = GetHtmlfyRequest(request_id=request_id)
        
        assert request.request_id == request_id

    def test_example_uuid_from_docstring(self):
        """Test the example UUID from the docstring"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetHtmlfyRequest(request_id=request_id)
        
        assert request.request_id == request_id
