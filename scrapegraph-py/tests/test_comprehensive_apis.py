from uuid import uuid4

import pytest
import responses
from pydantic import BaseModel

from scrapegraph_py.async_client import AsyncClient
from scrapegraph_py.client import Client
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


class TestSchema(BaseModel):
    """Test schema for output validation"""
    title: str
    description: str
    price: float


# ============================================================================
# SMART SCRAPER TESTS
# ============================================================================

@responses.activate
def test_smartscraper_basic_success(mock_api_key):
    """Test basic smartscraper with URL - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"title": "Test Page", "description": "Test content"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract title and description"
        )
        assert response["status"] == "completed"
        assert response["request_id"] == mock_request_id


@responses.activate
def test_smartscraper_with_html_success(mock_api_key):
    """Test smartscraper with HTML content - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"extracted_data": "Test data"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_html="<html><body><h1>Test</h1></body></html>",
            user_prompt="Extract data"
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_headers_success(mock_api_key):
    """Test smartscraper with custom headers - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"data": "Header test"}
        },
        status=200
    )

    headers = {"User-Agent": "Test Agent", "Cookie": "session=123"}
    
    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract data",
            headers=headers
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_cookies_success(mock_api_key):
    """Test smartscraper with cookies - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"data": "Cookie test"}
        },
        status=200
    )

    cookies = {"session": "abc123", "user": "test"}
    
    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract data",
            cookies=cookies
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_schema_success(mock_api_key):
    """Test smartscraper with output schema - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"title": "Test", "description": "Desc", "price": 99.99}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract product info",
            output_schema=TestSchema
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_scrolls_success(mock_api_key):
    """Test smartscraper with scrolls - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"scrolled_data": "Scroll test"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract data",
            number_of_scrolls=5
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_pagination_success(mock_api_key):
    """Test smartscraper with pagination - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"paginated_data": "Pagination test"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract data",
            total_pages=3
        )
        assert response["status"] == "completed"


@responses.activate
def test_get_smartscraper_success(mock_api_key, mock_uuid):
    """Test get smartscraper status - should return 200"""
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/smartscraper/{mock_uuid}",
        json={
            "request_id": mock_uuid,
            "status": "completed",
            "result": {"data": "Retrieved data"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_smartscraper(mock_uuid)
        assert response["status"] == "completed"
        assert response["request_id"] == mock_uuid


# ============================================================================
# SEARCH SCRAPER TESTS
# ============================================================================

@responses.activate
def test_searchscraper_basic_success(mock_api_key):
    """Test basic searchscraper - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"search_results": "Test results"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for products"
        )
        assert response["status"] == "completed"


@responses.activate
def test_searchscraper_with_num_results_success(mock_api_key):
    """Test searchscraper with num_results - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"results": ["result1", "result2", "result3"]}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for products",
            num_results=3
        )
        assert response["status"] == "completed"


@responses.activate
def test_searchscraper_with_headers_success(mock_api_key):
    """Test searchscraper with headers - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"results": "Header test results"}
        },
        status=200
    )

    headers = {"User-Agent": "Search Agent"}
    
    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for products",
            headers=headers
        )
        assert response["status"] == "completed"


@responses.activate
def test_searchscraper_with_schema_success(mock_api_key):
    """Test searchscraper with output schema - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"title": "Search Result", "description": "Desc", "price": 50.0}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for products",
            output_schema=TestSchema
        )
        assert response["status"] == "completed"


@responses.activate
def test_get_searchscraper_success(mock_api_key, mock_uuid):
    """Test get searchscraper status - should return 200"""
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/searchscraper/{mock_uuid}",
        json={
            "request_id": mock_uuid,
            "status": "completed",
            "result": {"search_data": "Retrieved search data"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_searchscraper(mock_uuid)
        assert response["status"] == "completed"
        assert response["request_id"] == mock_uuid


# ============================================================================
# MARKDOWNIFY TESTS
# ============================================================================

@responses.activate
def test_markdownify_basic_success(mock_api_key):
    """Test basic markdownify - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"markdown": "# Test Page\n\nThis is test content."}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.markdownify("https://example.com")
        assert response["status"] == "completed"


@responses.activate
def test_markdownify_with_headers_success(mock_api_key):
    """Test markdownify with headers - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"markdown": "# Header Test\n\nContent with headers."}
        },
        status=200
    )

    headers = {"User-Agent": "Markdown Agent"}
    
    with Client(api_key=mock_api_key) as client:
        response = client.markdownify(
            "https://example.com",
            headers=headers
        )
        assert response["status"] == "completed"


@responses.activate
def test_get_markdownify_success(mock_api_key, mock_uuid):
    """Test get markdownify status - should return 200"""
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/markdownify/{mock_uuid}",
        json={
            "request_id": mock_uuid,
            "status": "completed",
            "result": {"markdown": "# Retrieved Content\n\nMarkdown content."}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_markdownify(mock_uuid)
        assert response["status"] == "completed"
        assert response["request_id"] == mock_uuid


# ============================================================================
# CRAWL TESTS
# ============================================================================

@responses.activate
def test_crawl_basic_success(mock_api_key):
    """Test basic crawl - should return 200"""
    mock_crawl_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "crawl_id": mock_crawl_id,
            "status": "completed",
            "result": {"pages": ["page1", "page2"], "data": "Crawl data"}
        },
        status=200
    )

    data_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"}
        }
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract page data",
            data_schema=data_schema
        )
        assert response["status"] == "completed"


@responses.activate
def test_crawl_with_all_params_success(mock_api_key):
    """Test crawl with all parameters - should return 200"""
    mock_crawl_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "crawl_id": mock_crawl_id,
            "status": "completed",
            "result": {"pages": ["page1", "page2", "page3"], "data": "Full crawl data"}
        },
        status=200
    )

    data_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"}
        }
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract all page data",
            data_schema=data_schema,
            cache_website=True,
            depth=3,
            max_pages=5,
            same_domain_only=True,
            batch_size=10
        )
        assert response["status"] == "completed"


@responses.activate
def test_get_crawl_success(mock_api_key, mock_uuid):
    """Test get crawl status - should return 200"""
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/crawl/{mock_uuid}",
        json={
            "crawl_id": mock_uuid,
            "status": "completed",
            "result": {"pages": ["page1", "page2"], "data": "Retrieved crawl data"}
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_crawl(mock_uuid)
        assert response["status"] == "completed"
        assert response["crawl_id"] == mock_uuid


# ============================================================================
# CREDITS TESTS
# ============================================================================

@responses.activate
def test_get_credits_success(mock_api_key):
    """Test get credits - should return 200"""
    responses.add(
        responses.GET,
        "https://api.scrapegraphai.com/v1/credits",
        json={
            "credits": 1000,
            "used_credits": 150,
            "remaining_credits": 850
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_credits()
        assert response["credits"] == 1000
        assert response["used_credits"] == 150
        assert response["remaining_credits"] == 850


# ============================================================================
# FEEDBACK TESTS
# ============================================================================

@responses.activate
def test_submit_feedback_success(mock_api_key):
    """Test submit feedback - should return 200"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/feedback",
        json={
            "status": "success",
            "message": "Feedback submitted successfully"
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.submit_feedback(
            request_id=str(uuid4()),
            rating=5,
            feedback_text="Great service!"
        )
        assert response["status"] == "success"


@responses.activate
def test_submit_feedback_without_text_success(mock_api_key):
    """Test submit feedback without text - should return 200"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/feedback",
        json={
            "status": "success",
            "message": "Feedback submitted successfully"
        },
        status=200
    )

    with Client(api_key=mock_api_key) as client:
        response = client.submit_feedback(
            request_id=str(uuid4()),
            rating=4
        )
        assert response["status"] == "success"


# ============================================================================
# ASYNC CLIENT TESTS
# ============================================================================

@pytest.mark.asyncio
@responses.activate
async def test_async_smartscraper_success(mock_api_key):
    """Test async smartscraper - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"async_data": "Async test"}
        },
        status=200
    )

    async with AsyncClient(api_key=mock_api_key) as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract async data"
        )
        assert response["status"] == "completed"


@pytest.mark.asyncio
@responses.activate
async def test_async_searchscraper_success(mock_api_key):
    """Test async searchscraper - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"async_search": "Async search test"}
        },
        status=200
    )

    async with AsyncClient(api_key=mock_api_key) as client:
        response = await client.searchscraper(
            user_prompt="Async search"
        )
        assert response["status"] == "completed"


@pytest.mark.asyncio
@responses.activate
async def test_async_markdownify_success(mock_api_key):
    """Test async markdownify - should return 200"""
    mock_request_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": mock_request_id,
            "status": "completed",
            "result": {"markdown": "# Async Markdown\n\nAsync content."}
        },
        status=200
    )

    async with AsyncClient(api_key=mock_api_key) as client:
        response = await client.markdownify("https://example.com")
        assert response["status"] == "completed"


@pytest.mark.asyncio
@responses.activate
async def test_async_crawl_success(mock_api_key):
    """Test async crawl - should return 200"""
    mock_crawl_id = str(uuid4())
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "crawl_id": mock_crawl_id,
            "status": "completed",
            "result": {"async_pages": ["page1", "page2"], "data": "Async crawl data"}
        },
        status=200
    )

    data_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"}
        }
    }

    async with AsyncClient(api_key=mock_api_key) as client:
        response = await client.crawl(
            url="https://example.com",
            prompt="Extract async data",
            data_schema=data_schema
        )
        assert response["status"] == "completed"


@pytest.mark.asyncio
@responses.activate
async def test_async_get_credits_success(mock_api_key):
    """Test async get credits - should return 200"""
    responses.add(
        responses.GET,
        "https://api.scrapegraphai.com/v1/credits",
        json={
            "credits": 2000,
            "used_credits": 300,
            "remaining_credits": 1700
        },
        status=200
    )

    async with AsyncClient(api_key=mock_api_key) as client:
        response = await client.get_credits()
        assert response["credits"] == 2000
        assert response["used_credits"] == 300
        assert response["remaining_credits"] == 1700


@pytest.mark.asyncio
@responses.activate
async def test_async_submit_feedback_success(mock_api_key):
    """Test async submit feedback - should return 200"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/feedback",
        json={
            "status": "success",
            "message": "Async feedback submitted successfully"
        },
        status=200
    )

    async with AsyncClient(api_key=mock_api_key) as client:
        response = await client.submit_feedback(
            request_id=str(uuid4()),
            rating=5,
            feedback_text="Async great service!"
        )
        assert response["status"] == "success"


# ============================================================================
# CLIENT INITIALIZATION TESTS
# ============================================================================

def test_client_from_env_success(mock_api_key, monkeypatch):
    """Test client initialization from environment - should work"""
    monkeypatch.setenv("SGAI_API_KEY", mock_api_key)
    
    client = Client.from_env()
    assert client.api_key == mock_api_key


def test_async_client_from_env_success(mock_api_key, monkeypatch):
    """Test async client initialization from environment - should work"""
    monkeypatch.setenv("SGAI_API_KEY", mock_api_key)
    
    client = AsyncClient.from_env()
    assert client.api_key == mock_api_key


def test_client_context_manager_success(mock_api_key):
    """Test client context manager - should work properly"""
    with Client(api_key=mock_api_key) as client:
        assert client.api_key == mock_api_key
        # Session should be created
        assert hasattr(client, 'session')


@pytest.mark.asyncio
async def test_async_client_context_manager_success(mock_api_key):
    """Test async client context manager - should work properly"""
    async with AsyncClient(api_key=mock_api_key) as client:
        assert client.api_key == mock_api_key
        # Session should be created
        assert hasattr(client, 'session')


# ============================================================================
# ERROR HANDLING TESTS (Still return 200 but test error scenarios)
# ============================================================================

@responses.activate
def test_invalid_api_key_handling(mock_api_key):
    """Test handling of invalid API key - should handle gracefully"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "error": "Invalid API key",
            "status": "error"
        },
        status=200  # API returns 200 even for auth errors
    )

    with Client(api_key="invalid-key") as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Test"
        )
        # Should still return 200 status from API
        assert "status" in response


@responses.activate
def test_rate_limit_handling(mock_api_key):
    """Test handling of rate limiting - should handle gracefully"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "error": "Rate limit exceeded",
            "status": "error",
            "retry_after": 60
        },
        status=200  # API returns 200 even for rate limit errors
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Test"
        )
        # Should still return 200 status from API
        assert "status" in response


@responses.activate
def test_invalid_request_handling(mock_api_key):
    """Test handling of invalid request - should handle gracefully"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "error": "Invalid request parameters",
            "status": "error"
        },
        status=200  # API returns 200 even for validation errors
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="",  # Invalid URL
            user_prompt=""   # Invalid prompt
        )
        # Should still return 200 status from API
        assert "status" in response 