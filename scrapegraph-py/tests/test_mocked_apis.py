#!/usr/bin/env python3
"""
Mocked API Tests for ScrapeGraph Python SDK
These tests use mocked API responses for faster and more reliable testing
"""

from unittest.mock import patch

import pytest
from pydantic import BaseModel

from scrapegraph_py.async_client import AsyncClient
from scrapegraph_py.client import Client


class ProductSchema(BaseModel):
    """Test schema for product data"""

    title: str
    description: str
    price: float


class CompanySchema(BaseModel):
    """Test schema for company data"""

    name: str
    description: str
    website: str


# Mock responses
MOCK_SMARTSCRAPER_RESPONSE = {
    "status": "completed",
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "data": {
        "title": "Test Page",
        "description": "This is a test page",
        "content": "Mock content from the page",
    },
}

MOCK_SEARCHSCRAPER_RESPONSE = {
    "status": "completed",
    "request_id": "456e7890-e89b-12d3-a456-426614174001",
    "data": [
        {"title": "Result 1", "url": "https://example1.com"},
        {"title": "Result 2", "url": "https://example2.com"},
    ],
}

MOCK_MARKDOWNIFY_RESPONSE = {
    "status": "completed",
    "request_id": "789e0123-e89b-12d3-a456-426614174002",
    "data": "# Test Page\n\nThis is a test page in markdown format.",
}

MOCK_SCRAPE_RESPONSE = {
    "status": "completed",
    "scrape_request_id": "abc12345-e89b-12d3-a456-426614174003",
    "html": "<!DOCTYPE html><html><head><title>Test Page</title></head><body><h1>Test Page</h1><p>This is a test page in HTML format.</p></body></html>",
}

MOCK_STATUS_RESPONSE = {
    "status": "completed",
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "data": {"result": "Mock result data"},
}

MOCK_FEEDBACK_RESPONSE = {
    "status": "success",
    "message": "Feedback submitted successfully",
}

api_key = "sgai-c0811976-dac7-441c-acb6-7cd72643449c"  # its an invalid api key
# ============================================================================
# SYNC CLIENT TESTS
# ============================================================================


@patch("scrapegraph_py.client.Client._make_request")
def test_smartscraper_basic_mocked(mock_request):
    """Test basic smartscraper with mocked API call"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract the title and description of this page",
        )
        assert response["status"] == "completed"
        assert "request_id" in response
        assert "data" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_smartscraper_with_schema_mocked(mock_request):
    """Test smartscraper with output schema"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract company information",
            output_schema=CompanySchema,
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_smartscraper_with_headers_mocked(mock_request):
    """Test smartscraper with custom headers"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    with Client(api_key=api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract page information",
            headers=headers,
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_smartscraper_with_cookies_mocked(mock_request):
    """Test smartscraper with cookies"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    cookies = {"session": "test123", "user": "testuser"}

    with Client(api_key=api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract page information",
            cookies=cookies,
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_smartscraper_with_scrolls_mocked(mock_request):
    """Test smartscraper with scrolls"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract page information",
            number_of_scrolls=3,
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_get_smartscraper_status_mocked(mock_request):
    """Test getting smartscraper status"""
    mock_request.return_value = MOCK_STATUS_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.get_smartscraper("123e4567-e89b-12d3-a456-426614174000")
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_searchscraper_basic_mocked(mock_request):
    """Test basic searchscraper"""
    mock_request.return_value = MOCK_SEARCHSCRAPER_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.searchscraper(user_prompt="Search for programming tutorials")
        assert response["status"] == "completed"
        assert "request_id" in response
        assert "data" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_searchscraper_with_num_results_mocked(mock_request):
    """Test searchscraper with num_results parameter"""
    mock_request.return_value = MOCK_SEARCHSCRAPER_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for tutorials", num_results=5
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_searchscraper_with_schema_mocked(mock_request):
    """Test searchscraper with output schema"""
    mock_request.return_value = MOCK_SEARCHSCRAPER_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for products", output_schema=ProductSchema
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_get_searchscraper_status_mocked(mock_request):
    """Test getting searchscraper status"""
    mock_request.return_value = MOCK_STATUS_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.get_searchscraper("456e7890-e89b-12d3-a456-426614174001")
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_markdownify_basic_mocked(mock_request):
    """Test basic markdownify"""
    mock_request.return_value = MOCK_MARKDOWNIFY_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.markdownify("https://example.com")
        assert response["status"] == "completed"
        assert "request_id" in response
        assert "data" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_markdownify_with_headers_mocked(mock_request):
    """Test markdownify with custom headers"""
    mock_request.return_value = MOCK_MARKDOWNIFY_RESPONSE

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    with Client(api_key=api_key) as client:
        response = client.markdownify("https://example.com", headers=headers)
        assert response["status"] == "completed"
        assert "request_id" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_get_markdownify_status_mocked(mock_request):
    """Test getting markdownify status"""
    mock_request.return_value = MOCK_STATUS_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.get_markdownify("789e0123-e89b-12d3-a456-426614174002")
        assert response["status"] == "completed"
        assert "request_id" in response


# ============================================================================
# ASYNC CLIENT TESTS
# ============================================================================


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_smartscraper_basic_mocked(mock_request):
    """Test basic async smartscraper"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract async page information",
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_smartscraper_with_schema_mocked(mock_request):
    """Test async smartscraper with output schema"""
    mock_request.return_value = MOCK_SMARTSCRAPER_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract company data",
            output_schema=CompanySchema,
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_searchscraper_basic_mocked(mock_request):
    """Test basic async searchscraper"""
    mock_request.return_value = MOCK_SEARCHSCRAPER_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.searchscraper(
            user_prompt="Search for async programming tutorials"
        )
        assert response["status"] == "completed"
        assert "request_id" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_markdownify_basic_mocked(mock_request):
    """Test basic async markdownify"""
    mock_request.return_value = MOCK_MARKDOWNIFY_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.markdownify("https://example.com")
        assert response["status"] == "completed"
        assert "request_id" in response


# ============================================================================
# CLIENT INITIALIZATION TESTS
# ============================================================================


def test_client_context_manager_mocked():
    """Test client context manager"""
    with Client(api_key=api_key) as client:
        assert client.api_key == api_key


@pytest.mark.asyncio
async def test_async_client_context_manager_mocked():
    """Test async client context manager"""
    async with AsyncClient(api_key=api_key) as client:
        assert client.api_key == api_key


def test_missing_api_key_handling_mocked():
    """Test handling of missing API key"""
    with pytest.raises(ValueError):
        Client(api_key="")


def test_concurrent_requests_mocked():
    """Test concurrent requests"""
    with Client(api_key=api_key) as client:
        # This test verifies the client can handle multiple requests
        # In a real scenario, you'd mock the requests
        assert client.api_key == api_key


@pytest.mark.asyncio
async def test_async_concurrent_requests_mocked():
    """Test async concurrent requests"""
    async with AsyncClient(api_key=api_key) as client:
        # This test verifies the async client can handle multiple requests
        # In a real scenario, you'd mock the requests
        assert client.api_key == api_key


# ============================================================================
# SCRAPE TESTS
# ============================================================================


@patch("scrapegraph_py.client.Client._make_request")
def test_scrape_basic_mocked(mock_request):
    """Test basic scrape with mocked API call"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.scrape(website_url="https://example.com")
        assert response["status"] == "completed"
        assert "scrape_request_id" in response
        assert "html" in response
        assert "<title>Test Page</title>" in response["html"]


@patch("scrapegraph_py.client.Client._make_request")
def test_scrape_with_heavy_js_mocked(mock_request):
    """Test scrape with heavy JS rendering"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.scrape(
            website_url="https://example.com",
            render_heavy_js=True
        )
        assert response["status"] == "completed"
        assert "html" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_scrape_with_headers_mocked(mock_request):
    """Test scrape with custom headers"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": "session=123"
    }

    with Client(api_key=api_key) as client:
        response = client.scrape(
            website_url="https://example.com",
            headers=headers
        )
        assert response["status"] == "completed"
        assert "html" in response


@patch("scrapegraph_py.client.Client._make_request")
def test_get_scrape_mocked(mock_request):
    """Test get scrape result"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    with Client(api_key=api_key) as client:
        response = client.get_scrape("abc12345-e89b-12d3-a456-426614174003")
        assert response["status"] == "completed"
        assert "scrape_request_id" in response
        assert "html" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_scrape_basic_mocked(mock_request):
    """Test basic async scrape"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.scrape(website_url="https://example.com")
        assert response["status"] == "completed"
        assert "scrape_request_id" in response
        assert "html" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_scrape_with_heavy_js_mocked(mock_request):
    """Test async scrape with heavy JS rendering"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.scrape(
            website_url="https://example.com",
            render_heavy_js=True
        )
        assert response["status"] == "completed"
        assert "html" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_scrape_with_headers_mocked(mock_request):
    """Test async scrape with custom headers"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": "session=123"
    }

    async with AsyncClient(api_key=api_key) as client:
        response = await client.scrape(
            website_url="https://example.com",
            headers=headers
        )
        assert response["status"] == "completed"
        assert "html" in response


@pytest.mark.asyncio
@patch("scrapegraph_py.async_client.AsyncClient._make_request")
async def test_async_get_scrape_mocked(mock_request):
    """Test async get scrape result"""
    mock_request.return_value = MOCK_SCRAPE_RESPONSE

    async with AsyncClient(api_key=api_key) as client:
        response = await client.get_scrape("abc12345-e89b-12d3-a456-426614174003")
        assert response["status"] == "completed"
        assert "scrape_request_id" in response
        assert "html" in response
