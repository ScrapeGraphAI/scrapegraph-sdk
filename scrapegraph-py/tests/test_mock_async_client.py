"""
Tests for AsyncClient mock mode functionality
"""
import os
from unittest.mock import patch
from uuid import uuid4

import pytest
from pydantic import BaseModel

from scrapegraph_py.async_client import AsyncClient
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


class TestAsyncMockMode:
    """Test basic async mock mode functionality"""

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_basic(self, mock_api_key):
        """Test that async mock mode bypasses HTTP calls and returns stub data"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # Test credits endpoint
            credits = await client.get_credits()
            assert credits["remaining_credits"] == 1000
            assert credits["total_credits_used"] == 0
            
            # Test smartscraper POST endpoint
            response = await client.smartscraper(
                user_prompt="Extract title", 
                website_url="https://example.com"
            )
            assert "request_id" in response
            assert response["request_id"].startswith("mock-req-")
            
            # Test feedback endpoint
            feedback = await client.submit_feedback("test-id", 5, "Great!")
            assert feedback["status"] == "success"

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_get_endpoints(self, mock_api_key, mock_uuid):
        """Test GET endpoints in async mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # Test markdownify GET
            md_result = await client.get_markdownify(mock_uuid)
            assert md_result["status"] == "completed"
            assert "Mock markdown" in md_result["content"]
            
            # Test smartscraper GET
            ss_result = await client.get_smartscraper(mock_uuid)
            assert ss_result["status"] == "completed"
            assert "result" in ss_result
            
            # Test searchscraper GET
            search_result = await client.get_searchscraper(mock_uuid)
            assert search_result["status"] == "completed"
            assert "results" in search_result

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_crawl_endpoints(self, mock_api_key, mock_uuid):
        """Test crawl-specific endpoints in async mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # Test crawl POST
            crawl_response = await client.crawl(url="https://example.com")
            assert "crawl_id" in crawl_response
            assert crawl_response["crawl_id"].startswith("mock-crawl-")
            
            # Test crawl GET
            crawl_result = await client.get_crawl(mock_uuid)
            assert crawl_result["status"] == "completed"
            assert "pages" in crawl_result

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_agentic_scraper(self, mock_api_key, mock_uuid):
        """Test agentic scraper endpoints in async mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # Test agentic scraper POST
            response = await client.agenticscraper(
                url="https://example.com",
                steps=["click button", "extract data"]
            )
            assert "request_id" in response
            assert response["request_id"].startswith("mock-req-")
            
            # Test agentic scraper GET
            result = await client.get_agenticscraper(mock_uuid)
            assert result["status"] == "completed"
            assert "actions" in result

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_searchscraper(self, mock_api_key):
        """Test searchscraper endpoint in async mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            response = await client.searchscraper(
                user_prompt="Search for information",
                num_results=5
            )
            assert "request_id" in response
            assert response["request_id"].startswith("mock-req-")

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_markdownify(self, mock_api_key):
        """Test markdownify endpoint in async mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            response = await client.markdownify(
                website_url="https://example.com",
                headers={"User-Agent": "test"}
            )
            assert "request_id" in response
            assert response["request_id"].startswith("mock-req-")


class TestAsyncMockModeCustomization:
    """Test async mock mode customization features"""

    @pytest.mark.asyncio
    async def test_async_client_mock_responses_override(self, mock_api_key):
        """Test custom mock responses via mock_responses parameter"""
        custom_responses = {
            "/v1/credits": {"remaining_credits": 42, "total_credits_used": 58}
        }
        
        async with AsyncClient(
            api_key=mock_api_key, 
            mock=True, 
            mock_responses=custom_responses
        ) as client:
            credits = await client.get_credits()
            assert credits["remaining_credits"] == 42
            assert credits["total_credits_used"] == 58

    @pytest.mark.asyncio
    async def test_async_client_mock_responses_callable(self, mock_api_key):
        """Test custom mock responses with callable values"""
        def dynamic_credits():
            return {"remaining_credits": 123, "custom_field": "dynamic"}
        
        custom_responses = {
            "/v1/credits": dynamic_credits
        }
        
        async with AsyncClient(
            api_key=mock_api_key, 
            mock=True, 
            mock_responses=custom_responses
        ) as client:
            credits = await client.get_credits()
            assert credits["remaining_credits"] == 123
            assert credits["custom_field"] == "dynamic"

    @pytest.mark.asyncio
    async def test_async_client_mock_handler_override(self, mock_api_key):
        """Test custom mock handler"""
        def custom_handler(method, url, kwargs):
            return {
                "custom_handler": True,
                "method": method,
                "url": url,
                "has_kwargs": bool(kwargs)
            }
        
        async with AsyncClient(
            api_key=mock_api_key, 
            mock=True, 
            mock_handler=custom_handler
        ) as client:
            response = await client.get_credits()
            assert response["custom_handler"] is True
            assert response["method"] == "GET"
            assert "credits" in response["url"]

    @pytest.mark.asyncio
    async def test_async_client_mock_handler_fallback(self, mock_api_key):
        """Test that mock handler exceptions fall back to defaults"""
        def failing_handler(method, url, kwargs):
            raise ValueError("Handler failed")
        
        async with AsyncClient(
            api_key=mock_api_key, 
            mock=True, 
            mock_handler=failing_handler
        ) as client:
            # Should fall back to default mock response
            response = await client.get_credits()
            assert response["remaining_credits"] == 1000


class TestAsyncMockModeEnvironment:
    """Test async mock mode environment variable support"""

    @pytest.mark.asyncio
    async def test_async_client_from_env_with_mock_flag(self, mock_api_key):
        """Test AsyncClient.from_env with explicit mock=True"""
        with patch.dict(os.environ, {"SGAI_API_KEY": mock_api_key}):
            async with AsyncClient.from_env(mock=True) as client:
                assert client.mock is True
                
                response = await client.get_credits()
                assert response["remaining_credits"] == 1000

    @pytest.mark.asyncio
    async def test_async_client_from_env_without_api_key_mock_mode(self):
        """Test AsyncClient.from_env in mock mode without SGAI_API_KEY set"""
        with patch.dict(os.environ, {}, clear=True):
            # Should work in mock mode even without API key
            async with AsyncClient.from_env(mock=True) as client:
                assert client.mock is True
                assert client.api_key == "sgai-00000000-0000-0000-0000-000000000000"
                
                response = await client.get_credits()
                assert response["remaining_credits"] == 1000

    @pytest.mark.asyncio
    async def test_async_client_from_env_sgai_mock_environment(self):
        """Test SGAI_MOCK environment variable activation"""
        test_cases = ["1", "true", "True", "TRUE", "yes", "YES", "on", "ON"]
        
        for mock_value in test_cases:
            with patch.dict(os.environ, {"SGAI_MOCK": mock_value}, clear=True):
                async with AsyncClient.from_env() as client:
                    assert client.mock is True, f"Failed for SGAI_MOCK={mock_value}"

    @pytest.mark.asyncio
    async def test_async_client_from_env_sgai_mock_disabled(self):
        """Test SGAI_MOCK environment variable disabled states"""
        test_cases = ["0", "false", "False", "FALSE", "no", "NO", "off", "OFF", ""]
        
        for mock_value in test_cases:
            with patch.dict(os.environ, {"SGAI_MOCK": mock_value}, clear=True):
                try:
                    async with AsyncClient.from_env() as client:
                        # If no exception, mock should be False
                        assert client.mock is False, f"Failed for SGAI_MOCK={mock_value}"
                except ValueError as e:
                    # Expected when no API key is set and mock is disabled
                    assert "SGAI_API_KEY environment variable not set" in str(e)

    @pytest.mark.asyncio
    async def test_async_client_from_env_with_custom_responses(self, mock_api_key):
        """Test AsyncClient.from_env with mock_responses parameter"""
        custom_responses = {
            "/v1/credits": {"remaining_credits": 999}
        }
        
        with patch.dict(os.environ, {"SGAI_API_KEY": mock_api_key}):
            async with AsyncClient.from_env(
                mock=True, 
                mock_responses=custom_responses
            ) as client:
                response = await client.get_credits()
                assert response["remaining_credits"] == 999

    @pytest.mark.asyncio
    async def test_async_client_from_env_with_custom_handler(self, mock_api_key):
        """Test AsyncClient.from_env with mock_handler parameter"""
        def custom_handler(method, url, kwargs):
            return {"from_env": True, "method": method}
        
        with patch.dict(os.environ, {"SGAI_API_KEY": mock_api_key}):
            async with AsyncClient.from_env(
                mock=True, 
                mock_handler=custom_handler
            ) as client:
                response = await client.get_credits()
                assert response["from_env"] is True
                assert response["method"] == "GET"


class TestAsyncMockModeValidation:
    """Test async mock mode validation and edge cases"""

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_disabled_by_default(self, mock_api_key):
        """Test that mock mode is disabled by default"""
        async with AsyncClient(api_key=mock_api_key) as client:
            assert client.mock is False

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_with_schema(self, mock_api_key):
        """Test async mock mode works with Pydantic schemas"""
        class TestSchema(BaseModel):
            title: str
            price: float
        
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # Should not raise validation errors
            response = await client.smartscraper(
                user_prompt="Extract data",
                website_url="https://example.com",
                output_schema=TestSchema
            )
            assert "request_id" in response

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_preserves_logging(self, mock_api_key):
        """Test that async mock mode preserves logging behavior"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # This should complete without errors and log mock activity
            response = await client.markdownify("https://example.com")
            assert "request_id" in response

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_context_manager(self, mock_api_key):
        """Test async context manager works correctly with mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            assert client.mock is True
            response = await client.get_credits()
            assert response["remaining_credits"] == 1000
        
        # Client should be properly closed after context exit
        # Note: We can't easily test session closure without internal access

    @pytest.mark.asyncio
    async def test_async_client_mock_mode_multiple_calls(self, mock_api_key):
        """Test multiple async calls in mock mode"""
        async with AsyncClient(api_key=mock_api_key, mock=True) as client:
            # Multiple calls should all work and return consistent mock data
            credits1 = await client.get_credits()
            credits2 = await client.get_credits()
            
            assert credits1["remaining_credits"] == 1000
            assert credits2["remaining_credits"] == 1000
            
            # POST calls should return different UUIDs
            response1 = await client.smartscraper(
                user_prompt="Test 1", 
                website_url="https://example.com"
            )
            response2 = await client.smartscraper(
                user_prompt="Test 2", 
                website_url="https://example.com"
            )
            
            assert response1["request_id"] != response2["request_id"]
            assert response1["request_id"].startswith("mock-req-")
            assert response2["request_id"].startswith("mock-req-")
