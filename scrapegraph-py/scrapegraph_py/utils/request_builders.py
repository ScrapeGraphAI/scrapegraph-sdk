"""Canonical builders for SDK request payloads and query params."""

from typing import Any, Dict, List, Optional

from scrapegraph_py.models.crawl import CrawlRequest
from scrapegraph_py.models.extract import ExtractRequest
from scrapegraph_py.models.history import HistoryFilter
from scrapegraph_py.models.monitor import MonitorCreateRequest
from scrapegraph_py.models.scrape import ScrapeRequest
from scrapegraph_py.models.search import SearchRequest
from scrapegraph_py.models.shared import FetchConfig
from scrapegraph_py.utils.payloads import (
    build_json_format_entry,
    normalize_format_entries,
    normalize_history_params,
    schema_to_dict,
)


def build_crawl_payload(
    url: str,
    *,
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
    """Build the SGAI v2 crawl payload from SDK inputs."""
    resolved_max_depth = max_depth if max_depth is not None else depth
    request = CrawlRequest(
        url=url,
        formats=normalize_format_entries(formats, legacy_format=format),
        max_depth=resolved_max_depth if resolved_max_depth is not None else 2,
        max_pages=max_pages,
        max_links_per_page=max_links_per_page,
        allow_external=allow_external,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        content_types=content_types,
        fetch_config=fetch_config,
    )
    return request.model_dump()


def build_monitor_payload(
    *,
    name: Optional[str],
    url: str,
    prompt: Optional[str],
    interval: str,
    fetch_config: Optional[FetchConfig] = None,
    schema: Optional[Any] = None,
    formats: Optional[List[Dict[str, Any]]] = None,
    webhook_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the SGAI v2 monitor payload from SDK inputs."""
    if formats is not None:
        normalized_formats = normalize_format_entries(formats)
    else:
        if prompt is None:
            raise ValueError("prompt is required when formats are not provided")
        normalized_formats = [
            build_json_format_entry(
                prompt=prompt,
                schema=schema,
            )
        ]

    request = MonitorCreateRequest(
        name=name,
        url=url,
        formats=normalized_formats,
        interval=interval,
        webhook_url=webhook_url,
        fetch_config=fetch_config,
    )
    return request.model_dump()


def build_scrape_payload(
    url: str,
    *,
    format: str = "markdown",
    fetch_config: Optional[FetchConfig] = None,
    formats: Optional[List[Dict[str, Any]]] = None,
    content_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the SGAI v2 scrape payload from SDK inputs."""
    request = ScrapeRequest(
        url=url,
        formats=normalize_format_entries(formats, legacy_format=format),
        content_type=content_type,
        fetch_config=fetch_config,
    )
    return request.model_dump()


def build_extract_payload(
    *,
    url: Optional[str],
    prompt: str,
    fetch_config: Optional[FetchConfig] = None,
    schema: Optional[Any] = None,
    mode: str = "normal",
    content_type: Optional[str] = None,
    html: Optional[str] = None,
    markdown: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the SGAI v2 extract payload from SDK inputs."""
    request = ExtractRequest(
        url=url,
        html=html,
        markdown=markdown,
        prompt=prompt,
        schema_=schema_to_dict(schema),
        fetch_config=fetch_config,
        mode=mode,
        content_type=content_type,
    )
    return request.model_dump()


def build_search_payload(
    *,
    query: str,
    num_results: int = 3,
    country: Optional[str] = None,
    schema: Optional[Any] = None,
    prompt: Optional[str] = None,
    format: str = "markdown",
    mode: str = "prune",
    fetch_config: Optional[FetchConfig] = None,
    time_range: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the SGAI v2 search payload from SDK inputs."""
    request = SearchRequest(
        query=query,
        num_results=num_results,
        schema_=schema_to_dict(schema),
        prompt=prompt,
        format=format,
        mode=mode,
        fetch_config=fetch_config,
        country=country,
        time_range=time_range,
    )
    return request.model_dump()


def build_history_params(
    *,
    endpoint: Optional[str] = None,
    status: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    page: Optional[int] = None,
    service: Optional[str] = None,
) -> Dict[str, Any]:
    """Build SGAI v2 history query params from SDK inputs."""
    filter_obj = HistoryFilter(
        **normalize_history_params(
            page=page,
            limit=limit,
            service=service,
            endpoint=endpoint,
            status=status,
            offset=offset,
        )
    )
    return filter_obj.to_params()


def build_schema_payload(
    prompt: str,
    *,
    existing_schema: Optional[Any] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """Build the SGAI v2 schema payload from SDK inputs."""
    payload: Dict[str, Any] = {"prompt": prompt}
    schema_dict = schema_to_dict(existing_schema)
    if schema_dict is not None:
        payload["existingSchema"] = schema_dict
    if model is not None:
        payload["model"] = model
    return payload


def build_validate_params(email: str) -> Dict[str, str]:
    """Build the SGAI v2 validate query params from SDK inputs."""
    return {"email": email}
