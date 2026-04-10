"""Tests for the synchronous Client (v2 API)."""

from uuid import uuid4

import pytest
import responses
from pydantic import BaseModel, Field

from scrapegraph_py.client import Client
from scrapegraph_py.config import API_BASE_URL
from tests.utils import generate_mock_api_key


@pytest.fixture
def api_key():
    return generate_mock_api_key()


@pytest.fixture
def client(api_key):
    c = Client(api_key=api_key)
    yield c
    c.close()


# ------------------------------------------------------------------
# Auth & headers
# ------------------------------------------------------------------


def test_bearer_auth_header(api_key):
    c = Client(api_key=api_key)
    assert c.headers["Authorization"] == f"Bearer {api_key}"
    assert "X-SDK-Version" in c.headers
    assert c.headers["X-SDK-Version"].startswith("python@")
    c.close()


def test_missing_api_key_raises():
    import os

    old = os.environ.pop("SGAI_API_KEY", None)
    try:
        with pytest.raises(ValueError):
            Client()
    finally:
        if old is not None:
            os.environ["SGAI_API_KEY"] = old


# ------------------------------------------------------------------
# Scrape
# ------------------------------------------------------------------


@responses.activate
def test_scrape(client):
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/scrape",
        json={"request_id": str(uuid4()), "content": "# Hello"},
    )
    result = client.scrape("https://example.com")
    assert "content" in result


@responses.activate
def test_scrape_html_format(client):
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/scrape",
        json={"request_id": str(uuid4()), "content": "<h1>Hello</h1>"},
    )
    result = client.scrape("https://example.com", format="html")
    assert "content" in result


# ------------------------------------------------------------------
# Extract
# ------------------------------------------------------------------


@responses.activate
def test_extract(client):
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/extract",
        json={"request_id": str(uuid4()), "result": {"title": "Example"}},
    )
    result = client.extract(
        url="https://example.com",
        prompt="Extract the title",
    )
    assert result["result"]["title"] == "Example"


@responses.activate
def test_extract_with_pydantic_schema(client):
    class Product(BaseModel):
        name: str = Field(description="Product name")
        price: float = Field(description="Product price")

    responses.add(
        responses.POST,
        f"{API_BASE_URL}/extract",
        json={"request_id": str(uuid4()), "result": {"name": "Widget", "price": 9.99}},
    )
    result = client.extract(
        url="https://example.com",
        prompt="Extract product info",
        output_schema=Product,
    )
    assert result["result"]["name"] == "Widget"


@responses.activate
def test_extract_with_dict_schema(client):
    schema = {
        "type": "object",
        "properties": {"title": {"type": "string"}},
    }
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/extract",
        json={"request_id": str(uuid4()), "result": {"title": "Test"}},
    )
    result = client.extract(
        url="https://example.com",
        prompt="Extract title",
        output_schema=schema,
    )
    assert result["result"]["title"] == "Test"


# ------------------------------------------------------------------
# Search
# ------------------------------------------------------------------


@responses.activate
def test_search(client):
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/search",
        json={"request_id": str(uuid4()), "results": [{"url": "https://example.com"}]},
    )
    result = client.search("best web scrapers 2025")
    assert "results" in result


@responses.activate
def test_search_with_num_results(client):
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/search",
        json={"request_id": str(uuid4()), "results": []},
    )
    result = client.search("test query", num_results=10)
    assert "results" in result


@responses.activate
def test_search_with_location_geo_code(client):
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/search",
        json={"request_id": str(uuid4()), "results": [{"url": "https://example.it"}]},
    )
    result = client.search("best restaurants", location_geo_code="it")
    assert "results" in result


# ------------------------------------------------------------------
# Credits
# ------------------------------------------------------------------


@responses.activate
def test_credits(client):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/credits",
        json={"remaining_credits": 1000, "total_credits_used": 50},
    )
    result = client.credits()
    assert result["remaining_credits"] == 1000


# ------------------------------------------------------------------
# History
# ------------------------------------------------------------------


@responses.activate
def test_history(client):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/history",
        json={"requests": [], "total": 0},
    )
    result = client.history()
    assert "requests" in result


@responses.activate
def test_history_with_filters(client):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/history",
        json={"requests": [], "total": 0},
    )
    result = client.history(endpoint="scrape", status="completed", limit=10)
    assert "requests" in result


# ------------------------------------------------------------------
# Crawl namespace
# ------------------------------------------------------------------


@responses.activate
def test_crawl_start(client):
    crawl_id = str(uuid4())
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/crawl",
        json={"id": crawl_id, "status": "running"},
    )
    result = client.crawl.start("https://example.com", depth=3, max_pages=20)
    assert result["id"] == crawl_id


@responses.activate
def test_crawl_status(client):
    crawl_id = str(uuid4())
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/crawl/{crawl_id}",
        json={"id": crawl_id, "status": "completed", "pages": []},
    )
    result = client.crawl.status(crawl_id)
    assert result["status"] == "completed"


@responses.activate
def test_crawl_stop(client):
    crawl_id = str(uuid4())
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/crawl/{crawl_id}/stop",
        json={"id": crawl_id, "status": "stopped"},
    )
    result = client.crawl.stop(crawl_id)
    assert result["status"] == "stopped"


@responses.activate
def test_crawl_resume(client):
    crawl_id = str(uuid4())
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/crawl/{crawl_id}/resume",
        json={"id": crawl_id, "status": "running"},
    )
    result = client.crawl.resume(crawl_id)
    assert result["status"] == "running"


# ------------------------------------------------------------------
# Monitor namespace
# ------------------------------------------------------------------


@responses.activate
def test_monitor_create(client):
    monitor_id = str(uuid4())
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/monitor",
        json={"id": monitor_id, "name": "Price Monitor"},
    )
    result = client.monitor.create(
        name="Price Monitor",
        url="https://example.com/products",
        prompt="Extract product prices",
        cron="0 9 * * 1",
    )
    assert result["name"] == "Price Monitor"


@responses.activate
def test_monitor_list(client):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/monitor",
        json={"monitors": [], "total": 0},
    )
    result = client.monitor.list()
    assert "monitors" in result


@responses.activate
def test_monitor_get(client):
    monitor_id = str(uuid4())
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/monitor/{monitor_id}",
        json={"id": monitor_id, "name": "Test Monitor"},
    )
    result = client.monitor.get(monitor_id)
    assert result["id"] == monitor_id


@responses.activate
def test_monitor_pause(client):
    monitor_id = str(uuid4())
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/monitor/{monitor_id}/pause",
        json={"id": monitor_id, "status": "paused"},
    )
    result = client.monitor.pause(monitor_id)
    assert result["status"] == "paused"


@responses.activate
def test_monitor_resume(client):
    monitor_id = str(uuid4())
    responses.add(
        responses.POST,
        f"{API_BASE_URL}/monitor/{monitor_id}/resume",
        json={"id": monitor_id, "status": "active"},
    )
    result = client.monitor.resume(monitor_id)
    assert result["status"] == "active"


@responses.activate
def test_monitor_delete(client):
    monitor_id = str(uuid4())
    responses.add(
        responses.DELETE,
        f"{API_BASE_URL}/monitor/{monitor_id}",
        json={"message": "deleted"},
    )
    result = client.monitor.delete(monitor_id)
    assert result["message"] == "deleted"


# ------------------------------------------------------------------
# Error handling
# ------------------------------------------------------------------


@responses.activate
def test_api_error_handling(client):
    from scrapegraph_py.exceptions import APIError

    responses.add(
        responses.POST,
        f"{API_BASE_URL}/scrape",
        json={"error": "Invalid URL"},
        status=400,
    )
    with pytest.raises(APIError) as exc_info:
        client.scrape("https://example.com")
    assert exc_info.value.status_code == 400


# ------------------------------------------------------------------
# Context manager
# ------------------------------------------------------------------


@responses.activate
def test_context_manager(api_key):
    responses.add(
        responses.GET,
        f"{API_BASE_URL}/credits",
        json={"remaining_credits": 500},
    )
    with Client(api_key=api_key) as client:
        result = client.credits()
        assert result["remaining_credits"] == 500
