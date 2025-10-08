"""Tests for Sitemap models"""

import pytest
from pydantic import ValidationError

from scrapegraph_py.models.sitemap import SitemapRequest, SitemapResponse


class TestSitemapRequest:
    """Test SitemapRequest model"""

    def test_valid_sitemap_request(self):
        """Test valid sitemap request"""
        request = SitemapRequest(website_url="https://example.com")
        assert request.website_url == "https://example.com"
        assert request.mock is False

    def test_valid_sitemap_request_with_mock(self):
        """Test valid sitemap request with mock mode"""
        request = SitemapRequest(
            website_url="https://example.com",
            mock=True
        )
        assert request.website_url == "https://example.com"
        assert request.mock is True

    def test_valid_sitemap_request_https(self):
        """Test valid sitemap request with HTTPS URL"""
        request = SitemapRequest(website_url="https://secure.example.com")
        assert request.website_url == "https://secure.example.com"

    def test_valid_sitemap_request_http(self):
        """Test valid sitemap request with HTTP URL"""
        request = SitemapRequest(website_url="http://example.com")
        assert request.website_url == "http://example.com"

    def test_valid_sitemap_request_with_path(self):
        """Test valid sitemap request with URL containing path"""
        request = SitemapRequest(website_url="https://example.com/section")
        assert request.website_url == "https://example.com/section"

    def test_valid_sitemap_request_subdomain(self):
        """Test valid sitemap request with subdomain"""
        request = SitemapRequest(website_url="https://blog.example.com")
        assert request.website_url == "https://blog.example.com"

    def test_invalid_empty_url(self):
        """Test sitemap request with empty URL"""
        with pytest.raises(ValidationError) as exc_info:
            SitemapRequest(website_url="")
        assert "Website URL cannot be empty" in str(exc_info.value)

    def test_invalid_none_url(self):
        """Test sitemap request with None URL"""
        with pytest.raises(ValidationError):
            SitemapRequest(website_url=None)

    def test_invalid_whitespace_url(self):
        """Test sitemap request with whitespace-only URL"""
        with pytest.raises(ValidationError) as exc_info:
            SitemapRequest(website_url="   ")
        assert "Website URL cannot be empty" in str(exc_info.value)

    def test_invalid_protocol_url(self):
        """Test sitemap request with invalid protocol"""
        with pytest.raises(ValidationError) as exc_info:
            SitemapRequest(website_url="ftp://example.com")
        assert "URL must start with http:// or https://" in str(exc_info.value)

    def test_invalid_no_protocol_url(self):
        """Test sitemap request with no protocol"""
        with pytest.raises(ValidationError) as exc_info:
            SitemapRequest(website_url="example.com")
        assert "URL must start with http:// or https://" in str(exc_info.value)

    def test_invalid_relative_url(self):
        """Test sitemap request with relative URL"""
        with pytest.raises(ValidationError) as exc_info:
            SitemapRequest(website_url="/path/to/page")
        assert "URL must start with http:// or https://" in str(exc_info.value)

    def test_serialization(self):
        """Test sitemap request serialization"""
        request = SitemapRequest(website_url="https://example.com")
        data = request.model_dump()
        assert data["website_url"] == "https://example.com"
        # mock defaults to False and should be excluded by exclude_none
        assert data.get("mock") is False

    def test_serialization_with_mock(self):
        """Test sitemap request serialization with mock mode"""
        request = SitemapRequest(
            website_url="https://example.com",
            mock=True
        )
        data = request.model_dump()
        assert data["website_url"] == "https://example.com"
        assert data["mock"] is True

    def test_url_validation_edge_cases(self):
        """Test URL validation edge cases"""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://sub.example.com",
            "https://example.com:8080",
            "https://example.com/path",
            "https://example.com/path?param=value",
            "https://example.com/path#fragment",
            "https://blog.example.com/posts/2024/01/article"
        ]

        for url in valid_urls:
            request = SitemapRequest(website_url=url)
            assert request.website_url == url

        invalid_urls = [
            "ftp://example.com",
            "gopher://example.com",
            "example.com",
            "/relative/path",
            "file:///path/to/file",
            "www.example.com"
        ]

        for url in invalid_urls:
            with pytest.raises(ValidationError):
                SitemapRequest(website_url=url)


class TestSitemapResponse:
    """Test SitemapResponse model"""

    def test_valid_sitemap_response(self):
        """Test valid sitemap response"""
        urls = [
            "https://example.com/",
            "https://example.com/about",
            "https://example.com/products"
        ]
        response = SitemapResponse(urls=urls)
        assert response.urls == urls
        assert len(response.urls) == 3

    def test_valid_sitemap_response_empty(self):
        """Test valid sitemap response with empty list"""
        response = SitemapResponse(urls=[])
        assert response.urls == []
        assert len(response.urls) == 0

    def test_valid_sitemap_response_single_url(self):
        """Test valid sitemap response with single URL"""
        urls = ["https://example.com/"]
        response = SitemapResponse(urls=urls)
        assert response.urls == urls
        assert len(response.urls) == 1

    def test_valid_sitemap_response_many_urls(self):
        """Test valid sitemap response with many URLs"""
        urls = [f"https://example.com/page{i}" for i in range(100)]
        response = SitemapResponse(urls=urls)
        assert len(response.urls) == 100
        assert response.urls[0] == "https://example.com/page0"
        assert response.urls[-1] == "https://example.com/page99"

    def test_invalid_none_urls(self):
        """Test sitemap response with None URLs"""
        with pytest.raises(ValidationError):
            SitemapResponse(urls=None)

    def test_invalid_missing_urls(self):
        """Test sitemap response with missing URLs field"""
        with pytest.raises(ValidationError):
            SitemapResponse()

    def test_serialization(self):
        """Test sitemap response serialization"""
        urls = [
            "https://example.com/",
            "https://example.com/about"
        ]
        response = SitemapResponse(urls=urls)
        data = response.model_dump()
        assert data["urls"] == urls
        assert isinstance(data["urls"], list)

    def test_urls_immutability(self):
        """Test that URLs list is properly stored"""
        original_urls = [
            "https://example.com/",
            "https://example.com/about"
        ]
        response = SitemapResponse(urls=original_urls)

        # Verify the response has the correct URLs
        assert response.urls == original_urls

    def test_various_url_formats(self):
        """Test sitemap response with various URL formats"""
        urls = [
            "https://example.com/",
            "https://blog.example.com/post-1",
            "https://example.com/path/to/page",
            "https://example.com:8080/api",
            "https://example.com/page?param=value",
            "https://example.com/page#section"
        ]
        response = SitemapResponse(urls=urls)
        assert response.urls == urls
        assert len(response.urls) == 6
