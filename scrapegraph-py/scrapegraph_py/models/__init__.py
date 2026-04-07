"""
Pydantic models for the ScrapeGraphAI v2 API.
"""

from .crawl import CrawlFormat, CrawlRequest
from .extract import ExtractRequest
from .history import HistoryFilter
from .monitor import MonitorCreateRequest
from .scrape import GetScrapeRequest, ScrapeFormat, ScrapeRequest
from .search import SearchRequest
from .shared import FetchConfig, LlmConfig

__all__ = [
    # Shared
    "FetchConfig",
    "LlmConfig",
    # Scrape
    "ScrapeFormat",
    "ScrapeRequest",
    "GetScrapeRequest",
    # Extract
    "ExtractRequest",
    # Search
    "SearchRequest",
    # Crawl
    "CrawlFormat",
    "CrawlRequest",
    # Monitor
    "MonitorCreateRequest",
    # History
    "HistoryFilter",
]
