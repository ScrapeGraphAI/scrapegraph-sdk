"""
Synchronous HTTP client for the ScrapeGraphAI API.

This module provides a synchronous client for interacting with all ScrapeGraphAI
API endpoints including smartscraper, searchscraper, crawl, agentic scraper,
markdownify, schema generation, scheduled jobs, and utility functions.

The Client class supports:
- API key authentication
- SSL verification configuration
- Request timeout configuration
- Automatic retry logic with exponential backoff
- Mock mode for testing
- Context manager support for proper resource cleanup

Example:
    Basic usage with environment variables:
        >>> from scrapegraph_py import Client
        >>> client = Client.from_env()
        >>> result = client.smartscraper(
        ...     website_url="https://example.com",
        ...     user_prompt="Extract product information"
        ... )

    Using context manager:
        >>> with Client(api_key="sgai-...") as client:
        ...     result = client.scrape(website_url="https://example.com")
"""
import uuid as _uuid
from typing import Any, Callable, Dict, Optional
from urllib.parse import urlparse

import requests
import urllib3
from pydantic import BaseModel
from requests.exceptions import RequestException

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
from scrapegraph_py.models.agenticscraper import (
    AgenticScraperRequest,
    GetAgenticScraperRequest,
)
from scrapegraph_py.models.crawl import CrawlRequest, GetCrawlRequest
from scrapegraph_py.models.feedback import FeedbackRequest
from scrapegraph_py.models.markdownify import GetMarkdownifyRequest, MarkdownifyRequest
from scrapegraph_py.models.schema import (
    GenerateSchemaRequest,
    GetSchemaStatusRequest,
    SchemaGenerationResponse,
)
from scrapegraph_py.models.scrape import GetScrapeRequest, ScrapeRequest
from scrapegraph_py.models.searchscraper import (
    GetSearchScraperRequest,
    SearchScraperRequest,
)
from scrapegraph_py.models.sitemap import SitemapRequest, SitemapResponse
from scrapegraph_py.models.smartscraper import (
    GetSmartScraperRequest,
    SmartScraperRequest,
)
from scrapegraph_py.models.scheduled_jobs import (
    GetJobExecutionsRequest,
    GetScheduledJobRequest,
    GetScheduledJobsRequest,
    JobActionRequest,
    JobActionResponse,
    JobExecutionListResponse,
    JobTriggerResponse,
    ScheduledJobCreate,
    ScheduledJobListResponse,
    ScheduledJobResponse,
    ScheduledJobUpdate,
    TriggerJobRequest,
)
from scrapegraph_py.utils.helpers import handle_sync_response, validate_api_key


class Client:
    """
    Synchronous client for the ScrapeGraphAI API.

    This class provides synchronous methods for all ScrapeGraphAI API endpoints.
    It handles authentication, request management, error handling, and supports
    mock mode for testing.

    Attributes:
        api_key (str): The API key for authentication
        headers (dict): Default headers including API key
        timeout (Optional[float]): Request timeout in seconds
        max_retries (int): Maximum number of retry attempts
        retry_delay (float): Delay between retries in seconds
        mock (bool): Whether mock mode is enabled
        session (requests.Session): HTTP session for connection pooling

    Example:
        >>> client = Client.from_env()
        >>> result = client.smartscraper(
        ...     website_url="https://example.com",
        ...     user_prompt="Extract all products"
        ... )
    """
    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        mock: Optional[bool] = None,
        mock_handler: Optional[Callable[[str, str, Dict[str, Any]], Any]] = None,
        mock_responses: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Client using API key from environment variable.

        Args:
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            mock: If True, the client will not perform real HTTP requests and
                  will return stubbed responses. If None, reads from SGAI_MOCK env.
        """
        from os import getenv

        # Allow enabling mock mode from environment if not explicitly provided
        if mock is None:
            mock_env = getenv("SGAI_MOCK", "0").strip().lower()
            mock = mock_env in {"1", "true", "yes", "on"}
        
        api_key = getenv("SGAI_API_KEY")
        # In mock mode, we don't need a real API key
        if not api_key:
            if mock:
                api_key = "sgai-00000000-0000-0000-0000-000000000000"
            else:
                raise ValueError("SGAI_API_KEY environment variable not set")
        return cls(
            api_key=api_key,
            verify_ssl=verify_ssl,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
            mock=bool(mock),
            mock_handler=mock_handler,
            mock_responses=mock_responses,
        )

    def __init__(
        self,
        api_key: str = None,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        mock: bool = False,
        mock_handler: Optional[Callable[[str, str, Dict[str, Any]], Any]] = None,
        mock_responses: Optional[Dict[str, Any]] = None,
    ):
        """Initialize Client with configurable parameters.

        Args:
            api_key: API key for authentication. If None, will try to load
                     from environment
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            mock: If True, the client will bypass HTTP calls and return
                  deterministic mock responses
            mock_handler: Optional callable to generate custom mock responses
                           given (method, url, request_kwargs)
            mock_responses: Optional mapping of path (e.g. "/v1/credits") to
                            static response or callable returning a response
        """
        logger.info("🔑 Initializing Client")

        # Try to get API key from environment if not provided
        if api_key is None:
            from os import getenv

            api_key = getenv("SGAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "SGAI_API_KEY not provided and not found in environment"
                )

        validate_api_key(api_key)
        logger.debug(
            f"🛠️ Configuration: verify_ssl={verify_ssl}, timeout={timeout}, "
            f"max_retries={max_retries}"
        )

        self.api_key = api_key
        self.headers = {**DEFAULT_HEADERS, "SGAI-APIKEY": api_key}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.mock = bool(mock)
        self.mock_handler = mock_handler
        self.mock_responses = mock_responses or {}

        # Create a session for connection pooling
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.verify = verify_ssl

        # Configure retries
        adapter = requests.adapters.HTTPAdapter(
            max_retries=requests.urllib3.Retry(
                total=max_retries,
                backoff_factor=retry_delay,
                status_forcelist=[500, 502, 503, 504],
            )
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Add warning suppression if verify_ssl is False
        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        logger.info("✅ Client initialized successfully")

    def _make_request(self, method: str, url: str, **kwargs) -> Any:
        """
        Make HTTP request with error handling and retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Full URL for the request
            **kwargs: Additional arguments to pass to requests

        Returns:
            Parsed JSON response data

        Raises:
            APIError: If the API returns an error response
            ConnectionError: If unable to connect to the API

        Note:
            In mock mode, this method returns deterministic responses without
            making actual HTTP requests.
        """
        # Short-circuit when mock mode is enabled
        if getattr(self, "mock", False):
            return self._mock_response(method, url, **kwargs)
        try:
            logger.info(f"🚀 Making {method} request to {url}")
            logger.debug(f"🔍 Request parameters: {kwargs}")

            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            logger.debug(f"📥 Response status: {response.status_code}")

            result = handle_sync_response(response)
            logger.info(f"✅ Request completed successfully: {method} {url}")
            return result

        except RequestException as e:
            logger.error(f"❌ Request failed: {str(e)}")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error", str(e))
                    logger.error(f"🔴 API Error: {error_msg}")
                    raise APIError(error_msg, status_code=e.response.status_code)
                except ValueError:
                    logger.error("🔴 Could not parse error response")
                    raise APIError(
                        str(e),
                        status_code=(
                            e.response.status_code
                            if hasattr(e.response, "status_code")
                            else None
                        ),
                    )
            logger.error(f"🔴 Connection Error: {str(e)}")
            raise ConnectionError(f"Failed to connect to API: {str(e)}")

    def _mock_response(self, method: str, url: str, **kwargs) -> Any:
        """Return a deterministic mock response without performing network I/O.

        Resolution order:
        1) If a custom mock_handler is provided, delegate to it
        2) If mock_responses contains a key for the request path, use it
        3) Fallback to built-in defaults per endpoint family
        """
        logger.info(f"🧪 Mock mode active. Returning stub for {method} {url}")

        # 1) Custom handler
        if self.mock_handler is not None:
            try:
                return self.mock_handler(method, url, kwargs)
            except Exception as handler_error:
                logger.warning(f"Custom mock_handler raised: {handler_error}. Falling back to defaults.")

        # 2) Path-based override
        try:
            parsed = urlparse(url)
            path = parsed.path.rstrip("/")
        except Exception:
            path = url

        override = self.mock_responses.get(path)
        if override is not None:
            return override() if callable(override) else override

        # 3) Built-in defaults
        def new_id(prefix: str) -> str:
            return f"{prefix}-{_uuid.uuid4()}"

        upper_method = method.upper()

        # Credits endpoint
        if path.endswith("/credits") and upper_method == "GET":
            return {"remaining_credits": 1000, "total_credits_used": 0}

        # Feedback acknowledge
        if path.endswith("/feedback") and upper_method == "POST":
            return {"status": "success"}

        # Create-like endpoints (POST)
        if upper_method == "POST":
            if path.endswith("/crawl"):
                return {"crawl_id": new_id("mock-crawl")}
            elif path.endswith("/scheduled-jobs"):
                return {
                    "id": new_id("mock-job"),
                    "user_id": new_id("mock-user"),
                    "job_name": "Mock Scheduled Job",
                    "service_type": "smartscraper",
                    "cron_expression": "0 9 * * 1",
                    "job_config": {"mock": "config"},
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                    "next_run_at": "2024-01-08T09:00:00Z"
                }
            elif "/pause" in path:
                return {
                    "message": "Job paused successfully",
                    "job_id": new_id("mock-job"),
                    "is_active": False
                }
            elif "/resume" in path:
                return {
                    "message": "Job resumed successfully",
                    "job_id": new_id("mock-job"),
                    "is_active": True,
                    "next_run_at": "2024-01-08T09:00:00Z"
                }
            elif "/trigger" in path:
                return {
                    "execution_id": new_id("mock-task"),
                    "scheduled_job_id": new_id("mock-job"),
                    "triggered_at": "2024-01-01T00:00:00Z",
                    "message": f"Job triggered successfully. Task ID: {new_id('mock-task')}"
                }
            # All other POST endpoints return a request id
            return {"request_id": new_id("mock-req")}

        # Status-like endpoints (GET)
        if upper_method == "GET":
            if "markdownify" in path:
                return {"status": "completed", "content": "# Mock markdown\n\n..."}
            if "smartscraper" in path:
                return {"status": "completed", "result": [{"field": "value"}]}
            if "searchscraper" in path:
                return {
                    "status": "completed", 
                    "results": [{"url": "https://example.com"}],
                    "markdown_content": "# Mock Markdown Content\n\nThis is mock markdown content for testing purposes.\n\n## Section 1\n\nSome content here.\n\n## Section 2\n\nMore content here.",
                    "reference_urls": ["https://example.com", "https://example2.com"]
                }
            if "crawl" in path:
                return {"status": "completed", "pages": []}
            if "agentic-scrapper" in path:
                return {"status": "completed", "actions": []}
            if "scheduled-jobs" in path:
                if "/executions" in path:
                    return {
                        "executions": [
                            {
                                "id": new_id("mock-exec"),
                                "scheduled_job_id": new_id("mock-job"),
                                "execution_id": new_id("mock-task"),
                                "status": "completed",
                                "started_at": "2024-01-01T00:00:00Z",
                                "completed_at": "2024-01-01T00:01:00Z",
                                "result": {"mock": "result"},
                                "credits_used": 10
                            }
                        ],
                        "total": 1,
                        "page": 1,
                        "page_size": 20
                    }
                elif path.endswith("/scheduled-jobs"):  # List jobs endpoint
                    return {
                        "jobs": [
                            {
                                "id": new_id("mock-job"),
                                "user_id": new_id("mock-user"),
                                "job_name": "Mock Scheduled Job",
                                "service_type": "smartscraper",
                                "cron_expression": "0 9 * * 1",
                                "job_config": {"mock": "config"},
                                "is_active": True,
                                "created_at": "2024-01-01T00:00:00Z",
                                "updated_at": "2024-01-01T00:00:00Z",
                                "next_run_at": "2024-01-08T09:00:00Z"
                            }
                        ],
                        "total": 1,
                        "page": 1,
                        "page_size": 20
                    }
                else:  # Single job endpoint
                    return {
                        "id": new_id("mock-job"),
                        "user_id": new_id("mock-user"),
                        "job_name": "Mock Scheduled Job",
                        "service_type": "smartscraper",
                        "cron_expression": "0 9 * * 1",
                        "job_config": {"mock": "config"},
                        "is_active": True,
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "next_run_at": "2024-01-08T09:00:00Z"
                    }

        # Update operations (PATCH/PUT)
        if upper_method in ["PATCH", "PUT"] and "scheduled-jobs" in path:
            return {
                "id": new_id("mock-job"),
                "user_id": new_id("mock-user"),
                "job_name": "Updated Mock Scheduled Job",
                "service_type": "smartscraper",
                "cron_expression": "0 10 * * 1",
                "job_config": {"mock": "updated_config"},
                "is_active": True,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T01:00:00Z",
                "next_run_at": "2024-01-08T10:00:00Z"
            }

        # Delete operations
        if upper_method == "DELETE" and "scheduled-jobs" in path:
            return {"message": "Scheduled job deleted successfully"}

        # Generic fallback
        return {"status": "mock", "url": url, "method": method, "kwargs": kwargs}

    def markdownify(self, website_url: str, headers: Optional[dict[str, str]] = None, mock: bool = False, render_heavy_js: bool = False, stealth: bool = False):
        """Send a markdownify request"""
        logger.info(f"🔍 Starting markdownify request for {website_url}")
        if headers:
            logger.debug("🔧 Using custom headers")
        if stealth:
            logger.debug("🥷 Stealth mode enabled")
        if render_heavy_js:
            logger.debug("⚡ Heavy JavaScript rendering enabled")

        request = MarkdownifyRequest(website_url=website_url, headers=headers, mock=mock, render_heavy_js=render_heavy_js, stealth=stealth)
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/markdownify", json=request.model_dump()
        )
        logger.info("✨ Markdownify request completed successfully")
        return result

    def get_markdownify(self, request_id: str):
        """Get the result of a previous markdownify request"""
        logger.info(f"🔍 Fetching markdownify result for request {request_id}")

        # Validate input using Pydantic model
        GetMarkdownifyRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/markdownify/{request_id}")
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    def scrape(
        self,
        website_url: str,
        render_heavy_js: bool = False,
        headers: Optional[dict[str, str]] = None,
        mock:bool=False,
        stealth:bool=False,
    ):
        """Send a scrape request to get HTML content from a website

        Args:
            website_url: The URL of the website to get HTML from
            render_heavy_js: Whether to render heavy JavaScript (defaults to False)
            headers: Optional headers to send with the request
            stealth: Enable stealth mode to avoid bot detection
        """
        logger.info(f"🔍 Starting scrape request for {website_url}")
        logger.debug(f"🔧 Render heavy JS: {render_heavy_js}")
        if headers:
            logger.debug("🔧 Using custom headers")
        if stealth:
            logger.debug("🥷 Stealth mode enabled")

        request = ScrapeRequest(
            website_url=website_url,
            render_heavy_js=render_heavy_js,
            headers=headers,
            mock=mock,
            stealth=stealth
        )
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/scrape", json=request.model_dump()
        )
        logger.info("✨ Scrape request completed successfully")
        return result

    def get_scrape(self, request_id: str):
        """Get the result of a previous scrape request"""
        logger.info(f"🔍 Fetching scrape result for request {request_id}")

        # Validate input using Pydantic model
        GetScrapeRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/scrape/{request_id}")
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    def sitemap(
        self,
        website_url: str,
        mock: bool = False,
    ) -> SitemapResponse:
        """Extract all URLs from a website's sitemap.

        Automatically discovers sitemap from robots.txt or common sitemap locations.

        Args:
            website_url: The URL of the website to extract sitemap from
            mock: Whether to use mock mode for this request

        Returns:
            SitemapResponse: Object containing list of URLs extracted from sitemap

        Raises:
            ValueError: If website_url is invalid
            APIError: If the API request fails

        Examples:
            >>> client = Client(api_key="your-api-key")
            >>> response = client.sitemap("https://example.com")
            >>> print(f"Found {len(response.urls)} URLs")
            >>> for url in response.urls[:5]:
            ...     print(url)
        """
        logger.info(f"🗺️  Starting sitemap extraction for {website_url}")

        request = SitemapRequest(
            website_url=website_url,
            mock=mock
        )
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/sitemap", json=request.model_dump()
        )
        logger.info(f"✨ Sitemap extraction completed successfully - found {len(result.get('urls', []))} URLs")

        # Parse response into SitemapResponse model
        return SitemapResponse(**result)

    def smartscraper(
        self,
        user_prompt: str,
        website_url: Optional[str] = None,
        website_html: Optional[str] = None,
        website_markdown: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        output_schema: Optional[BaseModel] = None,
        number_of_scrolls: Optional[int] = None,
        total_pages: Optional[int] = None,
        mock: bool = False,
        plain_text: bool = False,
        render_heavy_js: bool = False,
        stealth: bool = False
    ):
        """
        Send a smartscraper request with optional pagination support and cookies.

        Supports three types of input (must provide exactly one):
        - website_url: Scrape from a URL
        - website_html: Process local HTML content
        - website_markdown: Process local Markdown content

        Args:
            user_prompt: Natural language prompt describing what to extract
            website_url: URL to scrape (optional)
            website_html: Raw HTML content to process (optional, max 2MB)
            website_markdown: Markdown content to process (optional, max 2MB)
            headers: Optional HTTP headers
            cookies: Optional cookies for authentication
            output_schema: Optional Pydantic model for structured output
            number_of_scrolls: Number of times to scroll (0-100)
            total_pages: Number of pages to scrape (1-10)
            mock: Enable mock mode for testing
            plain_text: Return plain text instead of structured data
            render_heavy_js: Enable heavy JavaScript rendering
            stealth: Enable stealth mode to avoid bot detection

        Returns:
            Dictionary containing the scraping results

        Raises:
            ValueError: If validation fails or invalid parameters provided
            APIError: If the API request fails
        """
        logger.info("🔍 Starting smartscraper request")
        if website_url:
            logger.debug(f"🌐 URL: {website_url}")
        if website_html:
            logger.debug("📄 Using provided HTML content")
        if website_markdown:
            logger.debug("📝 Using provided Markdown content")
        if headers:
            logger.debug("🔧 Using custom headers")
        if cookies:
            logger.debug("🍪 Using cookies for authentication/session management")
        if number_of_scrolls is not None:
            logger.debug(f"🔄 Number of scrolls: {number_of_scrolls}")
        if total_pages is not None:
            logger.debug(f"📄 Total pages to scrape: {total_pages}")
        if stealth:
            logger.debug("🥷 Stealth mode enabled")
        if render_heavy_js:
            logger.debug("⚡ Heavy JavaScript rendering enabled")
        logger.debug(f"📝 Prompt: {user_prompt}")

        request = SmartScraperRequest(
            website_url=website_url,
            website_html=website_html,
            website_markdown=website_markdown,
            headers=headers,
            cookies=cookies,
            user_prompt=user_prompt,
            output_schema=output_schema,
            number_of_scrolls=number_of_scrolls,
            total_pages=total_pages,
            mock=mock,
            plain_text=plain_text,
            render_heavy_js=render_heavy_js,
            stealth=stealth,
        )
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/smartscraper", json=request.model_dump()
        )
        logger.info("✨ Smartscraper request completed successfully")
        return result

    def get_smartscraper(self, request_id: str):
        """Get the result of a previous smartscraper request"""
        logger.info(f"🔍 Fetching smartscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSmartScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/smartscraper/{request_id}")
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    def submit_feedback(
        self, request_id: str, rating: int, feedback_text: Optional[str] = None
    ):
        """Submit feedback for a request"""
        logger.info(f"📝 Submitting feedback for request {request_id}")
        logger.debug(f"⭐ Rating: {rating}, Feedback: {feedback_text}")

        feedback = FeedbackRequest(
            request_id=request_id, rating=rating, feedback_text=feedback_text
        )
        logger.debug("✅ Feedback validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/feedback", json=feedback.model_dump()
        )
        logger.info("✨ Feedback submitted successfully")
        return result

    def get_credits(self):
        """Get credits information"""
        logger.info("💳 Fetching credits information")

        result = self._make_request(
            "GET",
            f"{API_BASE_URL}/credits",
        )
        logger.info(
            f"✨ Credits info retrieved: {result.get('remaining_credits')} "
            f"credits remaining"
        )
        return result

    def searchscraper(
        self,
        user_prompt: str,
        num_results: Optional[int] = 3,
        headers: Optional[dict[str, str]] = None,
        output_schema: Optional[BaseModel] = None,
        extraction_mode: bool = True,
        mock: bool=False,
        stealth: bool=False
    ):
        """Send a searchscraper request

        Args:
            user_prompt: The search prompt string
            num_results: Number of websites to scrape (3-20). Default is 3.
                        More websites provide better research depth but cost more
                        credits. Credit calculation: 30 base + 10 per additional
                        website beyond 3.
            headers: Optional headers to send with the request
            output_schema: Optional schema to structure the output
            extraction_mode: Whether to use AI extraction (True) or markdown conversion (False).
                           AI extraction costs 10 credits per page, markdown conversion costs 2 credits per page.
            stealth: Enable stealth mode to avoid bot detection
        """
        logger.info("🔍 Starting searchscraper request")
        logger.debug(f"📝 Prompt: {user_prompt}")
        logger.debug(f"🌐 Number of results: {num_results}")
        logger.debug(f"🤖 Extraction mode: {'AI extraction' if extraction_mode else 'Markdown conversion'}")
        if headers:
            logger.debug("🔧 Using custom headers")
        if stealth:
            logger.debug("🥷 Stealth mode enabled")

        request = SearchScraperRequest(
            user_prompt=user_prompt,
            num_results=num_results,
            headers=headers,
            output_schema=output_schema,
            extraction_mode=extraction_mode,
            mock=mock,
            stealth=stealth
        )
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/searchscraper", json=request.model_dump()
        )
        logger.info("✨ Searchscraper request completed successfully")
        return result

    def get_searchscraper(self, request_id: str):
        """Get the result of a previous searchscraper request"""
        logger.info(f"🔍 Fetching searchscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSearchScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/searchscraper/{request_id}")
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    def crawl(
        self,
        url: str,
        prompt: Optional[str] = None,
        data_schema: Optional[Dict[str, Any]] = None,
        extraction_mode: bool = True,
        cache_website: bool = True,
        depth: int = 2,
        max_pages: int = 2,
        same_domain_only: bool = True,
        batch_size: Optional[int] = None,
        sitemap: bool = False,
        headers: Optional[dict[str, str]] = None,
        render_heavy_js: bool = False,
        stealth: bool = False,
    ):
        """Send a crawl request with support for both AI extraction and
        markdown conversion modes"""
        logger.info("🔍 Starting crawl request")
        logger.debug(f"🌐 URL: {url}")
        logger.debug(
            f"🤖 Extraction mode: {'AI' if extraction_mode else 'Markdown conversion'}"
        )
        if extraction_mode:
            logger.debug(f"📝 Prompt: {prompt}")
            logger.debug(f"📊 Schema provided: {bool(data_schema)}")
        else:
            logger.debug(
                "📄 Markdown conversion mode - no AI processing, 2 credits per page"
            )
        logger.debug(f"💾 Cache website: {cache_website}")
        logger.debug(f"🔍 Depth: {depth}")
        logger.debug(f"📄 Max pages: {max_pages}")
        logger.debug(f"🏠 Same domain only: {same_domain_only}")
        logger.debug(f"🗺️ Use sitemap: {sitemap}")
        if stealth:
            logger.debug("🥷 Stealth mode enabled")
        if render_heavy_js:
            logger.debug("⚡ Heavy JavaScript rendering enabled")
        if batch_size is not None:
            logger.debug(f"📦 Batch size: {batch_size}")

        # Build request data, excluding None values
        request_data = {
            "url": url,
            "extraction_mode": extraction_mode,
            "cache_website": cache_website,
            "depth": depth,
            "max_pages": max_pages,
            "same_domain_only": same_domain_only,
            "sitemap": sitemap,
            "render_heavy_js": render_heavy_js,
            "stealth": stealth,
        }

        # Add optional parameters only if provided
        if prompt is not None:
            request_data["prompt"] = prompt
        if data_schema is not None:
            request_data["data_schema"] = data_schema
        if batch_size is not None:
            request_data["batch_size"] = batch_size
        if headers is not None:
            request_data["headers"] = headers

        request = CrawlRequest(**request_data)
        logger.debug("✅ Request validation passed")

        # Serialize the request, excluding None values
        request_json = request.model_dump(exclude_none=True)
        result = self._make_request("POST", f"{API_BASE_URL}/crawl", json=request_json)
        logger.info("✨ Crawl request completed successfully")
        return result

    def get_crawl(self, crawl_id: str):
        """Get the result of a previous crawl request"""
        logger.info(f"🔍 Fetching crawl result for request {crawl_id}")

        # Validate input using Pydantic model
        GetCrawlRequest(crawl_id=crawl_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/crawl/{crawl_id}")
        logger.info(f"✨ Successfully retrieved result for request {crawl_id}")
        return result

    def agenticscraper(
        self,
        url: str,
        steps: list[str],
        use_session: bool = True,
        user_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        ai_extraction: bool = False,
        mock: bool=False,
        stealth: bool=False,
    ):
        """Send an agentic scraper request to perform automated actions on a webpage

        Args:
            url: The URL to scrape
            steps: List of steps to perform on the webpage
            use_session: Whether to use session for the scraping (default: True)
            user_prompt: Prompt for AI extraction (required when ai_extraction=True)
            output_schema: Schema for structured data extraction (optional, used with ai_extraction=True)
            ai_extraction: Whether to use AI for data extraction from the scraped content (default: False)
            stealth: Enable stealth mode to avoid bot detection
        """
        logger.info(f"🤖 Starting agentic scraper request for {url}")
        logger.debug(f"🔧 Use session: {use_session}")
        logger.debug(f"📋 Steps: {steps}")
        logger.debug(f"🧠 AI extraction: {ai_extraction}")
        if ai_extraction:
            logger.debug(f"💭 User prompt: {user_prompt}")
            logger.debug(f"📋 Output schema provided: {output_schema is not None}")
        if stealth:
            logger.debug("🥷 Stealth mode enabled")

        request = AgenticScraperRequest(
            url=url,
            steps=steps,
            use_session=use_session,
            user_prompt=user_prompt,
            output_schema=output_schema,
            ai_extraction=ai_extraction,
            mock=mock,
            stealth=stealth
        )
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/agentic-scrapper", json=request.model_dump()
        )
        logger.info("✨ Agentic scraper request completed successfully")
        return result

    def get_agenticscraper(self, request_id: str):
        """Get the result of a previous agentic scraper request"""
        logger.info(f"🔍 Fetching agentic scraper result for request {request_id}")

        # Validate input using Pydantic model
        GetAgenticScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/agentic-scrapper/{request_id}")
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    def generate_schema(
        self,
        user_prompt: str,
        existing_schema: Optional[Dict[str, Any]] = None,
    ):
        """Generate a JSON schema from a user prompt
        
        Args:
            user_prompt: The user's search query to be refined into a schema
            existing_schema: Optional existing JSON schema to modify/extend
        """
        logger.info("🔧 Starting schema generation request")
        logger.debug(f"💭 User prompt: {user_prompt}")
        if existing_schema:
            logger.debug(f"📋 Existing schema provided: {existing_schema is not None}")

        request = GenerateSchemaRequest(
            user_prompt=user_prompt,
            existing_schema=existing_schema,
        )
        logger.debug("✅ Request validation passed")

        result = self._make_request(
            "POST", f"{API_BASE_URL}/generate_schema", json=request.model_dump()
        )
        logger.info("✨ Schema generation request completed successfully")
        return result

    def get_schema_status(self, request_id: str):
        """Get the status of a schema generation request
        
        Args:
            request_id: The request ID returned from generate_schema
        """
        logger.info(f"🔍 Fetching schema generation status for request {request_id}")

        # Validate input using Pydantic model
        GetSchemaStatusRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = self._make_request("GET", f"{API_BASE_URL}/generate_schema/{request_id}")
        logger.info(f"✨ Successfully retrieved schema status for request {request_id}")
        return result

    def create_scheduled_job(
        self,
        job_name: str,
        service_type: str,
        cron_expression: str,
        job_config: dict,
        is_active: bool = True,
    ):
        """Create a new scheduled job"""
        logger.info(f"📅 Creating scheduled job: {job_name}")

        request = ScheduledJobCreate(
            job_name=job_name,
            service_type=service_type,
            cron_expression=cron_expression,
            job_config=job_config,
            is_active=is_active,
        )

        result = self._make_request(
            "POST", f"{API_BASE_URL}/scheduled-jobs", json=request.model_dump()
        )
        logger.info("✨ Scheduled job created successfully")
        return result

    def get_scheduled_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        service_type: Optional[str] = None,
        is_active: Optional[bool] = None,
    ):
        """Get list of scheduled jobs with pagination"""
        logger.info("📋 Fetching scheduled jobs")

        GetScheduledJobsRequest(
            page=page,
            page_size=page_size,
            service_type=service_type,
            is_active=is_active,
        )

        params = {"page": page, "page_size": page_size}
        if service_type:
            params["service_type"] = service_type
        if is_active is not None:
            params["is_active"] = is_active

        result = self._make_request("GET", f"{API_BASE_URL}/scheduled-jobs", params=params)
        logger.info(f"✨ Successfully retrieved {len(result.get('jobs', []))} scheduled jobs")
        return result

    def get_scheduled_job(self, job_id: str):
        """Get details of a specific scheduled job"""
        logger.info(f"🔍 Fetching scheduled job {job_id}")

        GetScheduledJobRequest(job_id=job_id)

        result = self._make_request("GET", f"{API_BASE_URL}/scheduled-jobs/{job_id}")
        logger.info(f"✨ Successfully retrieved scheduled job {job_id}")
        return result

    def update_scheduled_job(
        self,
        job_id: str,
        job_name: Optional[str] = None,
        cron_expression: Optional[str] = None,
        job_config: Optional[dict] = None,
        is_active: Optional[bool] = None,
    ):
        """Update an existing scheduled job (partial update)"""
        logger.info(f"📝 Updating scheduled job {job_id}")

        update_data = {}
        if job_name is not None:
            update_data["job_name"] = job_name
        if cron_expression is not None:
            update_data["cron_expression"] = cron_expression
        if job_config is not None:
            update_data["job_config"] = job_config
        if is_active is not None:
            update_data["is_active"] = is_active

        ScheduledJobUpdate(**update_data)

        result = self._make_request(
            "PATCH", f"{API_BASE_URL}/scheduled-jobs/{job_id}", json=update_data
        )
        logger.info(f"✨ Successfully updated scheduled job {job_id}")
        return result

    def replace_scheduled_job(
        self,
        job_id: str,
        job_name: str,
        cron_expression: str,
        job_config: dict,
        is_active: bool = True,
    ):
        """Replace an existing scheduled job (full update)"""
        logger.info(f"🔄 Replacing scheduled job {job_id}")

        request_data = {
            "job_name": job_name,
            "cron_expression": cron_expression,
            "job_config": job_config,
            "is_active": is_active,
        }

        result = self._make_request(
            "PUT", f"{API_BASE_URL}/scheduled-jobs/{job_id}", json=request_data
        )
        logger.info(f"✨ Successfully replaced scheduled job {job_id}")
        return result

    def delete_scheduled_job(self, job_id: str):
        """Delete a scheduled job"""
        logger.info(f"🗑️ Deleting scheduled job {job_id}")

        JobActionRequest(job_id=job_id)

        result = self._make_request("DELETE", f"{API_BASE_URL}/scheduled-jobs/{job_id}")
        logger.info(f"✨ Successfully deleted scheduled job {job_id}")
        return result

    def pause_scheduled_job(self, job_id: str):
        """Pause a scheduled job"""
        logger.info(f"⏸️ Pausing scheduled job {job_id}")

        JobActionRequest(job_id=job_id)

        result = self._make_request("POST", f"{API_BASE_URL}/scheduled-jobs/{job_id}/pause")
        logger.info(f"✨ Successfully paused scheduled job {job_id}")
        return result

    def resume_scheduled_job(self, job_id: str):
        """Resume a paused scheduled job"""
        logger.info(f"▶️ Resuming scheduled job {job_id}")

        JobActionRequest(job_id=job_id)

        result = self._make_request("POST", f"{API_BASE_URL}/scheduled-jobs/{job_id}/resume")
        logger.info(f"✨ Successfully resumed scheduled job {job_id}")
        return result

    def trigger_scheduled_job(self, job_id: str):
        """Manually trigger a scheduled job"""
        logger.info(f"🚀 Manually triggering scheduled job {job_id}")

        TriggerJobRequest(job_id=job_id)

        result = self._make_request("POST", f"{API_BASE_URL}/scheduled-jobs/{job_id}/trigger")
        logger.info(f"✨ Successfully triggered scheduled job {job_id}")
        return result

    def get_job_executions(
        self,
        job_id: str,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
    ):
        """Get execution history for a scheduled job"""
        logger.info(f"📊 Fetching execution history for job {job_id}")

        GetJobExecutionsRequest(
            job_id=job_id,
            page=page,
            page_size=page_size,
            status=status,
        )

        params = {"page": page, "page_size": page_size}
        if status:
            params["status"] = status

        result = self._make_request(
            "GET", f"{API_BASE_URL}/scheduled-jobs/{job_id}/executions", params=params
        )
        logger.info(f"✨ Successfully retrieved execution history for job {job_id}")
        return result

    def close(self):
        """Close the session to free up resources"""
        logger.info("🔒 Closing Client session")
        self.session.close()
        logger.debug("✅ Session closed successfully")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
