"""
Synchronous HTTP client for the ScrapeGraphAI v2 API.

Example:
    >>> from scrapegraph_py import Client
    >>> client = Client(api_key="sgai-...")
    >>> result = client.extract(
    ...     url="https://example.com",
    ...     prompt="Extract product information"
    ... )
    >>> print(result)

    >>> # Namespaced crawl/monitor
    >>> job = client.crawl.start("https://example.com", depth=3)
    >>> status = client.crawl.status(job["id"])
"""

from typing import Any, Dict, List, Optional

import requests
import urllib3
from requests.exceptions import RequestException

from scrapegraph_py.config import API_BASE_URL, DEFAULT_HEADERS
from scrapegraph_py.exceptions import APIError
from scrapegraph_py.logger import sgai_logger as logger
from scrapegraph_py.models.shared import FetchConfig, LlmConfig
from scrapegraph_py.utils.helpers import handle_sync_response, validate_api_key
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


class _CrawlNamespace:
    """Namespaced crawl operations: client.crawl.start(), .status(), .stop(), .resume()."""

    def __init__(self, client: "Client"):
        self._client = client

    def start(
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
        """Start a crawl job.

        Args:
            url: The starting URL for the crawl
            depth: Legacy alias for max_depth
            max_pages: Maximum pages to crawl
            format: Legacy single output format
            include_patterns: URL patterns to include
            exclude_patterns: URL patterns to exclude
            fetch_config: Fetch configuration options
        """
        logger.info(f"Starting crawl for {url}")
        return self._client._make_request(
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

    def status(self, crawl_id: str) -> Dict[str, Any]:
        """Get crawl job status and results.

        Args:
            crawl_id: The crawl job ID
        """
        logger.info(f"Fetching crawl status for {crawl_id}")
        return self._client._make_request(
            "GET", f"{self._client.base_url}/crawl/{crawl_id}"
        )

    def stop(self, crawl_id: str) -> Dict[str, Any]:
        """Stop a running crawl job.

        Args:
            crawl_id: The crawl job ID to stop
        """
        logger.info(f"Stopping crawl {crawl_id}")
        return self._client._make_request(
            "POST", f"{self._client.base_url}/crawl/{crawl_id}/stop"
        )

    def resume(self, crawl_id: str) -> Dict[str, Any]:
        """Resume a stopped crawl job.

        Args:
            crawl_id: The crawl job ID to resume
        """
        logger.info(f"Resuming crawl {crawl_id}")
        return self._client._make_request(
            "POST", f"{self._client.base_url}/crawl/{crawl_id}/resume"
        )


class _MonitorNamespace:
    """Namespaced monitor operations: client.monitor.create(), .list(), .get(), etc."""

    def __init__(self, client: "Client"):
        self._client = client

    def create(
        self,
        name: Optional[str],
        url: str,
        prompt: Optional[str],
        interval: str,
        output_schema: Optional[Dict[str, Any]] = None,
        fetch_config: Optional[FetchConfig] = None,
        llm_config: Optional[LlmConfig] = None,
        schema: Optional[Any] = None,
        formats: Optional[List[Dict[str, Any]]] = None,
        webhook_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new monitor.

        Args:
            name: Name of the monitor
            url: URL to monitor
            prompt: Legacy prompt for JSON extraction monitors
            interval: Cron expression (5 fields)
            output_schema: Legacy alias for schema
            fetch_config: Fetch configuration options
            llm_config: LLM configuration options for JSON formats
        """
        logger.info(f"Creating monitor '{name}' for {url}")
        return self._client._make_request(
            "POST",
            f"{self._client.base_url}/monitor",
            json=build_monitor_payload(
                name=name,
                url=url,
                prompt=prompt,
                interval=interval,
                output_schema=output_schema,
                fetch_config=fetch_config,
                llm_config=llm_config,
                schema=schema,
                formats=formats,
                webhook_url=webhook_url,
            ),
        )

    def list(self) -> Dict[str, Any]:
        """List all monitors."""
        logger.info("Listing monitors")
        return self._client._make_request("GET", f"{self._client.base_url}/monitor")

    def get(self, monitor_id: str) -> Dict[str, Any]:
        """Get a specific monitor.

        Args:
            monitor_id: The monitor ID
        """
        logger.info(f"Fetching monitor {monitor_id}")
        return self._client._make_request(
            "GET", f"{self._client.base_url}/monitor/{monitor_id}"
        )

    def pause(self, monitor_id: str) -> Dict[str, Any]:
        """Pause a monitor.

        Args:
            monitor_id: The monitor ID to pause
        """
        logger.info(f"Pausing monitor {monitor_id}")
        return self._client._make_request(
            "POST", f"{self._client.base_url}/monitor/{monitor_id}/pause"
        )

    def resume(self, monitor_id: str) -> Dict[str, Any]:
        """Resume a paused monitor.

        Args:
            monitor_id: The monitor ID to resume
        """
        logger.info(f"Resuming monitor {monitor_id}")
        return self._client._make_request(
            "POST", f"{self._client.base_url}/monitor/{monitor_id}/resume"
        )

    def delete(self, monitor_id: str) -> Dict[str, Any]:
        """Delete a monitor.

        Args:
            monitor_id: The monitor ID to delete
        """
        logger.info(f"Deleting monitor {monitor_id}")
        return self._client._make_request(
            "DELETE", f"{self._client.base_url}/monitor/{monitor_id}"
        )


class Client:
    """Synchronous client for the ScrapeGraphAI v2 API.

    Example:
        >>> client = Client(api_key="sgai-...")
        >>> result = client.scrape("https://example.com")
        >>> result = client.extract("https://example.com", prompt="Extract prices")
        >>> job = client.crawl.start("https://example.com", depth=3)
    """

    @classmethod
    def from_env(
        cls,
        verify_ssl: bool = True,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> "Client":
        """Initialize Client using SGAI_API_KEY environment variable."""
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
        """Initialize Client.

        Args:
            api_key: API key for authentication. If None, reads from SGAI_API_KEY env var
            base_url: Override the default API base URL
            verify_ssl: Whether to verify SSL certificates
            timeout: Request timeout in seconds (None = no timeout)
            max_retries: Maximum retry attempts on server errors
            retry_delay: Base delay between retries in seconds
        """
        logger.info("Initializing Client")

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
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        # HTTP session with connection pooling and retry
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.verify = verify_ssl

        adapter = requests.adapters.HTTPAdapter(
            max_retries=urllib3.Retry(
                total=max_retries,
                backoff_factor=retry_delay,
                status_forcelist=[500, 502, 503, 504],
            )
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Namespaced sub-clients
        self.crawl = _CrawlNamespace(self)
        self.monitor = _MonitorNamespace(self)

        logger.info("Client initialized successfully")

    def _make_request(self, method: str, url: str, **kwargs: Any) -> Any:
        """Make HTTP request with error handling."""
        try:
            logger.debug(f"Making {method} request to {url}")
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            return handle_sync_response(response)
        except RequestException as e:
            logger.error(f"Request failed: {e}")
            if hasattr(e, "response") and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get("error", str(e))
                    raise APIError(error_msg, status_code=e.response.status_code)
                except ValueError:
                    raise APIError(
                        str(e),
                        status_code=getattr(e.response, "status_code", None),
                    )
            raise ConnectionError(f"Failed to connect to API: {e}")

    # ------------------------------------------------------------------
    # Scrape
    # ------------------------------------------------------------------

    def scrape(
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
        return self._make_request(
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

    def extract(
        self,
        url: Optional[str],
        prompt: str,
        output_schema: Optional[Any] = None,
        fetch_config: Optional[FetchConfig] = None,
        llm_config: Optional[LlmConfig] = None,
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
            output_schema: Legacy alias for schema
            fetch_config: Fetch configuration options
            llm_config: Deprecated and ignored by the SGAI v2 extract route
        """
        logger.info(f"Extracting from {url}")
        return self._make_request(
            "POST",
            f"{self.base_url}/extract",
            json=build_extract_payload(
                url=url,
                prompt=prompt,
                output_schema=output_schema,
                fetch_config=fetch_config,
                llm_config=llm_config,
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

    def search(
        self,
        query: str,
        num_results: int = 5,
        output_schema: Optional[Any] = None,
        location_geo_code: Optional[str] = None,
        llm_config: Optional[LlmConfig] = None,
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
            num_results: Number of results (1-20, default 5)
            output_schema: Legacy alias for schema
            location_geo_code: Geo code for geo-targeted results
            llm_config: Deprecated and ignored by the SGAI v2 search route
        """
        logger.info(f"Searching: {query}")
        return self._make_request(
            "POST",
            f"{self.base_url}/search",
            json=build_search_payload(
                query=query,
                num_results=num_results,
                output_schema=output_schema,
                location_geo_code=location_geo_code,
                llm_config=llm_config,
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

    def credits(self) -> Dict[str, Any]:
        """Get remaining API credits."""
        logger.info("Fetching credits")
        return self._make_request("GET", f"{self.base_url}/credits")

    # ------------------------------------------------------------------
    # History
    # ------------------------------------------------------------------

    def history(
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
        return self._make_request(
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

    def schema(
        self,
        prompt: str,
        existing_schema: Optional[Any] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate or refine a JSON schema from a prompt."""
        logger.info("Generating schema")
        return self._make_request(
            "POST",
            f"{self.base_url}/schema",
            json=build_schema_payload(
                prompt, existing_schema=existing_schema, model=model
            ),
        )

    def validate(self, email: str) -> Dict[str, Any]:
        """Validate an email address against SGAI's allowlist endpoint."""
        logger.info("Validating email")
        return self._make_request(
            "GET", f"{self.base_url}/validate", params=build_validate_params(email)
        )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the HTTP session."""
        logger.info("Closing Client session")
        self.session.close()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
