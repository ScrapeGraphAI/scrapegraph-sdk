"""
Pydantic models for all ScrapeGraphAI API endpoints.

This module provides request and response models for validating and
structuring data for all API operations. All models use Pydantic for
data validation and serialization.

Available Models:
    - AgenticScraperRequest, GetAgenticScraperRequest: Agentic scraper operations
    - CrawlRequest, GetCrawlRequest: Website crawling operations
    - FeedbackRequest: User feedback submission
    - ScrapeRequest, GetScrapeRequest: Basic HTML scraping
    - MarkdownifyRequest, GetMarkdownifyRequest: Markdown conversion
    - SearchScraperRequest, GetSearchScraperRequest: Web research
    - SmartScraperRequest, GetSmartScraperRequest: AI-powered scraping
    - GenerateSchemaRequest, GetSchemaStatusRequest: Schema generation
    - ScheduledJob models: Job scheduling and management

Example:
    >>> from scrapegraph_py.models import SmartScraperRequest
    >>> request = SmartScraperRequest(
    ...     website_url="https://example.com",
    ...     user_prompt="Extract product info"
    ... )
"""

from .agenticscraper import AgenticScraperRequest, GetAgenticScraperRequest
from .crawl import CrawlRequest, GetCrawlRequest
from .feedback import FeedbackRequest
from .scrape import GetScrapeRequest, ScrapeRequest
from .markdownify import GetMarkdownifyRequest, MarkdownifyRequest
from .searchscraper import GetSearchScraperRequest, SearchScraperRequest
from .sitemap import SitemapRequest, SitemapResponse
from .smartscraper import GetSmartScraperRequest, SmartScraperRequest
from .schema import GenerateSchemaRequest, GetSchemaStatusRequest, SchemaGenerationResponse

__all__ = [
    "AgenticScraperRequest",
    "GetAgenticScraperRequest",
    "CrawlRequest",
    "GetCrawlRequest",
    "FeedbackRequest",
    "GetScrapeRequest",
    "ScrapeRequest",
    "GetMarkdownifyRequest",
    "MarkdownifyRequest",
    "GetSearchScraperRequest",
    "SearchScraperRequest",
    "SitemapRequest",
    "SitemapResponse",
    "GetSmartScraperRequest",
    "SmartScraperRequest",
    "GenerateSchemaRequest",
    "GetSchemaStatusRequest",
    "SchemaGenerationResponse",
]
