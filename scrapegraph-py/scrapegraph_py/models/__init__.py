"""
Pydantic models for the ScrapeGraphAI v2 API.
"""

from .shared import FetchConfig, LlmConfig
from .scrape import ScrapeFormat, ScrapeRequest, GetScrapeRequest
from .extract import ExtractRequest
from .search import SearchRequest
from .crawl import CrawlFormat, CrawlRequest
from .monitor import MonitorCreateRequest
from .history import HistoryFilter

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
