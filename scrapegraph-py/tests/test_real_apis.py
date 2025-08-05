#!/usr/bin/env python3
"""
Real API Tests for ScrapeGraph Python SDK
These tests use actual API calls with environment variables
"""

import asyncio
import os

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


# ============================================================================
# SYNC CLIENT TESTS
# ============================================================================

def test_smartscraper_basic_real():
    """Test basic smartscraper with real API call"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract the title and description of this page"
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_smartscraper_with_schema_real():
    """Test smartscraper with output schema"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract company information",
            output_schema=CompanySchema
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_smartscraper_with_headers_real():
    """Test smartscraper with custom headers"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    with Client.from_env() as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract page information",
            headers=headers
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_smartscraper_with_cookies_real():
    """Test smartscraper with cookies"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    cookies = {"session": "test123", "user": "testuser"}
    
    with Client.from_env() as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract page information",
            cookies=cookies
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_smartscraper_with_scrolls_real():
    """Test smartscraper with infinite scrolling"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract all content with scrolling",
            number_of_scrolls=3
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_smartscraper_with_pagination_real():
    """Test smartscraper with pagination"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract all pages",
            total_pages=2
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_get_smartscraper_status_real():
    """Test getting smartscraper status"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        # First create a request
        initial_response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract basic information"
        )
        
        request_id = initial_response["request_id"]
        
        # Then get the status
        status_response = client.get_smartscraper(request_id)
        assert "status" in status_response
        assert "request_id" in status_response


def test_searchscraper_basic_real():
    """Test basic searchscraper"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.searchscraper(
            user_prompt="Search for Python programming tutorials"
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_searchscraper_with_num_results_real():
    """Test searchscraper with custom number of results"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.searchscraper(
            user_prompt="Search for web scraping tools",
            num_results=5
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_searchscraper_with_schema_real():
    """Test searchscraper with output schema"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.searchscraper(
            user_prompt="Search for products",
            output_schema=ProductSchema
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_get_searchscraper_status_real():
    """Test getting searchscraper status"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        # First create a search request
        initial_response = client.searchscraper(
            user_prompt="Search for AI tools"
        )
        
        request_id = initial_response["request_id"]
        
        # Then get the status
        status_response = client.get_searchscraper(request_id)
        assert "status" in status_response
        assert "request_id" in status_response


def test_markdownify_basic_real():
    """Test basic markdownify"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        response = client.markdownify("https://example.com")
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_markdownify_with_headers_real():
    """Test markdownify with custom headers"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    headers = {"User-Agent": "MarkdownBot/1.0"}
    
    with Client.from_env() as client:
        response = client.markdownify(
            "https://example.com",
            headers=headers
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


def test_get_markdownify_status_real():
    """Test getting markdownify status"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        # First create a markdownify request
        initial_response = client.markdownify("https://example.com")
        
        request_id = initial_response["request_id"]
        
        # Then get the status
        status_response = client.get_markdownify(request_id)
        assert "status" in status_response
        assert "request_id" in status_response


    """Test submitting feedback without text"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        # First create a request to get a request_id
        initial_response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract basic info"
        )
        
        request_id = initial_response["request_id"]
        
        # Submit feedback without text
        feedback_response = client.submit_feedback(
            request_id=request_id,
            rating=4
        )
        assert "status" in feedback_response


# ============================================================================
# ASYNC CLIENT TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_async_smartscraper_basic_real():
    """Test basic async smartscraper"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    async with AsyncClient.from_env() as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract async page information"
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


@pytest.mark.asyncio
async def test_async_smartscraper_with_schema_real():
    """Test async smartscraper with output schema"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    async with AsyncClient.from_env() as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract company data",
            output_schema=CompanySchema
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


@pytest.mark.asyncio
async def test_async_searchscraper_basic_real():
    """Test basic async searchscraper"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    async with AsyncClient.from_env() as client:
        response = await client.searchscraper(
            user_prompt="Search for async programming tutorials"
        )
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response


@pytest.mark.asyncio
async def test_async_markdownify_basic_real():
    """Test basic async markdownify"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    async with AsyncClient.from_env() as client:
        response = await client.markdownify("https://example.com")
        assert response["status"] in ["completed", "processing", "pending"]
        assert "request_id" in response




# ============================================================================
# CLIENT INITIALIZATION TESTS
# ============================================================================


def test_client_context_manager_real():
    """Test client context manager"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        assert client.api_key == os.getenv("SGAI_API_KEY")
        assert hasattr(client, 'session')


@pytest.mark.asyncio
async def test_async_client_context_manager_real():
    """Test async client context manager"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    async with AsyncClient.from_env() as client:
        assert client.api_key == os.getenv("SGAI_API_KEY")
        assert hasattr(client, 'session')


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================


def test_missing_api_key_handling():
    """Test handling of missing API key"""
    # Temporarily remove API key
    original_key = os.getenv("SGAI_API_KEY")
    if original_key:
        del os.environ["SGAI_API_KEY"]
    
    try:
        with pytest.raises(ValueError, match="SGAI_API_KEY"):
            Client.from_env()
    finally:
        # Restore original key
        if original_key:
            os.environ["SGAI_API_KEY"] = original_key


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

def test_concurrent_requests_real():
    """Test multiple concurrent requests"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    with Client.from_env() as client:
        # Make multiple requests
        responses = []
        for i in range(3):
            response = client.smartscraper(
                website_url="https://example.com",
                user_prompt=f"Extract info {i}"
            )
            responses.append(response)
        
        # All should have request_ids
        for response in responses:
            assert "request_id" in response
            assert response["status"] in ["completed", "processing", "pending"]


@pytest.mark.asyncio
async def test_async_concurrent_requests_real():
    """Test multiple async concurrent requests"""
    if not os.getenv("SGAI_API_KEY"):
        pytest.skip("SGAI_API_KEY not set")
    
    async with AsyncClient.from_env() as client:
        # Make multiple concurrent requests
        tasks = []
        for i in range(3):
            task = client.smartscraper(
                website_url="https://example.com",
                user_prompt=f"Extract async info {i}"
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # All should have request_ids
        for response in responses:
            assert "request_id" in response
            assert response["status"] in ["completed", "processing", "pending"] 