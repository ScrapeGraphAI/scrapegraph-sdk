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

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
from scrapegraph_py.models.shared import FetchConfig
from scrapegraph_py.utils.helpers import handle_async_response, validate_api_key
from scrapegraph_py.utils.request_builders import (
    build_crawl_payload,
    build_extract_payload,
    build_history_params,
    build_monitor_payload,
    build_schema_payload,
    build_scrape_payload,
    build_search_payload,
    build_validate_params,
)


class _AsyncCrawlNamespace:
    """Namespaced async crawl operations."""

    def __init__(self, client: "AsyncClient"):
        self._client = client

    async def start(
        self,
        url: str,
        depth: Optional[int] = None,
        max_pages: int = 10,
        format: str = "markdown",
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
        fetch_config: Optional[FetchConfig] = None,
        formats: Optional[List[Dict[str, Any]]] = None,
        max_depth: Optional[int] = None,
        max_links_per_page: int = 10,
        allow_external: bool = False,
        content_types: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Start a crawl job."""
        logger.info(f"Starting crawl for {url}")
        return await self._client._make_request(
            "POST",
            f"{self._client.base_url}/crawl",
            json=build_crawl_payload(
                url,
                depth=depth,
                max_pages=max_pages,
                format=format,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                fetch_config=fetch_config,
                formats=formats,
                max_depth=max_depth,
                max_links_per_page=max_links_per_page,
                allow_external=allow_external,
                content_types=content_types,
            ),
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
        name: Optional[str],
        url: str,
        prompt: Optional[str],
        interval: str,
        fetch_config: Optional[FetchConfig] = None,
        schema: Optional[Any] = None,
        formats: Optional[List[Dict[str, Any]]] = None,
        webhook_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new monitor."""
        logger.info(f"Creating monitor '{name}' for {url}")
        return await self._client._make_request(
            "POST",
            f"{self._client.base_url}/monitor",
            json=build_monitor_payload(
                name=name,
                url=url,
                prompt=prompt,
                interval=interval,
                fetch_config=fetch_config,
                schema=schema,
                formats=formats,
                webhook_url=webhook_url,
            ),
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
        api_key: Optional[str] = None,
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
        formats: Optional[List[Dict[str, Any]]] = None,
        content_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Scrape a page and return it in the specified format.

        Args:
            url: URL to scrape
            format: Legacy single output format
            fetch_config: Fetch configuration options
        """
        logger.info(f"Scraping {url} (format={format})")
        return await self._make_request(
            "POST",
            f"{self.base_url}/scrape",
            json=build_scrape_payload(
                url,
                format=format,
                fetch_config=fetch_config,
                formats=formats,
                content_type=content_type,
            ),
        )

    # ------------------------------------------------------------------
    # Extract  (replaces SmartScraper)
    # ------------------------------------------------------------------

    async def extract(
        self,
        url: Optional[str],
        prompt: str,
        fetch_config: Optional[FetchConfig] = None,
        *,
        schema: Optional[Any] = None,
        mode: str = "normal",
        content_type: Optional[str] = None,
        html: Optional[str] = None,
        markdown: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Extract structured data from a page using AI.

        Args:
            url: URL to extract data from
            prompt: Natural language prompt describing what to extract
            fetch_config: Fetch configuration options
        """
        logger.info(f"Extracting from {url}")
        return await self._make_request(
            "POST",
            f"{self.base_url}/extract",
            json=build_extract_payload(
                url=url,
                prompt=prompt,
                fetch_config=fetch_config,
                schema=schema,
                mode=mode,
                content_type=content_type,
                html=html,
                markdown=markdown,
            ),
        )

    # ------------------------------------------------------------------
    # Search  (replaces SearchScraper)
    # ------------------------------------------------------------------

    async def search(
        self,
        query: str,
        num_results: int = 5,
        location_geo_code: Optional[str] = None,
        *,
        schema: Optional[Any] = None,
        prompt: Optional[str] = None,
        format: str = "markdown",
        mode: str = "prune",
        fetch_config: Optional[FetchConfig] = None,
        time_range: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Search the web and extract structured results.

        Args:
            query: The search query
            num_results: Number of results (3-20, default 5)
            location_geo_code: Geo code for geo-targeted results
        """
        logger.info(f"Searching: {query}")
        return await self._make_request(
            "POST",
            f"{self.base_url}/search",
            json=build_search_payload(
                query=query,
                num_results=num_results,
                location_geo_code=location_geo_code,
                schema=schema,
                prompt=prompt,
                format=format,
                mode=mode,
                fetch_config=fetch_config,
                time_range=time_range,
            ),
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
        *,
        page: Optional[int] = None,
        service: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve request history.

        Args:
            endpoint: Legacy alias for service
            status: Unsupported in SGAI v2
            limit: Maximum number of results (1-100)
            offset: Legacy alias mapped onto page when possible
        """
        logger.info("Fetching history")
        return await self._make_request(
            "GET",
            f"{self.base_url}/history",
            params=build_history_params(
                endpoint=endpoint,
                status=status,
                limit=limit,
                offset=offset,
                page=page,
                service=service,
            )
            or None,
        )

    # ------------------------------------------------------------------
    # Schema / Validate
    # ------------------------------------------------------------------

    async def schema(
        self,
        prompt: str,
        existing_schema: Optional[Any] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate or refine a JSON schema from a prompt."""
        logger.info("Generating schema")
        return await self._make_request(
            "POST",
            f"{self.base_url}/schema",
            json=build_schema_payload(
                prompt, existing_schema=existing_schema, model=model
            ),
        )

    async def validate(self, email: str) -> Dict[str, Any]:
        """Validate an email address against SGAI's allowlist endpoint."""
        logger.info("Validating email")
        return await self._make_request(
            "GET", f"{self.base_url}/validate", params=build_validate_params(email)
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
