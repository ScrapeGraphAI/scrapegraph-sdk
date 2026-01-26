"""
ScrapeGraphAI Python SDK

A comprehensive Python SDK for the ScrapeGraphAI API, providing both synchronous
and asynchronous clients for all API endpoints.

Main Features:
    - SmartScraper: AI-powered web scraping with structured data extraction
    - SearchScraper: Web research across multiple sources
    - Agentic Scraper: Automated browser interactions and form filling
    - Crawl: Website crawling with AI extraction or markdown conversion
    - Markdownify: Convert web pages to clean markdown
    - Schema Generation: AI-assisted schema creation for data extraction
    - Scheduled Jobs: Automate recurring scraping tasks

Quick Start:
    >>> from scrapegraph_py import Client
    >>>
    >>> # Initialize client from environment variables
    >>> client = Client.from_env()
    >>>
    >>> # Basic scraping
    >>> result = client.smartscraper(
    ...     website_url="https://example.com",
    ...     user_prompt="Extract all product information"
    ... )
    >>>
    >>> # With context manager
    >>> with Client.from_env() as client:
    ...     result = client.scrape(website_url="https://example.com")

Async Usage:
    >>> import asyncio
    >>> from scrapegraph_py import AsyncClient
    >>>
    >>> async def main():
    ...     async with AsyncClient.from_env() as client:
    ...         result = await client.smartscraper(
    ...             website_url="https://example.com",
    ...             user_prompt="Extract products"
    ...         )
    >>>
    >>> asyncio.run(main())

For more information visit: https://scrapegraphai.com
Documentation: https://docs.scrapegraphai.com
"""

from .async_client import AsyncClient
from .client import Client

# Scrape Models
from .models.scrape import (
    ScrapeRequest,
    GetScrapeRequest,
)

# Scheduled Jobs Models
from .models.scheduled_jobs import (
    GetJobExecutionsRequest,
    GetScheduledJobRequest,
    GetScheduledJobsRequest,
    JobActionRequest,
    JobActionResponse,
    JobExecutionListResponse,
    JobExecutionResponse,
    JobTriggerResponse,
    ScheduledJobCreate,
    ScheduledJobListResponse,
    ScheduledJobResponse,
    ScheduledJobUpdate,
    ServiceType,
    TriggerJobRequest,
)

__all__ = [
    "Client", 
    "AsyncClient",
    # Scrape Models
    "ScrapeRequest",
    "GetScrapeRequest",
    # Scheduled Jobs Models
    "ServiceType",
    "ScheduledJobCreate",
    "ScheduledJobUpdate", 
    "ScheduledJobResponse",
    "ScheduledJobListResponse",
    "JobExecutionResponse",
    "JobExecutionListResponse",
    "JobTriggerResponse",
    "JobActionResponse",
    "GetScheduledJobsRequest",
    "GetScheduledJobRequest",
    "GetJobExecutionsRequest",
    "TriggerJobRequest",
    "JobActionRequest",
]
