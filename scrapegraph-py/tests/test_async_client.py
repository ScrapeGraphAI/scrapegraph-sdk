"""Tests for the asynchronous AsyncClient against the SGAI v2 contract."""

import pytest
import pytest_asyncio
from pydantic import BaseModel, Field

from scrapegraph_py.async_client import AsyncClient
from tests.utils import generate_mock_api_key


@pytest.fixture
def api_key():
    return generate_mock_api_key()


@pytest_asyncio.fixture
async def client(api_key):
    c = AsyncClient(api_key=api_key)
    yield c
    await c.close()


@pytest.mark.asyncio
async def test_bearer_auth_header(api_key):
    c = AsyncClient(api_key=api_key)
    assert c.headers["Authorization"] == f"Bearer {api_key}"
    assert c.headers["X-SDK-Version"].startswith("python@")
    await c.close()


@pytest.mark.asyncio
async def test_scrape_translates_legacy_format_to_formats_array(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["method"] = method
        captured["url"] = url
        captured["json"] = kwargs["json"]
        return {
            "results": {"html": "<h1>Hello</h1>"},
            "metadata": {"url": "https://example.com"},
        }

    client._make_request = fake_request

    result = await client.scrape("https://example.com", format="html")

    assert captured["method"] == "POST"
    assert captured["url"].endswith("/scrape")
    assert captured["json"] == {
        "url": "https://example.com",
        "formats": [{"type": "html", "mode": "normal"}],
    }
    assert result["results"]["html"] == "<h1>Hello</h1>"


@pytest.mark.asyncio
async def test_extract_sends_schema_and_fetch_config(client):
    captured = {}

    class Product(BaseModel):
        name: str = Field(description="Product name")

    async def fake_request(method, url, **kwargs):
        captured["json"] = kwargs["json"]
        return {
            "json": {"name": "Widget"},
            "raw": None,
            "usage": {},
            "metadata": {"chunker": {}},
        }

    client._make_request = fake_request

    result = await client.extract(
        url="https://example.com",
        prompt="Extract product name",
        schema=Product,
        fetch_config={"timeout": 5000},
    )

    assert captured["json"] == {
        "url": "https://example.com",
        "prompt": "Extract product name",
        "schema": {
            "properties": {
                "name": {
                    "description": "Product name",
                    "title": "Name",
                    "type": "string",
                }
            },
            "required": ["name"],
            "title": "Product",
            "type": "object",
        },
        "mode": "normal",
        "fetchConfig": {"mode": "auto", "timeout": 5000, "mock": False},
    }
    assert result["json"]["name"] == "Widget"


@pytest.mark.asyncio
async def test_search_accepts_single_result_and_uses_camel_case(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["json"] = kwargs["json"]
        return {
            "results": [{"url": "https://example.com"}],
            "metadata": {"search": {}, "pages": {"requested": 1, "scraped": 1}},
        }

    client._make_request = fake_request

    result = await client.search(
        "example domain",
        num_results=1,
        prompt="Extract titles",
        schema={"type": "object", "properties": {"title": {"type": "string"}}},
        location_geo_code="it",
        time_range="past_week",
    )

    assert captured["json"] == {
        "query": "example domain",
        "numResults": 1,
        "format": "markdown",
        "mode": "prune",
        "prompt": "Extract titles",
        "schema": {"type": "object", "properties": {"title": {"type": "string"}}},
        "locationGeoCode": "it",
        "timeRange": "past_week",
    }
    assert result["results"][0]["url"] == "https://example.com"


@pytest.mark.asyncio
async def test_credits_returns_v2_balance_shape(client):
    async def fake_request(method, url, **kwargs):
        return {"remaining": 1000, "used": 50, "plan": "local"}

    client._make_request = fake_request
    result = await client.credits()
    assert result["remaining"] == 1000
    assert result["used"] == 50


@pytest.mark.asyncio
async def test_history_maps_legacy_endpoint_and_offset(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["params"] = kwargs["params"]
        return {"data": [], "pagination": {"page": 3, "limit": 10, "total": 0}}

    client._make_request = fake_request

    result = await client.history(endpoint="scrape", limit=10, offset=20)

    assert captured["params"] == {"page": 3, "limit": 10, "service": "scrape"}
    assert result["pagination"]["page"] == 3


@pytest.mark.asyncio
async def test_history_rejects_status_filter(client):
    with pytest.raises(ValueError, match="not supported"):
        await client.history(status="completed")


@pytest.mark.asyncio
async def test_schema_posts_prompt_and_existing_schema(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["json"] = kwargs["json"]
        return {
            "refinedPrompt": "Refined prompt",
            "schema": {"type": "object"},
            "usage": {},
        }

    client._make_request = fake_request

    result = await client.schema(
        "Extract product data",
        existing_schema={"type": "object", "properties": {"name": {"type": "string"}}},
    )

    assert captured["json"] == {
        "prompt": "Extract product data",
        "existingSchema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
        },
    }
    assert result["schema"]["type"] == "object"


@pytest.mark.asyncio
async def test_validate_uses_email_query_param(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["params"] = kwargs["params"]
        return {"ok": True}

    client._make_request = fake_request

    result = await client.validate("user@example.com")

    assert captured["params"] == {"email": "user@example.com"}
    assert result["ok"] is True


@pytest.mark.asyncio
async def test_crawl_start_translates_legacy_depth_and_format(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["json"] = kwargs["json"]
        return {
            "id": "crawl-123",
            "status": "running",
            "total": 0,
            "finished": 0,
            "pages": [],
        }

    client._make_request = fake_request

    result = await client.crawl.start(
        "https://example.com", depth=3, max_pages=20, format="html"
    )

    assert captured["json"] == {
        "url": "https://example.com",
        "formats": [{"type": "html", "mode": "normal"}],
        "maxDepth": 3,
        "maxPages": 20,
        "maxLinksPerPage": 10,
        "allowExternal": False,
    }
    assert result["id"] == "crawl-123"


@pytest.mark.asyncio
async def test_monitor_create_translates_legacy_prompt_to_json_format(client):
    captured = {}

    async def fake_request(method, url, **kwargs):
        captured["json"] = kwargs["json"]
        return {
            "cronId": "mon-1",
            "scheduleId": "sched-1",
            "interval": "0 9 * * 1",
            "status": "active",
            "config": kwargs["json"],
            "createdAt": "2026-01-01T00:00:00.000Z",
            "updatedAt": "2026-01-01T00:00:00.000Z",
        }

    client._make_request = fake_request

    result = await client.monitor.create(
        name="Price Monitor",
        url="https://example.com/products",
        prompt="Extract product prices",
        interval="0 9 * * 1",
        schema={"type": "object", "properties": {"price": {"type": "number"}}},
    )

    assert captured["json"] == {
        "name": "Price Monitor",
        "url": "https://example.com/products",
        "formats": [
            {
                "type": "json",
                "prompt": "Extract product prices",
                "mode": "normal",
                "schema": {
                    "type": "object",
                    "properties": {"price": {"type": "number"}},
                },
            }
        ],
        "interval": "0 9 * * 1",
    }
    assert result["cronId"] == "mon-1"


@pytest.mark.asyncio
async def test_api_error_handling(client):
    from scrapegraph_py.exceptions import APIError

    async def fake_request(method, url, **kwargs):
        raise APIError("Invalid URL", status_code=400)

    client._make_request = fake_request

    with pytest.raises(APIError) as exc_info:
        await client.scrape("https://example.com")
    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_context_manager(api_key):
    async with AsyncClient(api_key=api_key) as client:

        async def fake_request(method, url, **kwargs):
            return {"remaining": 500, "used": 0, "plan": "local"}

        client._make_request = fake_request
        result = await client.credits()
        assert result["remaining"] == 500
