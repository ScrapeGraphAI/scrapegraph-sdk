"""
Tests for Client mock mode functionality
"""
import os
from unittest.mock import patch
from uuid import uuid4

import pytest
from pydantic import BaseModel

from scrapegraph_py.client import Client
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


class TestMockMode:
    """Test basic mock mode functionality"""

    def test_client_mock_mode_basic(self, mock_api_key):
        """Test that mock mode bypasses HTTP calls and returns stub data"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # Test credits endpoint
        credits = client.get_credits()
        assert credits["remaining_credits"] == 1000
        assert credits["total_credits_used"] == 0
        
        # Test smartscraper POST endpoint
        response = client.smartscraper(
            user_prompt="Extract title", 
            website_url="https://example.com"
        )
        assert "request_id" in response
        assert response["request_id"].startswith("mock-req-")
        
        # Test feedback endpoint
        feedback = client.submit_feedback("test-id", 5, "Great!")
        assert feedback["status"] == "success"

    def test_client_mock_mode_get_endpoints(self, mock_api_key, mock_uuid):
        """Test GET endpoints in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # Test markdownify GET
        md_result = client.get_markdownify(mock_uuid)
        assert md_result["status"] == "completed"
        assert "Mock markdown" in md_result["content"]
        
        # Test smartscraper GET
        ss_result = client.get_smartscraper(mock_uuid)
        assert ss_result["status"] == "completed"
        assert "result" in ss_result
        
        # Test searchscraper GET
        search_result = client.get_searchscraper(mock_uuid)
        assert search_result["status"] == "completed"
        assert "results" in search_result

    def test_client_mock_mode_crawl_endpoints(self, mock_api_key, mock_uuid):
        """Test crawl-specific endpoints in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # Test crawl POST
        crawl_response = client.crawl(url="https://example.com")
        assert "crawl_id" in crawl_response
        assert crawl_response["crawl_id"].startswith("mock-crawl-")
        
        # Test crawl GET
        crawl_result = client.get_crawl(mock_uuid)
        assert crawl_result["status"] == "completed"
        assert "pages" in crawl_result

    def test_client_mock_mode_agentic_scraper(self, mock_api_key, mock_uuid):
        """Test agentic scraper endpoints in mock mode"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # Test agentic scraper POST
        response = client.agenticscraper(
            url="https://example.com",
            steps=["click button", "extract data"]
        )
        assert "request_id" in response
        assert response["request_id"].startswith("mock-req-")
        
        # Test agentic scraper GET
        result = client.get_agenticscraper(mock_uuid)
        assert result["status"] == "completed"
        assert "actions" in result


class TestMockModeCustomization:
    """Test mock mode customization features"""

    def test_client_mock_responses_override(self, mock_api_key):
        """Test custom mock responses via mock_responses parameter"""
        custom_responses = {
            "/v1/credits": {"remaining_credits": 42, "total_credits_used": 58}
        }
        
        client = Client(
            api_key=mock_api_key, 
            mock=True, 
            mock_responses=custom_responses
        )
        
        credits = client.get_credits()
        assert credits["remaining_credits"] == 42
        assert credits["total_credits_used"] == 58

    def test_client_mock_responses_callable(self, mock_api_key):
        """Test custom mock responses with callable values"""
        def dynamic_credits():
            return {"remaining_credits": 123, "custom_field": "dynamic"}
        
        custom_responses = {
            "/v1/credits": dynamic_credits
        }
        
        client = Client(
            api_key=mock_api_key, 
            mock=True, 
            mock_responses=custom_responses
        )
        
        credits = client.get_credits()
        assert credits["remaining_credits"] == 123
        assert credits["custom_field"] == "dynamic"

    def test_client_mock_handler_override(self, mock_api_key):
        """Test custom mock handler"""
        def custom_handler(method, url, kwargs):
            return {
                "custom_handler": True,
                "method": method,
                "url": url,
                "has_kwargs": bool(kwargs)
            }
        
        client = Client(
            api_key=mock_api_key, 
            mock=True, 
            mock_handler=custom_handler
        )
        
        response = client.get_credits()
        assert response["custom_handler"] is True
        assert response["method"] == "GET"
        assert "credits" in response["url"]

    def test_client_mock_handler_fallback(self, mock_api_key):
        """Test that mock handler exceptions fall back to defaults"""
        def failing_handler(method, url, kwargs):
            raise ValueError("Handler failed")
        
        client = Client(
            api_key=mock_api_key, 
            mock=True, 
            mock_handler=failing_handler
        )
        
        # Should fall back to default mock response
        response = client.get_credits()
        assert response["remaining_credits"] == 1000


class TestMockModeEnvironment:
    """Test mock mode environment variable support"""

    def test_client_from_env_with_mock_flag(self, mock_api_key):
        """Test Client.from_env with explicit mock=True"""
        with patch.dict(os.environ, {"SGAI_API_KEY": mock_api_key}):
            client = Client.from_env(mock=True)
            assert client.mock is True
            
            response = client.get_credits()
            assert response["remaining_credits"] == 1000

    def test_client_from_env_without_api_key_mock_mode(self):
        """Test Client.from_env in mock mode without SGAI_API_KEY set"""
        with patch.dict(os.environ, {}, clear=True):
            # Should work in mock mode even without API key
            client = Client.from_env(mock=True)
            assert client.mock is True
            assert client.api_key == "sgai-00000000-0000-0000-0000-000000000000"
            
            response = client.get_credits()
            assert response["remaining_credits"] == 1000

    def test_client_from_env_sgai_mock_environment(self):
        """Test SGAI_MOCK environment variable activation"""
        test_cases = ["1", "true", "True", "TRUE", "yes", "YES", "on", "ON"]
        
        for mock_value in test_cases:
            with patch.dict(os.environ, {"SGAI_MOCK": mock_value}, clear=True):
                client = Client.from_env()
                assert client.mock is True, f"Failed for SGAI_MOCK={mock_value}"

    def test_client_from_env_sgai_mock_disabled(self):
        """Test SGAI_MOCK environment variable disabled states"""
        test_cases = ["0", "false", "False", "FALSE", "no", "NO", "off", "OFF", ""]
        
        for mock_value in test_cases:
            with patch.dict(os.environ, {"SGAI_MOCK": mock_value}, clear=True):
                try:
                    client = Client.from_env()
                    # If no exception, mock should be False
                    assert client.mock is False, f"Failed for SGAI_MOCK={mock_value}"
                except ValueError as e:
                    # Expected when no API key is set and mock is disabled
                    assert "SGAI_API_KEY environment variable not set" in str(e)

    def test_client_from_env_with_custom_responses(self, mock_api_key):
        """Test Client.from_env with mock_responses parameter"""
        custom_responses = {
            "/v1/credits": {"remaining_credits": 999}
        }
        
        with patch.dict(os.environ, {"SGAI_API_KEY": mock_api_key}):
            client = Client.from_env(mock=True, mock_responses=custom_responses)
            
            response = client.get_credits()
            assert response["remaining_credits"] == 999

    def test_client_from_env_with_custom_handler(self, mock_api_key):
        """Test Client.from_env with mock_handler parameter"""
        def custom_handler(method, url, kwargs):
            return {"from_env": True, "method": method}
        
        with patch.dict(os.environ, {"SGAI_API_KEY": mock_api_key}):
            client = Client.from_env(mock=True, mock_handler=custom_handler)
            
            response = client.get_credits()
            assert response["from_env"] is True
            assert response["method"] == "GET"


class TestMockModeValidation:
    """Test mock mode validation and edge cases"""

    def test_client_mock_mode_disabled_by_default(self, mock_api_key):
        """Test that mock mode is disabled by default"""
        client = Client(api_key=mock_api_key)
        assert client.mock is False

    def test_client_mock_mode_with_schema(self, mock_api_key):
        """Test mock mode works with Pydantic schemas"""
        class TestSchema(BaseModel):
            title: str
            price: float
        
        client = Client(api_key=mock_api_key, mock=True)
        
        # Should not raise validation errors
        response = client.smartscraper(
            user_prompt="Extract data",
            website_url="https://example.com",
            output_schema=TestSchema
        )
        assert "request_id" in response

    def test_client_mock_mode_preserves_logging(self, mock_api_key):
        """Test that mock mode preserves logging behavior"""
        client = Client(api_key=mock_api_key, mock=True)
        
        # This should complete without errors and log mock activity
        response = client.markdownify("https://example.com")
        assert "request_id" in response
