import asyncio
from typing import Any, Optional, Dict

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
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
from scrapegraph_py.utils.helpers import handle_async_response, validate_api_key


class AsyncClient:
    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize AsyncClient using API key from environment variable.

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
        """Initialize AsyncClient with configurable parameters.

        Args:
            api_key: API key for authentication. If None, will try to load from environment
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds. None means no timeout (infinite)
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        logger.info("🔑 Initializing AsyncClient")

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
            f"🛠️ Configuration: verify_ssl={verify_ssl}, timeout={timeout}, max_retries={max_retries}"
        )
        self.api_key = api_key
        self.headers = {**DEFAULT_HEADERS, "SGAI-APIKEY": api_key}
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        ssl = None if verify_ssl else False
        self.timeout = ClientTimeout(total=timeout) if timeout is not None else None

        self.session = ClientSession(
            headers=self.headers, connector=TCPConnector(ssl=ssl), timeout=self.timeout
        )

        logger.info("✅ AsyncClient initialized successfully")

    async def _make_request(self, method: str, url: str, **kwargs) -> Any:
        """Make HTTP request with retry logic."""
        for attempt in range(self.max_retries):
            try:
                logger.info(
                    f"🚀 Making {method} request to {url} (Attempt {attempt + 1}/{self.max_retries})"
                )
                logger.debug(f"🔍 Request parameters: {kwargs}")

                async with self.session.request(method, url, **kwargs) as response:
                    logger.debug(f"📥 Response status: {response.status}")
                    result = await handle_async_response(response)
                    logger.info(f"✅ Request completed successfully: {method} {url}")
                    return result

            except ClientError as e:
                logger.warning(f"⚠️ Request attempt {attempt + 1} failed: {str(e)}")
                if hasattr(e, "status") and e.status is not None:
                    try:
                        error_data = await e.response.json()
                        error_msg = error_data.get("error", str(e))
                        logger.error(f"🔴 API Error: {error_msg}")
                        raise APIError(error_msg, status_code=e.status)
                    except ValueError:
                        logger.error("🔴 Could not parse error response")
                        raise APIError(
                            str(e),
                            status_code=e.status if hasattr(e, "status") else None,
                        )

                if attempt == self.max_retries - 1:
                    logger.error(f"❌ All retry attempts failed for {method} {url}")
                    raise ConnectionError(f"Failed to connect to API: {str(e)}")

                retry_delay = self.retry_delay * (attempt + 1)
                logger.info(f"⏳ Waiting {retry_delay}s before retry {attempt + 2}")
                await asyncio.sleep(retry_delay)

    async def markdownify(
        self, website_url: str, headers: Optional[dict[str, str]] = None
    ):
        """Send a markdownify request"""
        logger.info(f"🔍 Starting markdownify request for {website_url}")
        if headers:
            logger.debug("🔧 Using custom headers")

        request = MarkdownifyRequest(website_url=website_url, headers=headers)
        logger.debug("✅ Request validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/markdownify", json=request.model_dump()
        )
        logger.info("✨ Markdownify request completed successfully")
        return result

    async def get_markdownify(self, request_id: str):
        """Get the result of a previous markdownify request"""
        logger.info(f"🔍 Fetching markdownify result for request {request_id}")

        # Validate input using Pydantic model
        GetMarkdownifyRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request(
            "GET", f"{API_BASE_URL}/markdownify/{request_id}"
        )
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    async def smartscraper(
        self,
        user_prompt: str,
        website_url: Optional[str] = None,
        website_html: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        output_schema: Optional[BaseModel] = None,
        number_of_scrolls: Optional[int] = None,
    ):
        """Send a smartscraper request"""
        logger.info("🔍 Starting smartscraper request")
        if website_url:
            logger.debug(f"🌐 URL: {website_url}")
        if website_html:
            logger.debug("📄 Using provided HTML content")
        if headers:
            logger.debug("🔧 Using custom headers")
        if number_of_scrolls is not None:
            logger.debug(f"🔄 Number of scrolls: {number_of_scrolls}")
        logger.debug(f"📝 Prompt: {user_prompt}")

        request = SmartScraperRequest(
            website_url=website_url,
            website_html=website_html,
            headers=headers,
            user_prompt=user_prompt,
            output_schema=output_schema,
            number_of_scrolls=number_of_scrolls,
        )

        logger.debug("✅ Request validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/smartscraper", json=request.model_dump()
        )
        logger.info("✨ Smartscraper request completed successfully")
        return result

    async def get_smartscraper(self, request_id: str):
        """Get the result of a previous smartscraper request"""
        logger.info(f"🔍 Fetching smartscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSmartScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request(
            "GET", f"{API_BASE_URL}/smartscraper/{request_id}"
        )
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    async def submit_feedback(
        self, request_id: str, rating: int, feedback_text: Optional[str] = None
    ):
        """Submit feedback for a request"""
        logger.info(f"📝 Submitting feedback for request {request_id}")
        logger.debug(f"⭐ Rating: {rating}, Feedback: {feedback_text}")

        feedback = FeedbackRequest(
            request_id=request_id, rating=rating, feedback_text=feedback_text
        )
        logger.debug("✅ Feedback validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/feedback", json=feedback.model_dump()
        )
        logger.info("✨ Feedback submitted successfully")
        return result

    async def get_credits(self):
        """Get credits information"""
        logger.info("💳 Fetching credits information")

        result = await self._make_request(
            "GET",
            f"{API_BASE_URL}/credits",
        )
        logger.info(
            f"✨ Credits info retrieved: {result.get('remaining_credits')} credits remaining"
        )
        return result

    async def searchscraper(
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
                        More websites provide better research depth but cost more credits.
                        Credit calculation: 30 base + 10 per additional website beyond 3.
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

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/searchscraper", json=request.model_dump()
        )
        logger.info("✨ Searchscraper request completed successfully")
        return result

    async def get_searchscraper(self, request_id: str):
        """Get the result of a previous searchscraper request"""
        logger.info(f"🔍 Fetching searchscraper result for request {request_id}")

        # Validate input using Pydantic model
        GetSearchScraperRequest(request_id=request_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request(
            "GET", f"{API_BASE_URL}/searchscraper/{request_id}"
        )
        logger.info(f"✨ Successfully retrieved result for request {request_id}")
        return result

    async def crawl(
        self,
        url: str,
        prompt: str,
        data_schema: Dict[str, Any],
        cache_website: bool = True,
        depth: int = 2,
        max_pages: int = 2,
        same_domain_only: bool = True,
        batch_size: int = 1,
    ):
        """Send a crawl request"""
        logger.info("🔍 Starting crawl request")
        logger.debug(f"🌐 URL: {url}")
        logger.debug(f"📝 Prompt: {prompt}")
        logger.debug(f"📊 Schema provided: {bool(data_schema)}")
        logger.debug(f"💾 Cache website: {cache_website}")
        logger.debug(f"🔍 Depth: {depth}")
        logger.debug(f"📄 Max pages: {max_pages}")
        logger.debug(f"🏠 Same domain only: {same_domain_only}")
        logger.debug(f"📦 Batch size: {batch_size}")

        request = CrawlRequest(
            url=url,
            prompt=prompt,
            data_schema=data_schema,
            cache_website=cache_website,
            depth=depth,
            max_pages=max_pages,
            same_domain_only=same_domain_only,
            batch_size=batch_size,
        )
        logger.debug("✅ Request validation passed")

        result = await self._make_request(
            "POST", f"{API_BASE_URL}/crawl", json=request.model_dump()
        )
        logger.info("✨ Crawl request completed successfully")
        return result

    async def get_crawl(self, crawl_id: str):
        """Get the result of a previous crawl request"""
        logger.info(f"🔍 Fetching crawl result for request {crawl_id}")

        # Validate input using Pydantic model
        GetCrawlRequest(crawl_id=crawl_id)
        logger.debug("✅ Request ID validation passed")

        result = await self._make_request("GET", f"{API_BASE_URL}/crawl/{crawl_id}")
        logger.info(f"✨ Successfully retrieved result for request {crawl_id}")
        return result

    async def close(self):
        """Close the session to free up resources"""
        logger.info("🔒 Closing AsyncClient session")
        await self.session.close()
        logger.debug("✅ Session closed successfully")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
