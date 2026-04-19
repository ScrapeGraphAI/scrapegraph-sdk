from unittest.mock import MagicMock, patch

import httpx
import pytest

from scrapegraph_py import (
    CrawlRequest,
    ExtractRequest,
    FetchConfig,
    HistoryFilter,
    HtmlFormatConfig,
    ImagesFormatConfig,
    JsonFormatConfig,
    LinksFormatConfig,
    MarkdownFormatConfig,
    MonitorCreateRequest,
    ScrapeGraphAI,
    ScrapeRequest,
    ScreenshotFormatConfig,
    SearchRequest,
)

API_KEY = "test-sgai-key"
BASE_URL = "https://api.scrapegraphai.com/v2"


def mock_response(body: dict, status: int = 200, headers: dict | None = None) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status
    resp.is_success = 200 <= status < 300
    resp.json.return_value = body
    resp.headers = headers or {}
    return resp


class TestScrape:
    def test_success(self):
        body = {
            "results": {"markdown": {"data": ["# Hello"]}},
            "metadata": {"contentType": "text/html"},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(ScrapeRequest(url="https://example.com"))

            assert res.status == "success"
            assert res.data.results == body["results"]
            assert res.data.metadata.content_type == "text/html"
            assert res.elapsed_ms >= 0

            mock.assert_called_once()
            _, kwargs = mock.call_args
            assert "example.com" in kwargs["json"]["url"]

    def test_with_fetch_config_js_mode(self):
        body = {
            "results": {"markdown": {"data": ["# Hello"]}},
            "metadata": {"contentType": "text/html", "provider": "playwright"},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(
                ScrapeRequest(
                    url="https://example.com",
                    fetch_config=FetchConfig(
                        mode="js",
                        stealth=True,
                        timeout=45000,
                        wait=2000,
                        scrolls=3,
                    ),
                    formats=[MarkdownFormatConfig()],
                )
            )

            assert res.status == "success"
            _, kwargs = mock.call_args
            assert kwargs["json"]["fetchConfig"]["mode"] == "js"
            assert kwargs["json"]["fetchConfig"]["stealth"] is True
            assert kwargs["json"]["fetchConfig"]["timeout"] == 45000

    def test_with_fetch_config_headers_cookies(self):
        body = {
            "results": {"html": {"data": ["<html></html>"]}},
            "metadata": {"contentType": "text/html"},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(
                ScrapeRequest(
                    url="https://example.com",
                    fetch_config=FetchConfig(
                        mode="fast",
                        headers={"X-Custom": "test"},
                        cookies={"session": "abc123"},
                    ),
                    formats=[HtmlFormatConfig()],
                )
            )

            assert res.status == "success"
            _, kwargs = mock.call_args
            assert kwargs["json"]["fetchConfig"]["headers"] == {"X-Custom": "test"}
            assert kwargs["json"]["fetchConfig"]["cookies"] == {"session": "abc123"}

    def test_multiple_formats(self):
        body = {
            "results": {
                "markdown": {"data": ["# Title"]},
                "html": {"data": ["<h1>Title</h1>"]},
                "links": {"data": ["https://example.com/page1"]},
                "images": {"data": ["https://example.com/image.png"]},
            },
            "metadata": {"contentType": "text/html"},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(
                ScrapeRequest(
                    url="https://example.com",
                    formats=[
                        MarkdownFormatConfig(mode="reader"),
                        HtmlFormatConfig(mode="prune"),
                        LinksFormatConfig(),
                        ImagesFormatConfig(),
                    ],
                )
            )

            assert res.status == "success"
            assert res.data.results["markdown"] is not None
            assert res.data.results["links"] is not None

    def test_json_format_with_schema(self):
        body = {
            "results": {
                "json": {"data": {"title": "Example", "price": 99.99}},
            },
            "metadata": {"contentType": "text/html"},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(
                ScrapeRequest(
                    url="https://example.com",
                    formats=[
                        JsonFormatConfig(
                            prompt="Extract product info",
                            schema={"type": "object", "properties": {"title": {"type": "string"}}},
                        ),
                    ],
                )
            )

            assert res.status == "success"
            _, kwargs = mock.call_args
            assert kwargs["json"]["formats"][0]["prompt"] == "Extract product info"
            assert kwargs["json"]["formats"][0]["schema"] is not None

    def test_screenshot_format(self):
        body = {
            "results": {"screenshot": {"data": {"url": "https://..."}}},
            "metadata": {"contentType": "text/html"},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(
                ScrapeRequest(
                    url="https://example.com",
                    formats=[ScreenshotFormatConfig(full_page=True, width=1920, height=1080)],
                )
            )

            assert res.status == "success"
            _, kwargs = mock.call_args
            assert kwargs["json"]["formats"][0]["fullPage"] is True
            assert kwargs["json"]["formats"][0]["width"] == 1920

    def test_http_401_error(self):
        with patch.object(
            httpx.Client, "request", return_value=mock_response({"detail": "Invalid key"}, 401)
        ):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(ScrapeRequest(url="https://example.com"))

            assert res.status == "error"
            assert "Invalid or missing API key" in res.error

    def test_http_402_error(self):
        with patch.object(httpx.Client, "request", return_value=mock_response({}, 402)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(ScrapeRequest(url="https://example.com"))

            assert res.status == "error"
            assert "Insufficient credits" in res.error

    def test_http_429_error(self):
        with patch.object(httpx.Client, "request", return_value=mock_response({}, 429)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(ScrapeRequest(url="https://example.com"))

            assert res.status == "error"
            assert "Rate limited" in res.error

    def test_timeout_error(self):
        with patch.object(httpx.Client, "request", side_effect=httpx.TimeoutException("timeout")):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.scrape(ScrapeRequest(url="https://example.com"))

            assert res.status == "error"
            assert "timed out" in res.error


class TestExtract:
    def test_success(self):
        body = {
            "raw": "Example Domain",
            "json": {"title": "Example"},
            "usage": {"promptTokens": 100, "completionTokens": 50},
            "metadata": {},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.extract(
                ExtractRequest(
                    url="https://example.com",
                    prompt="What is this page about?",
                )
            )

            assert res.status == "success"
            assert res.data.json_data == {"title": "Example"}

    def test_with_schema(self):
        body = {
            "raw": None,
            "json": {"name": "Test"},
            "usage": {"promptTokens": 10, "completionTokens": 5},
            "metadata": {},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.extract(
                ExtractRequest(
                    url="https://example.com",
                    prompt="Extract data",
                    schema={"type": "object"},
                )
            )

            assert res.status == "success"
            _, kwargs = mock.call_args
            assert kwargs["json"]["schema"] == {"type": "object"}


class TestSearch:
    def test_success(self):
        body = {
            "results": [{"url": "https://...", "title": "Result", "content": "..."}],
            "metadata": {"search": {}, "pages": {}},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.search(SearchRequest(query="test query", num_results=5))

            assert res.status == "success"
            assert len(res.data.results) == 1

    def test_with_extraction(self):
        body = {
            "results": [],
            "json": {"summary": "Test"},
            "metadata": {"search": {}, "pages": {}},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.search(
                SearchRequest(
                    query="test",
                    prompt="Summarize results",
                )
            )

            assert res.status == "success"
            _, kwargs = mock.call_args
            assert kwargs["json"]["prompt"] == "Summarize results"


class TestCrawl:
    def test_start(self):
        body = {"id": "crawl-123", "status": "running", "total": 0, "finished": 0, "pages": []}
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.crawl.start(
                CrawlRequest(
                    url="https://example.com",
                    max_pages=10,
                    max_depth=2,
                )
            )

            assert res.status == "success"
            assert res.data.id == "crawl-123"
            _, kwargs = mock.call_args
            assert kwargs["json"]["maxPages"] == 10
            assert kwargs["json"]["maxDepth"] == 2

    def test_get(self):
        body = {"id": "crawl-123", "status": "completed", "total": 5, "finished": 5, "pages": []}
        with patch.object(httpx.Client, "request", return_value=mock_response(body)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.crawl.get("crawl-123")

            assert res.status == "success"
            assert res.data.status == "completed"

    def test_stop(self):
        with patch.object(httpx.Client, "request", return_value=mock_response({})):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.crawl.stop("crawl-123")
            assert res.status == "success"

    def test_delete(self):
        with patch.object(httpx.Client, "request", return_value=mock_response({})):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.crawl.delete("crawl-123")
            assert res.status == "success"


class TestMonitor:
    def test_create(self):
        body = {
            "cronId": "mon-123",
            "scheduleId": "sch-456",
            "interval": "0 * * * *",
            "status": "active",
            "config": {},
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-01T00:00:00Z",
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.monitor.create(
                MonitorCreateRequest(
                    url="https://example.com",
                    name="Test Monitor",
                    interval="0 * * * *",
                )
            )

            assert res.status == "success"
            assert res.data.cron_id == "mon-123"

    def test_list(self):
        body = [
            {
                "cronId": "mon-1",
                "scheduleId": "sch-1",
                "interval": "0 * * * *",
                "status": "active",
                "config": {},
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
            },
            {
                "cronId": "mon-2",
                "scheduleId": "sch-2",
                "interval": "0 */2 * * *",
                "status": "active",
                "config": {},
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
            },
        ]
        with patch.object(httpx.Client, "request", return_value=mock_response(body)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.monitor.list()
            assert res.status == "success"
            assert len(res.data) == 2
            assert res.data[0].cron_id == "mon-1"
            assert res.data[1].cron_id == "mon-2"


class TestHistory:
    def test_list(self):
        body = {
            "data": [
                {
                    "id": "req-1",
                    "service": "scrape",
                    "status": "completed",
                    "error": None,
                    "elapsedMs": 100,
                    "createdAt": "2024-01-01T00:00:00Z",
                    "requestParentId": None,
                    "params": {},
                    "result": {},
                }
            ],
            "pagination": {"page": 1, "limit": 20, "total": 100},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.history.list(HistoryFilter(limit=5, service="scrape"))

            assert res.status == "success"
            assert res.data.pagination.total == 100

    def test_get(self):
        body = {
            "id": "req-1",
            "service": "scrape",
            "status": "completed",
            "error": None,
            "elapsedMs": 100,
            "createdAt": "2024-01-01T00:00:00Z",
            "requestParentId": None,
            "params": {},
            "result": {},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.history.get("req-1")
            assert res.status == "success"


class TestCreditsAndHealth:
    def test_credits(self):
        body = {
            "remaining": 1000,
            "used": 500,
            "plan": "pro",
            "jobs": {"crawl": {"used": 1, "limit": 10}, "monitor": {"used": 2, "limit": 5}},
        }
        with patch.object(httpx.Client, "request", return_value=mock_response(body)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.credits()

            assert res.status == "success"
            assert res.data.remaining == 1000
            assert res.data.plan == "pro"

    def test_health(self):
        body = {"status": "ok", "uptime": 12345}
        with patch.object(httpx.Client, "request", return_value=mock_response(body)):
            sgai = ScrapeGraphAI(api_key=API_KEY)
            res = sgai.health()

            assert res.status == "success"
            assert res.data.status == "ok"


class TestClientInit:
    def test_missing_api_key_raises(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="API key required"):
                ScrapeGraphAI()

    def test_api_key_from_env(self):
        with patch.dict("os.environ", {"SGAI_API_KEY": "env-key"}):
            sgai = ScrapeGraphAI()
            assert sgai._api_key == "env-key"

    def test_explicit_api_key(self):
        sgai = ScrapeGraphAI(api_key="explicit-key")
        assert sgai._api_key == "explicit-key"


class TestCamelCaseSerialization:
    def test_snake_to_camel(self):
        with patch.object(httpx.Client, "request", return_value=mock_response({})) as mock:
            sgai = ScrapeGraphAI(api_key=API_KEY)
            sgai.scrape(
                ScrapeRequest(
                    url="https://example.com",
                    content_type="application/pdf",
                    fetch_config=FetchConfig(
                        mode="js",
                        timeout=30000,
                    ),
                )
            )

            _, kwargs = mock.call_args
            body = kwargs["json"]
            assert "contentType" in body
            assert "content_type" not in body
            assert "fetchConfig" in body
            assert "fetch_config" not in body
