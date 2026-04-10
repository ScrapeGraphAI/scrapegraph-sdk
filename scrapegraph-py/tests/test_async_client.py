"""Tests for the asynchronous AsyncClient (v2 API)."""

from uuid import uuid4

import pytest
import pytest_asyncio
from aioresponses import aioresponses
from pydantic import BaseModel, Field

from scrapegraph_py.async_client import AsyncClient
from scrapegraph_py.config import API_BASE_URL
from tests.utils import generate_mock_api_key


@pytest.fixture
def api_key():
    return generate_mock_api_key()


@pytest_asyncio.fixture
async def client(api_key):
    c = AsyncClient(api_key=api_key)
    yield c
    await c.close()


# ------------------------------------------------------------------
# Auth & headers
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_bearer_auth_header(api_key):
    c = AsyncClient(api_key=api_key)
    assert c.headers["Authorization"] == f"Bearer {api_key}"
    assert c.headers["X-SDK-Version"].startswith("python@")
    await c.close()


# ------------------------------------------------------------------
# Scrape
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_scrape(client):
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/scrape",
            payload={"request_id": str(uuid4()), "content": "# Hello"},
        )
        result = await client.scrape("https://example.com")
        assert "content" in result


@pytest.mark.asyncio
async def test_scrape_html_format(client):
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/scrape",
            payload={"request_id": str(uuid4()), "content": "<h1>Hello</h1>"},
        )
        result = await client.scrape("https://example.com", format="html")
        assert "content" in result


# ------------------------------------------------------------------
# Extract
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_extract(client):
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/extract",
            payload={"request_id": str(uuid4()), "result": {"title": "Example"}},
        )
        result = await client.extract(
            url="https://example.com",
            prompt="Extract the title",
        )
        assert result["result"]["title"] == "Example"


@pytest.mark.asyncio
async def test_extract_with_pydantic_schema(client):
    class Product(BaseModel):
        name: str = Field(description="Product name")
        price: float = Field(description="Product price")

    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/extract",
            payload={
                "request_id": str(uuid4()),
                "result": {"name": "Widget", "price": 9.99},
            },
        )
        result = await client.extract(
            url="https://example.com",
            prompt="Extract product info",
            output_schema=Product,
        )
        assert result["result"]["name"] == "Widget"


# ------------------------------------------------------------------
# Search
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_search(client):
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/search",
            payload={
                "request_id": str(uuid4()),
                "results": [{"url": "https://example.com"}],
            },
        )
        result = await client.search("best web scrapers 2025")
        assert "results" in result


@pytest.mark.asyncio
async def test_search_with_location_geo_code(client):
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/search",
            payload={
                "request_id": str(uuid4()),
                "results": [{"url": "https://example.it"}],
            },
        )
        result = await client.search("best restaurants", location_geo_code="it")
        assert "results" in result


# ------------------------------------------------------------------
# Credits
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_credits(client):
    with aioresponses() as mocked:
        mocked.get(
            f"{API_BASE_URL}/credits",
            payload={"remaining_credits": 1000, "total_credits_used": 50},
        )
        result = await client.credits()
        assert result["remaining_credits"] == 1000


# ------------------------------------------------------------------
# History
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_history(client):
    with aioresponses() as mocked:
        mocked.get(
            f"{API_BASE_URL}/history",
            payload={"requests": [], "total": 0},
        )
        result = await client.history()
        assert "requests" in result


# ------------------------------------------------------------------
# Crawl namespace
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_crawl_start(client):
    crawl_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/crawl",
            payload={"id": crawl_id, "status": "running"},
        )
        result = await client.crawl.start("https://example.com", depth=3)
        assert result["id"] == crawl_id


@pytest.mark.asyncio
async def test_crawl_status(client):
    crawl_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.get(
            f"{API_BASE_URL}/crawl/{crawl_id}",
            payload={"id": crawl_id, "status": "completed", "pages": []},
        )
        result = await client.crawl.status(crawl_id)
        assert result["status"] == "completed"


@pytest.mark.asyncio
async def test_crawl_stop(client):
    crawl_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/crawl/{crawl_id}/stop",
            payload={"id": crawl_id, "status": "stopped"},
        )
        result = await client.crawl.stop(crawl_id)
        assert result["status"] == "stopped"


@pytest.mark.asyncio
async def test_crawl_resume(client):
    crawl_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/crawl/{crawl_id}/resume",
            payload={"id": crawl_id, "status": "running"},
        )
        result = await client.crawl.resume(crawl_id)
        assert result["status"] == "running"


# ------------------------------------------------------------------
# Monitor namespace
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_monitor_create(client):
    monitor_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/monitor",
            payload={"id": monitor_id, "name": "Price Monitor"},
        )
        result = await client.monitor.create(
            name="Price Monitor",
            url="https://example.com/products",
            prompt="Extract product prices",
            interval="0 9 * * 1",
        )
        assert result["name"] == "Price Monitor"


@pytest.mark.asyncio
async def test_monitor_list(client):
    with aioresponses() as mocked:
        mocked.get(
            f"{API_BASE_URL}/monitor",
            payload={"monitors": [], "total": 0},
        )
        result = await client.monitor.list()
        assert "monitors" in result


@pytest.mark.asyncio
async def test_monitor_get(client):
    monitor_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.get(
            f"{API_BASE_URL}/monitor/{monitor_id}",
            payload={"id": monitor_id, "name": "Test Monitor"},
        )
        result = await client.monitor.get(monitor_id)
        assert result["id"] == monitor_id


@pytest.mark.asyncio
async def test_monitor_pause(client):
    monitor_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/monitor/{monitor_id}/pause",
            payload={"id": monitor_id, "status": "paused"},
        )
        result = await client.monitor.pause(monitor_id)
        assert result["status"] == "paused"


@pytest.mark.asyncio
async def test_monitor_resume(client):
    monitor_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/monitor/{monitor_id}/resume",
            payload={"id": monitor_id, "status": "active"},
        )
        result = await client.monitor.resume(monitor_id)
        assert result["status"] == "active"


@pytest.mark.asyncio
async def test_monitor_delete(client):
    monitor_id = str(uuid4())
    with aioresponses() as mocked:
        mocked.delete(
            f"{API_BASE_URL}/monitor/{monitor_id}",
            payload={"message": "deleted"},
        )
        result = await client.monitor.delete(monitor_id)
        assert result["message"] == "deleted"


# ------------------------------------------------------------------
# Error handling
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_api_error_handling(client):
    from scrapegraph_py.exceptions import APIError

    with aioresponses() as mocked:
        mocked.post(
            f"{API_BASE_URL}/scrape",
            payload={"error": "Invalid URL"},
            status=400,
        )
        with pytest.raises(APIError) as exc_info:
            await client.scrape("https://example.com")
        assert exc_info.value.status_code == 400


# ------------------------------------------------------------------
# Context manager
# ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_context_manager(api_key):
    with aioresponses() as mocked:
        mocked.get(
            f"{API_BASE_URL}/credits",
            payload={"remaining_credits": 500},
        )
        async with AsyncClient(api_key=api_key) as client:
            result = await client.credits()
            assert result["remaining_credits"] == 500
