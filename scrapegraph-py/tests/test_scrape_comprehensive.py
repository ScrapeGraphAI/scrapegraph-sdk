"""Comprehensive tests for Scrape API functionality"""

import pytest
from unittest.mock import Mock, patch
from pydantic import ValidationError

from scrapegraph_py import Client, AsyncClient
from scrapegraph_py.models.scrape import ScrapeRequest, GetScrapeRequest
from scrapegraph_py.exceptions import APIError


class TestScrapeAPIIntegration:
    """Integration tests for Scrape API"""

    def test_scrape_basic_request(self):
        """Test basic scrape request"""
        client = Client(api_key="test-key", mock=True)
        
        result = client.scrape(
            website_url="https://example.com",
            render_heavy_js=False
        )
        
        assert "request_id" in result
        assert result["request_id"].startswith("mock-req-")
        client.close()

    def test_scrape_with_heavy_js(self):
        """Test scrape request with heavy JS rendering"""
        client = Client(api_key="test-key", mock=True)
        
        result = client.scrape(
            website_url="https://example.com",
            render_heavy_js=True
        )
        
        assert "request_id" in result
        client.close()

    def test_scrape_with_headers(self):
        """Test scrape request with custom headers"""
        client = Client(api_key="test-key", mock=True)
        
        custom_headers = {
            "User-Agent": "Mozilla/5.0 Test Browser",
            "Accept-Language": "en-US,en;q=0.9",
            "Cookie": "session=test123"
        }
        
        result = client.scrape(
            website_url="https://example.com",
            render_heavy_js=False,
            headers=custom_headers
        )
        
        assert "request_id" in result
        client.close()

    def test_get_scrape_result(self):
        """Test getting scrape result by request ID"""
        client = Client(api_key="test-key", mock=True)
        
        # First make a scrape request
        scrape_result = client.scrape(
            website_url="https://example.com",
            render_heavy_js=False
        )
        
        request_id = scrape_result["request_id"]
        
        # Then get the result
        result = client.get_scrape(request_id)
        
        # In mock mode, we should get a mock response
        assert "status" in result
        client.close()

    @pytest.mark.asyncio
    async def test_async_scrape_basic_request(self):
        """Test basic async scrape request"""
        async with AsyncClient(api_key="test-key", mock=True) as client:
            result = await client.scrape(
                website_url="https://example.com",
                render_heavy_js=False
            )
            
            assert "request_id" in result
            assert result["request_id"].startswith("mock-req-")

    @pytest.mark.asyncio
    async def test_async_scrape_with_heavy_js(self):
        """Test async scrape request with heavy JS rendering"""
        async with AsyncClient(api_key="test-key", mock=True) as client:
            result = await client.scrape(
                website_url="https://example.com",
                render_heavy_js=True
            )
            
            assert "request_id" in result

    @pytest.mark.asyncio
    async def test_async_get_scrape_result(self):
        """Test getting async scrape result by request ID"""
        async with AsyncClient(api_key="test-key", mock=True) as client:
            # First make a scrape request
            scrape_result = await client.scrape(
                website_url="https://example.com",
                render_heavy_js=False
            )
            
            request_id = scrape_result["request_id"]
            
            # Then get the result
            result = await client.get_scrape(request_id)
            
            # In mock mode, we should get a mock response
            assert "status" in result


class TestScrapeValidation:
    """Test scrape request validation"""

    def test_invalid_url_schemes(self):
        """Test that invalid URL schemes are rejected"""
        invalid_urls = [
            "ftp://example.com",
            "file:///path/to/file",
            "gopher://example.com",
            "mailto:test@example.com",
            "tel:+1234567890"
        ]
        
        for url in invalid_urls:
            with pytest.raises(ValidationError):
                ScrapeRequest(website_url=url)

    def test_malformed_urls(self):
        """Test that malformed URLs are rejected"""
        malformed_urls = [
            "not-a-url",
            "http://",
            "https://",
            "://example.com",
            "http:///path",
            "https:example.com",
            "http//example.com"
        ]
        
        for url in malformed_urls:
            with pytest.raises(ValidationError):
                ScrapeRequest(website_url=url)

    def test_empty_and_none_urls(self):
        """Test that empty and None URLs are rejected"""
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="")
        
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url=None)
        
        with pytest.raises(ValidationError):
            ScrapeRequest(website_url="   ")

    def test_valid_url_variations(self):
        """Test that valid URL variations are accepted"""
        valid_urls = [
            "https://example.com",
            "http://example.com", 
            "https://sub.example.com",
            "https://example.com:8080",
            "https://example.com/path",
            "https://example.com/path?param=value",
            "https://example.com/path#fragment",
            "https://example.com/path?param=value&other=test#fragment",
            "https://user:pass@example.com/path",
            "https://192.168.1.1",
            "https://[::1]:8080/path"
        ]
        
        for url in valid_urls:
            request = ScrapeRequest(website_url=url)
            assert request.website_url == url

    def test_render_heavy_js_boolean(self):
        """Test render_heavy_js parameter validation"""
        # Should accept boolean values
        request1 = ScrapeRequest(website_url="https://example.com", render_heavy_js=True)
        assert request1.render_heavy_js is True
        
        request2 = ScrapeRequest(website_url="https://example.com", render_heavy_js=False)
        assert request2.render_heavy_js is False
        
        # Should default to False
        request3 = ScrapeRequest(website_url="https://example.com")
        assert request3.render_heavy_js is False

    def test_headers_validation(self):
        """Test headers parameter validation"""
        # Should accept valid headers
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US",
            "Cookie": "session=123",
            "Authorization": "Bearer token123"
        }
        
        request = ScrapeRequest(
            website_url="https://example.com",
            headers=headers
        )
        assert request.headers == headers
        
        # Should accept None headers
        request2 = ScrapeRequest(website_url="https://example.com", headers=None)
        assert request2.headers is None


class TestScrapeErrorHandling:
    """Test error handling in scrape operations"""

    def test_invalid_api_key_format(self):
        """Test handling of invalid API key format"""
        with pytest.raises(ValueError, match="Invalid API key format"):
            Client(api_key="invalid-key-format")

    def test_missing_api_key(self):
        """Test handling of missing API key"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="SGAI_API_KEY not provided"):
                Client.from_env()

    @patch('requests.Session.request')
    def test_api_error_handling(self, mock_request):
        """Test API error response handling"""
        # Mock an API error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"error": "Invalid website URL"}
        mock_request.return_value = mock_response
        
        client = Client(api_key="sgai-test-key-12345678-1234-1234-1234-123456789012")
        
        with pytest.raises(APIError, match="Invalid website URL"):
            client.scrape(website_url="https://example.com")
        
        client.close()

    @patch('requests.Session.request')
    def test_connection_error_handling(self, mock_request):
        """Test connection error handling"""
        # Mock a connection error
        from requests.exceptions import ConnectionError
        mock_request.side_effect = ConnectionError("Connection failed")
        
        client = Client(api_key="sgai-test-key-12345678-1234-1234-1234-123456789012")
        
        with pytest.raises(ConnectionError, match="Failed to connect to API"):
            client.scrape(website_url="https://example.com")
        
        client.close()

    def test_get_scrape_invalid_uuid(self):
        """Test get_scrape with invalid UUID"""
        client = Client(api_key="test-key", mock=True)
        
        with pytest.raises(ValidationError):
            client.get_scrape("invalid-uuid")
        
        client.close()


class TestScrapeModelSerialization:
    """Test scrape model serialization"""

    def test_scrape_request_serialization_exclude_none(self):
        """Test that None values are excluded from serialization"""
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=False,
            headers=None
        )
        
        data = request.model_dump()
        assert "headers" not in data
        assert "mock" not in data  # Default False should be excluded
        assert data["website_url"] == "https://example.com"
        assert data["render_heavy_js"] is False

    def test_scrape_request_serialization_with_values(self):
        """Test serialization with all values provided"""
        headers = {"User-Agent": "Test Agent"}
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=True,
            headers=headers,
            mock=True
        )
        
        data = request.model_dump()
        assert data["website_url"] == "https://example.com"
        assert data["render_heavy_js"] is True
        assert data["headers"] == headers
        assert data["mock"] is True

    def test_get_scrape_request_serialization(self):
        """Test GetScrapeRequest serialization"""
        request_id = "123e4567-e89b-12d3-a456-426614174000"
        request = GetScrapeRequest(request_id=request_id)
        
        data = request.model_dump()
        assert data["request_id"] == request_id


class TestScrapeMockMode:
    """Test scrape operations in mock mode"""

    def test_mock_mode_environment_variable(self):
        """Test mock mode activation via environment variable"""
        with patch.dict('os.environ', {'SGAI_MOCK': '1', 'SGAI_API_KEY': 'test'}):
            client = Client.from_env()
            assert client.mock is True
            client.close()

    def test_mock_scrape_response_structure(self):
        """Test that mock scrape responses have expected structure"""
        client = Client(api_key="test-key", mock=True)
        
        result = client.scrape(website_url="https://example.com")
        
        assert isinstance(result, dict)
        assert "request_id" in result
        assert result["request_id"].startswith("mock-req-")
        
        client.close()

    def test_mock_get_scrape_response_structure(self):
        """Test that mock get_scrape responses have expected structure"""
        client = Client(api_key="test-key", mock=True)
        
        result = client.get_scrape("123e4567-e89b-12d3-a456-426614174000")
        
        assert isinstance(result, dict)
        assert "status" in result
        
        client.close()

    @pytest.mark.asyncio
    async def test_async_mock_scrape_response_structure(self):
        """Test that async mock scrape responses have expected structure"""
        async with AsyncClient(api_key="test-key", mock=True) as client:
            result = await client.scrape(website_url="https://example.com")
            
            assert isinstance(result, dict)
            assert "request_id" in result
            assert result["request_id"].startswith("mock-req-")


class TestScrapePerformance:
    """Test scrape performance characteristics"""

    def test_scrape_request_creation_performance(self):
        """Test that scrape request creation is fast"""
        import time
        
        start_time = time.time()
        for _ in range(1000):
            request = ScrapeRequest(
                website_url="https://example.com",
                render_heavy_js=False
            )
        end_time = time.time()
        
        # Should be able to create 1000 requests in less than 1 second
        assert end_time - start_time < 1.0

    def test_mock_scrape_performance(self):
        """Test that mock scrape responses are fast"""
        import time
        
        client = Client(api_key="test-key", mock=True)
        
        start_time = time.time()
        for _ in range(100):
            client.scrape(website_url="https://example.com")
        end_time = time.time()
        
        # Should be able to make 100 mock requests in less than 1 second
        assert end_time - start_time < 1.0
        
        client.close()
