"""Tests for the SGAI v2 Pydantic models."""

import pytest

from scrapegraph_py.models.crawl import CrawlFormat, CrawlRequest
from scrapegraph_py.models.extract import ExtractRequest
from scrapegraph_py.models.history import HistoryFilter
from scrapegraph_py.models.monitor import MonitorCreateRequest
from scrapegraph_py.models.scrape import ScrapeFormat, ScrapeRequest
from scrapegraph_py.models.search import SearchRequest
from scrapegraph_py.models.shared import FetchConfig, FetchMode


def test_fetch_config_defaults():
    config = FetchConfig()
    assert config.mock is False
    assert config.mode == FetchMode.AUTO


def test_fetch_config_uses_camel_case():
    config = FetchConfig(mode="fast")
    data = config.model_dump()
    assert "cookies" not in data
    assert data["mode"] == "fast"


def test_scrape_request_defaults_to_markdown_formats():
    req = ScrapeRequest(url="https://example.com")
    assert req.formats == [{"type": "markdown", "mode": "normal"}]
    assert req.model_dump()["formats"] == [{"type": "markdown", "mode": "normal"}]


def test_scrape_request_invalid_url():
    with pytest.raises(ValueError, match="URL must start with"):
        ScrapeRequest(url="ftp://example.com")


def test_extract_request_valid():
    req = ExtractRequest(url="https://example.com", prompt="Extract data")
    assert req.prompt == "Extract data"
    assert req.model_dump()["mode"] == "normal"


def test_extract_request_requires_one_content_input():
    with pytest.raises(ValueError, match="Either url, html, or markdown is required"):
        ExtractRequest(url=None, html=None, markdown=None, prompt="Extract")


def test_search_request_accepts_single_result():
    req = SearchRequest(query="python web scraping", num_results=1)
    assert req.num_results == 1
    assert req.model_dump()["numResults"] == 1


def test_search_request_schema_requires_prompt():
    with pytest.raises(ValueError, match="schema requires prompt"):
        SearchRequest(
            query="python web scraping",
            schema={"type": "object"},
        )


def test_crawl_request_defaults_to_markdown_formats():
    req = CrawlRequest(url="https://example.com")
    assert req.formats == [{"type": "markdown", "mode": "normal"}]
    assert req.max_depth == 2
    assert req.model_dump()["maxDepth"] == 2


def test_crawl_request_custom_values():
    req = CrawlRequest(
        url="https://example.com",
        formats=[{"type": CrawlFormat.HTML.value, "mode": "normal"}],
        max_depth=5,
        max_pages=50,
        include_patterns=["/blog/*"],
        exclude_patterns=["/admin/*"],
    )
    data = req.model_dump()
    assert data["formats"] == [{"type": "html", "mode": "normal"}]
    assert data["maxDepth"] == 5
    assert len(data["includePatterns"]) == 1


def test_monitor_create_valid():
    req = MonitorCreateRequest(
        name="Price Tracker",
        url="https://example.com",
        formats=[
            {
                "type": ScrapeFormat.JSON.value,
                "prompt": "Extract prices",
                "mode": "normal",
            }
        ],
        interval="0 9 * * 1",
    )
    assert req.name == "Price Tracker"
    assert req.model_dump()["formats"][0]["type"] == "json"


def test_monitor_create_invalid_interval():
    with pytest.raises(ValueError, match="5 fields"):
        MonitorCreateRequest(
            name="Test",
            url="https://example.com",
            formats=[{"type": "markdown", "mode": "normal"}],
            interval="invalid",
        )


def test_history_filter_to_params():
    filt = HistoryFilter(page=2, service="scrape", limit=10)
    assert filt.to_params() == {"page": 2, "limit": 10, "service": "scrape"}
