# Client implementation goes here
from typing import Any, Dict, Optional

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
from scrapegraph_py.models.searchscraper import (
    GetSearchScraperRequest,
    SearchScraperRequest,
)
from scrapegraph_py.models.smartscraper import (
    GetSmartScraperRequest,
    SmartScraperRequest,
)
from scrapegraph_py.utils.helpers import handle_sync_response, validate_api_key


class Client:
    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize Client using API key from environment variable.

        Args:
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        from os import getenv

        api_key = getenv("SGAI_API_KEY")
        if not api_key:
            raise ValueError("SGAI_API_KEY environment variable not set")
        return cls(
            api_key=api_key,
            verify_ssl=verify_ssl,
            timeout=timeout,
            max_retries=max_retries,
            retry_delay=retry_delay,
        )

    def __init__(
        self,
        api_key: str = None,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize Client with configurable parameters.

        Args:
            api_key: API key for authentication. If None, will try to load
                     from environment
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
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
        """Make HTTP request with error handling."""
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

    def markdownify(self, website_url: str, headers: Optional[dict[str, str]] = None):
        """Send a markdownify request"""
        logger.info(f"🔍 Starting markdownify request for {website_url}")
        if headers:
            logger.debug("🔧 Using custom headers")

        request = MarkdownifyRequest(website_url=website_url, headers=headers)
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

    def smartscraper(
        self,
        user_prompt: str,
        website_url: Optional[str] = None,
        website_html: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        output_schema: Optional[BaseModel] = None,
        number_of_scrolls: Optional[int] = None,
        total_pages: Optional[int] = None,
    ):
        """Send a smartscraper request with optional pagination support and cookies"""
        logger.info("🔍 Starting smartscraper request")
        if website_url:
            logger.debug(f"🌐 URL: {website_url}")
        if website_html:
            logger.debug("📄 Using provided HTML content")
        if headers:
            logger.debug("🔧 Using custom headers")
        if cookies:
            logger.debug("🍪 Using cookies for authentication/session management")
        if number_of_scrolls is not None:
            logger.debug(f"🔄 Number of scrolls: {number_of_scrolls}")
        if total_pages is not None:
            logger.debug(f"📄 Total pages to scrape: {total_pages}")
        logger.debug(f"📝 Prompt: {user_prompt}")

        request = SmartScraperRequest(
            website_url=website_url,
            website_html=website_html,
            headers=headers,
            cookies=cookies,
            user_prompt=user_prompt,
            output_schema=output_schema,
            number_of_scrolls=number_of_scrolls,
            total_pages=total_pages,
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
        """
        logger.info("🔍 Starting searchscraper request")
        logger.debug(f"📝 Prompt: {user_prompt}")
        logger.debug(f"🌐 Number of results: {num_results}")
        if headers:
            logger.debug("🔧 Using custom headers")

        request = SearchScraperRequest(
            user_prompt=user_prompt,
            num_results=num_results,
            headers=headers,
            output_schema=output_schema,
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
        }

        # Add optional parameters only if provided
        if prompt is not None:
            request_data["prompt"] = prompt
        if data_schema is not None:
            request_data["data_schema"] = data_schema
        if batch_size is not None:
            request_data["batch_size"] = batch_size

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
    ):
        """Send an agentic scraper request to perform automated actions on a webpage
        
        Args:
            url: The URL to scrape
            steps: List of steps to perform on the webpage
            use_session: Whether to use session for the scraping (default: True)
            user_prompt: Prompt for AI extraction (required when ai_extraction=True)
            output_schema: Schema for structured data extraction (optional, used with ai_extraction=True)
            ai_extraction: Whether to use AI for data extraction from the scraped content (default: False)
        """
        logger.info(f"🤖 Starting agentic scraper request for {url}")
        logger.debug(f"🔧 Use session: {use_session}")
        logger.debug(f"📋 Steps: {steps}")
        logger.debug(f"🧠 AI extraction: {ai_extraction}")
        if ai_extraction:
            logger.debug(f"💭 User prompt: {user_prompt}")
            logger.debug(f"📋 Output schema provided: {output_schema is not None}")

        request = AgenticScraperRequest(
            url=url,
            steps=steps,
            use_session=use_session,
            user_prompt=user_prompt,
            output_schema=output_schema,
            ai_extraction=ai_extraction,
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

    def close(self):
        """Close the session to free up resources"""
        logger.info("🔒 Closing Client session")
        self.session.close()
        logger.debug("✅ Session closed successfully")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
