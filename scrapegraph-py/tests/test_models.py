"""Tests for v2 Pydantic models."""

import pytest

from scrapegraph_py.models.crawl import CrawlFormat, CrawlRequest
from scrapegraph_py.models.extract import ExtractRequest
from scrapegraph_py.models.history import HistoryFilter
from scrapegraph_py.models.monitor import MonitorCreateRequest
from scrapegraph_py.models.scrape import ScrapeFormat, ScrapeRequest
from scrapegraph_py.models.search import SearchRequest
from scrapegraph_py.models.shared import FetchConfig, FetchMode, LlmConfig

# ------------------------------------------------------------------
# Shared models
# ------------------------------------------------------------------


def test_fetch_config_defaults():
    config = FetchConfig()
    assert config.mock is False
    assert config.mode == FetchMode.AUTO


def test_fetch_config_excludes_none():
    config = FetchConfig(mode="fast")
    data = config.model_dump()
    assert "cookies" not in data
    assert data["mode"] == "fast"


def test_fetch_config_all_modes():
    for mode in FetchMode:
        config = FetchConfig(mode=mode)
        assert config.mode == mode


def test_fetch_config_invalid_mode():
    with pytest.raises(ValueError):
        FetchConfig(mode="invalid")


def test_llm_config_excludes_none():
    config = LlmConfig(model="gpt-4")
    data = config.model_dump()
    assert data["model"] == "gpt-4"
    assert "temperature" not in data


# ------------------------------------------------------------------
# Scrape
# ------------------------------------------------------------------


def test_scrape_request_valid():
    req = ScrapeRequest(url="https://example.com")
    assert req.format == ScrapeFormat.MARKDOWN


def test_scrape_request_html():
    req = ScrapeRequest(url="https://example.com", format=ScrapeFormat.HTML)
    assert req.format == ScrapeFormat.HTML


def test_scrape_request_empty_url():
    with pytest.raises(ValueError, match="URL cannot be empty"):
        ScrapeRequest(url="")


def test_scrape_request_invalid_url():
    with pytest.raises(ValueError, match="URL must start with"):
        ScrapeRequest(url="ftp://example.com")


# ------------------------------------------------------------------
# Extract
# ------------------------------------------------------------------


def test_extract_request_valid():
    req = ExtractRequest(url="https://example.com", prompt="Extract data")
    assert req.prompt == "Extract data"


def test_extract_request_empty_prompt():
    with pytest.raises(ValueError, match="Prompt cannot be empty"):
        ExtractRequest(url="https://example.com", prompt="")


def test_extract_request_with_schema():
    req = ExtractRequest(
        url="https://example.com",
        prompt="Extract",
        output_schema={"type": "object", "properties": {"name": {"type": "string"}}},
    )
    assert req.output_schema is not None


# ------------------------------------------------------------------
# Search
# ------------------------------------------------------------------


def test_search_request_valid():
    req = SearchRequest(query="python web scraping")
    assert req.num_results == 5


def test_search_request_custom_results():
    req = SearchRequest(query="test", num_results=10)
    assert req.num_results == 10


def test_search_request_empty_query():
    with pytest.raises(ValueError, match="Query cannot be empty"):
        SearchRequest(query="")


def test_search_request_num_results_bounds():
    with pytest.raises(ValueError):
        SearchRequest(query="test", num_results=2)
    with pytest.raises(ValueError):
        SearchRequest(query="test", num_results=21)


# ------------------------------------------------------------------
# Crawl
# ------------------------------------------------------------------


def test_crawl_request_valid():
    req = CrawlRequest(url="https://example.com")
    assert req.depth == 2
    assert req.max_pages == 10
    assert req.format == CrawlFormat.MARKDOWN


def test_crawl_request_custom():
    req = CrawlRequest(
        url="https://example.com",
        depth=5,
        max_pages=50,
        format=CrawlFormat.HTML,
        include_patterns=["/blog/*"],
        exclude_patterns=["/admin/*"],
    )
    assert req.depth == 5
    assert len(req.include_patterns) == 1


def test_crawl_request_invalid_url():
    with pytest.raises(ValueError):
        CrawlRequest(url="not-a-url")


def test_crawl_request_depth_bounds():
    with pytest.raises(ValueError):
        CrawlRequest(url="https://example.com", depth=0)
    with pytest.raises(ValueError):
        CrawlRequest(url="https://example.com", depth=11)


# ------------------------------------------------------------------
# Monitor
# ------------------------------------------------------------------


def test_monitor_create_valid():
    req = MonitorCreateRequest(
        name="Price Tracker",
        url="https://example.com",
        prompt="Extract prices",
        cron="0 9 * * 1",
    )
    assert req.name == "Price Tracker"


def test_monitor_create_invalid_cron():
    with pytest.raises(ValueError, match="5 fields"):
        MonitorCreateRequest(
            name="Test",
            url="https://example.com",
            prompt="Test",
            cron="invalid",
        )


def test_monitor_create_empty_name():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        MonitorCreateRequest(
            name="",
            url="https://example.com",
            prompt="Test",
            cron="0 9 * * 1",
        )


# ------------------------------------------------------------------
# History
# ------------------------------------------------------------------


def test_history_filter_empty():
    f = HistoryFilter()
    assert f.to_params() == {}


def test_history_filter_with_values():
    f = HistoryFilter(endpoint="scrape", limit=10)
    params = f.to_params()
    assert params == {"endpoint": "scrape", "limit": 10}
