"""
ScrapeGraphAI Python SDK v2

A Python SDK for the ScrapeGraphAI v2 API, providing both synchronous
and asynchronous clients for intelligent web scraping powered by AI.

Quick Start:
    >>> from scrapegraph_py import Client
    >>> client = Client(api_key="sgai-...")
    >>> result = client.scrape("https://example.com")
    >>> result = client.extract("https://example.com", prompt="Extract prices")
    >>> job = client.crawl.start("https://example.com", depth=3)

Async Usage:
    >>> import asyncio
    >>> from scrapegraph_py import AsyncClient
    >>> async def main():
    ...     async with AsyncClient(api_key="sgai-...") as client:
    ...         result = await client.extract(
    ...             url="https://example.com",
    ...             prompt="Extract products"
    ...         )
    >>> asyncio.run(main())
"""

from .async_client import AsyncClient
from .client import Client
from .config import VERSION
from .models.crawl import CrawlFormat, CrawlRequest
from .models.extract import ExtractRequest
from .models.history import HistoryFilter
from .models.monitor import MonitorCreateRequest
from .models.scrape import ScrapeFormat, ScrapeRequest
from .models.search import SearchRequest
from .models.shared import FetchConfig, LlmConfig

__version__ = VERSION

__all__ = [
    "Client",
    "AsyncClient",
    # Shared config
    "FetchConfig",
    "LlmConfig",
    # Scrape
    "ScrapeFormat",
    "ScrapeRequest",
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
