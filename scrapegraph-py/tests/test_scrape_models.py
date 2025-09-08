"""Tests for Scrape models"""

import pytest
from pydantic import ValidationError

from scrapegraph_py.models.scrape import ScrapeRequest, GetScrapeRequest


class TestScrapeRequest:
    """Test ScrapeRequest model"""

    def test_valid_scrape_request(self):
        """Test valid scrape request"""
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        assert request.website_url == "https://example.com"
        assert request.render_heavy_js is False

    def test_valid_scrape_request_with_headers(self):
        """Test valid scrape request with headers"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Cookie": "session=123"
        }
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=True,
            headers=headers
        )
        assert request.website_url == "https://example.com"
        assert request.render_heavy_js is True
        assert request.headers == headers

    def test_valid_scrape_request_https(self):
        """Test valid scrape request with HTTPS URL"""
        request = ScrapeRequest(
            website_url="https://secure.example.com",
            render_heavy_js=False
        )
        assert request.website_url == "https://secure.example.com"

    def test_valid_scrape_request_http(self):
        """Test valid scrape request with HTTP URL"""
        request = ScrapeRequest(
            website_url="http://example.com",
            render_heavy_js=False
        )
        assert request.website_url == "http://example.com"

    def test_invalid_empty_url(self):
        """Test scrape request with empty URL"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="")

    def test_invalid_none_url(self):
        """Test scrape request with None URL"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url=None)

    def test_invalid_whitespace_url(self):
        """Test scrape request with whitespace-only URL"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="   ")

    def test_invalid_protocol_url(self):
        """Test scrape request with invalid protocol"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="ftp://example.com")

    def test_invalid_no_protocol_url(self):
        """Test scrape request with no protocol"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="example.com")

    def test_invalid_relative_url(self):
        """Test scrape request with relative URL"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="/path/to/page")

    def test_serialization(self):
        """Test scrape request serialization"""
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=True
        )
        data = request.model_dump()
        assert data["website_url"] == "https://example.com"
        assert data["render_heavy_js"] is True
        assert "headers" not in data  # Should be excluded when None

    def test_serialization_with_headers(self):
        """Test scrape request serialization with headers"""
        headers = {"User-Agent": "Custom Agent"}
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=False,
            headers=headers
        )
        data = request.model_dump()
        assert data["headers"] == headers

    def test_url_validation_edge_cases(self):
        """Test URL validation edge cases"""
        valid_urls = [
            "https://example.com",
            "http://example.com",
            "https://sub.example.com",
            "https://example.com:8080",
            "https://example.com/path",
            "https://example.com/path?param=value",
            "https://example.com/path#fragment"
        ]

        for url in valid_urls:
            request = ScrapeRequest(website_url=url)
            assert request.website_url == url

        invalid_urls = [
            "ftp://example.com",
            "gopher://example.com",
            "example.com",
            "/relative/path",
            "file:///path/to/file"
        ]

        for url in invalid_urls:
            with pytest.raises(ValidationError):
                ScrapeRequest(website_url=url)


class TestGetScrapeRequest:
    """Test GetScrapeRequest model"""

    def test_valid_get_scrape_request(self):
        """Test valid get scrape request"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetScrapeRequest(request_id=request_id)
        assert request.request_id == request_id

    def test_invalid_uuid_format(self):
        """Test get scrape request with invalid UUID format"""
        with pytest.raises(ValidationError):
            GetScrapeRequest(request_id="invalid-uuid")

    def test_empty_request_id(self):
        """Test get scrape request with empty request ID"""
        with pytest.raises(ValidationError):
            GetScrapeRequest(request_id="")

    def test_none_request_id(self):
        """Test get scrape request with None request ID"""
        with pytest.raises(ValidationError):
            GetScrapeRequest(request_id=None)

    def test_short_uuid(self):
        """Test get scrape request with short UUID"""
        with pytest.raises(ValidationError):
            GetScrapeRequest(request_id="123")

    def test_incomplete_uuid(self):
        """Test get scrape request with incomplete UUID"""
        with pytest.raises(ValidationError):
            GetScrapeRequest(request_id="123e4567-e89b-12d3-a456-42661417400")

    def test_serialization(self):
        """Test get scrape request serialization"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetScrapeRequest(request_id=request_id)
        data = request.model_dump()
        assert data["request_id"] == request_id

    def test_validation_passed(self):
        """Test that validation passes for valid UUIDs"""
        valid_uuids = [
            "123e4567-e89b-12d3-a456-426614174000",
            "987fcdeb-51a2-43c1-b567-890123456789",
            "00000000-0000-0000-0000-000000000000"
        ]

        for uuid_str in valid_uuids:
            request = GetScrapeRequest(request_id=uuid_str)
            assert request.request_id == uuid_str
