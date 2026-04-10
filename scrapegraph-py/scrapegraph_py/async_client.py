"""
Asynchronous HTTP client for the ScrapeGraphAI v2 API.

Example:
    >>> import asyncio
    >>> from scrapegraph_py import AsyncClient
    >>> async def main():
    ...     async with AsyncClient(api_key="sgai-...") as client:
    ...         result = await client.extract(
    ...             url="https://example.com",
    ...             prompt="Extract product information"
    ...         )
    ...         print(result)
    >>> asyncio.run(main())
"""

import asyncio
from typing import Any, Dict, List, Optional

from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.client_exceptions import ClientError
from pydantic import BaseModel

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
from scrapegraph_py.models.crawl import CrawlFormat, CrawlRequest
from scrapegraph_py.models.extract import ExtractRequest
from scrapegraph_py.models.history import HistoryFilter
from scrapegraph_py.models.monitor import MonitorCreateRequest
from scrapegraph_py.models.scrape import ScrapeFormat, ScrapeRequest
from scrapegraph_py.models.search import SearchRequest
from scrapegraph_py.models.shared import FetchConfig, LlmConfig
from scrapegraph_py.utils.helpers import handle_async_response, validate_api_key


class _AsyncCrawlNamespace:
    """Namespaced async crawl operations."""

    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def start(
        self,
        url: str,
        depth: int = 2,
        max_pages: int = 10,
        format: str = "markdown",
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        fetch_config: Optional[FetchConfig] = None,
    ) -> Dict[str, Any]:
        """Start a crawl job."""
        logger.info(f"Starting crawl for {url}")
        request = CrawlRequest(
            url=url,
            depth=depth,
            max_pages=max_pages,
            format=CrawlFormat(format),
            include_patterns=include_patterns,
            exclude_patterns=exclude_patterns,
            fetch_config=fetch_config,
        )
        return await self._client._make_request(
            "POST", f"{self._client.base_url}/crawl", json=request.model_dump()
        )

    async def status(self, crawl_id: str) -> Dict[str, Any]:
        """Get crawl job status and results."""
        logger.info(f"Fetching crawl status for {crawl_id}")
        return await self._client._make_request(
            "GET", f"{self._client.base_url}/crawl/{crawl_id}"
        )

    async def stop(self, crawl_id: str) -> Dict[str, Any]:
        """Stop a running crawl job."""
        logger.info(f"Stopping crawl {crawl_id}")
        return await self._client._make_request(
            "POST", f"{self._client.base_url}/crawl/{crawl_id}/stop"
        )

    async def resume(self, crawl_id: str) -> Dict[str, Any]:
        """Resume a stopped crawl job."""
        logger.info(f"Resuming crawl {crawl_id}")
        return await self._client._make_request(
            "POST", f"{self._client.base_url}/crawl/{crawl_id}/resume"
        )


class _AsyncMonitorNamespace:
    """Namespaced async monitor operations."""

    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def create(
        self,
        name: str,
        url: str,
        prompt: str,
        interval: str,
        output_schema: Optional[Dict[str, Any]] = None,
        fetch_config: Optional[FetchConfig] = None,
        llm_config: Optional[LlmConfig] = None,
    ) -> Dict[str, Any]:
        """Create a new monitor."""
        logger.info(f"Creating monitor '{name}' for {url}")
        request = MonitorCreateRequest(
            name=name,
            url=url,
            prompt=prompt,
            interval=interval,
            output_schema=output_schema,
            fetch_config=fetch_config,
            llm_config=llm_config,
        )
        return await self._client._make_request(
            "POST", f"{self._client.base_url}/monitor", json=request.model_dump()
        )

    async def list(self) -> Dict[str, Any]:
        """List all monitors."""
        logger.info("Listing monitors")
        return await self._client._make_request(
            "GET", f"{self._client.base_url}/monitor"
        )

    async def get(self, monitor_id: str) -> Dict[str, Any]:
        """Get a specific monitor."""
        logger.info(f"Fetching monitor {monitor_id}")
        return await self._client._make_request(
            "GET", f"{self._client.base_url}/monitor/{monitor_id}"
        )

    async def pause(self, monitor_id: str) -> Dict[str, Any]:
        """Pause a monitor."""
        logger.info(f"Pausing monitor {monitor_id}")
        return await self._client._make_request(
            "POST", f"{self._client.base_url}/monitor/{monitor_id}/pause"
        )

    async def resume(self, monitor_id: str) -> Dict[str, Any]:
        """Resume a paused monitor."""
        logger.info(f"Resuming monitor {monitor_id}")
        return await self._client._make_request(
            "POST", f"{self._client.base_url}/monitor/{monitor_id}/resume"
        )

    async def delete(self, monitor_id: str) -> Dict[str, Any]:
        """Delete a monitor."""
        logger.info(f"Deleting monitor {monitor_id}")
        return await self._client._make_request(
            "DELETE", f"{self._client.base_url}/monitor/{monitor_id}"
        )


class AsyncClient:
    """Asynchronous client for the ScrapeGraphAI v2 API.

    Example:
        >>> async with AsyncClient(api_key="sgai-...") as client:
        ...     result = await client.scrape("https://example.com")
        ...     result = await client.extract("https://example.com", prompt="Extract prices")
        ...     job = await client.crawl.start("https://example.com", depth=3)
    """

    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> "AsyncClient":
        """Initialize AsyncClient using SGAI_API_KEY environment variable."""
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
        base_url: Optional[str] = None,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """Initialize AsyncClient.

        Args:
            api_key: API key for authentication. If None, reads from SGAI_API_KEY env var
            base_url: Override the default API base URL
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds (None = no timeout)
            max_retries: Maximum retry attempts on server errors
            retry_delay: Base delay between retries in seconds
        """
        logger.info("Initializing AsyncClient")

        if api_key is None:
            from os import getenv

            api_key = getenv("SGAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "SGAI_API_KEY not provided and not found in environment"
                )

        validate_api_key(api_key)

        self.api_key = api_key
        self.base_url = (base_url or API_BASE_URL).rstrip("/")
        self.headers = {
            **DEFAULT_HEADERS,
            "Authorization": f"Bearer {api_key}",
            "SGAI-APIKEY": api_key,
        }
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        ssl = None if verify_ssl else False
        self.timeout = ClientTimeout(total=timeout) if timeout is not None else None

        self.session = ClientSession(
            headers=self.headers,
            connector=TCPConnector(ssl=ssl),
            timeout=self.timeout,
        )

        # Namespaced sub-clients
        self.crawl = _AsyncCrawlNamespace(self)
        self.monitor = _AsyncMonitorNamespace(self)

        logger.info("AsyncClient initialized successfully")

    async def _make_request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Make async HTTP request with retry logic."""
        for attempt in range(self.max_retries):
            try:
                logger.debug(
                    f"Making {method} request to {url} "
                    f"(attempt {attempt + 1}/{self.max_retries})"
                )
                async with self.session.request(method, url, **kwargs) as response:
                    return await handle_async_response(response)

            except ClientError as e:
                logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                if hasattr(e, "status") and e.status is not None:
                    try:
                        error_data = await e.response.json()
                        error_msg = error_data.get("error", str(e))
                        raise APIError(error_msg, status_code=e.status)
                    except (ValueError, AttributeError):
                        raise APIError(
                            str(e),
                            status_code=getattr(e, "status", None),
                        )

                if attempt == self.max_retries - 1:
                    raise ConnectionError(f"Failed to connect to API: {e}")

                retry_delay = self.retry_delay * (attempt + 1)
                logger.info(f"Waiting {retry_delay}s before retry {attempt + 2}")
                await asyncio.sleep(retry_delay)

    # ------------------------------------------------------------------
    # Scrape
    # ------------------------------------------------------------------

    async def scrape(
        self,
        url: str,
        format: str = "markdown",
        fetch_config: Optional[FetchConfig] = None,
    ) -> Dict[str, Any]:
        """Scrape a page and return it in the specified format.

        Args:
            url: URL to scrape
            format: Output format - 'markdown', 'html', 'screenshot', or 'branding'
            fetch_config: Fetch configuration options
        """
        logger.info(f"Scraping {url} (format={format})")
        request = ScrapeRequest(
            url=url,
            format=ScrapeFormat(format),
            fetch_config=fetch_config,
        )
        return await self._make_request(
            "POST", f"{self.base_url}/scrape", json=request.model_dump()
        )

    # ------------------------------------------------------------------
    # Extract  (replaces SmartScraper)
    # ------------------------------------------------------------------

    async def extract(
        self,
        url: str,
        prompt: str,
        output_schema: Optional[Any] = None,
        fetch_config: Optional[FetchConfig] = None,
        llm_config: Optional[LlmConfig] = None,
    ) -> Dict[str, Any]:
        """Extract structured data from a page using AI.

        Args:
            url: URL to extract data from
            prompt: Natural language prompt describing what to extract
            output_schema: JSON Schema dict or Pydantic BaseModel class for output structure
            fetch_config: Fetch configuration options
            llm_config: LLM configuration options
        """
        logger.info(f"Extracting from {url}")

        schema_dict = None
        if output_schema is not None:
            if isinstance(output_schema, type) and issubclass(output_schema, BaseModel):
                schema_dict = output_schema.model_json_schema()
            elif isinstance(output_schema, dict):
                schema_dict = output_schema
            else:
                raise ValueError(
                    "output_schema must be a dict (JSON Schema) or a Pydantic BaseModel class"
                )

        request = ExtractRequest(
            url=url,
            prompt=prompt,
            output_schema=schema_dict,
            fetch_config=fetch_config,
            llm_config=llm_config,
        )
        return await self._make_request(
            "POST", f"{self.base_url}/extract", json=request.model_dump()
        )

    # ------------------------------------------------------------------
    # Search  (replaces SearchScraper)
    # ------------------------------------------------------------------

    async def search(
        self,
        query: str,
        num_results: int = 5,
        output_schema: Optional[Any] = None,
        location_geo_code: Optional[str] = None,
        llm_config: Optional[LlmConfig] = None,
    ) -> Dict[str, Any]:
        """Search the web and extract structured results.

        Args:
            query: The search query
            num_results: Number of results (3-20, default 5)
            output_schema: JSON Schema dict or Pydantic BaseModel class for output structure
            location_geo_code: Two-letter country code for geo-targeted results (e.g. 'us', 'gb')
            llm_config: LLM configuration options
        """
        logger.info(f"Searching: {query}")

        schema_dict = None
        if output_schema is not None:
            if isinstance(output_schema, type) and issubclass(output_schema, BaseModel):
                schema_dict = output_schema.model_json_schema()
            elif isinstance(output_schema, dict):
                schema_dict = output_schema
            else:
                raise ValueError(
                    "output_schema must be a dict (JSON Schema) or a Pydantic BaseModel class"
                )

        request = SearchRequest(
            query=query,
            num_results=num_results,
            output_schema=schema_dict,
            location_geo_code=location_geo_code,
            llm_config=llm_config,
        )
        return await self._make_request(
            "POST", f"{self.base_url}/search", json=request.model_dump()
        )

    # ------------------------------------------------------------------
    # Credits
    # ------------------------------------------------------------------

    async def credits(self) -> Dict[str, Any]:
        """Get remaining API credits."""
        logger.info("Fetching credits")
        return await self._make_request("GET", f"{self.base_url}/credits")

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    async def history(
        self,
        endpoint: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Retrieve request history.

        Args:
            endpoint: Filter by endpoint name (e.g. 'scrape', 'extract')
            status: Filter by request status
            limit: Maximum number of results (1-100)
            offset: Number of results to skip
        """
        logger.info("Fetching history")
        filter_obj = HistoryFilter(
            endpoint=endpoint, status=status, limit=limit, offset=offset
        )
        params = filter_obj.to_params()
        return await self._make_request(
            "GET", f"{self.base_url}/history", params=params or None
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def close(self) -> None:
        """Close the HTTP session."""
        logger.info("Closing AsyncClient session")
        await self.session.close()

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
