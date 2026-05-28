from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from typing import Literal

import httpx
from pydantic import BaseModel, TypeAdapter

from .env import env
from .schemas import (
    ApiResult,
    CrawlPagesQuery,
    CrawlPagesResponse,
    CrawlRequest,
    CrawlResponse,
    CreditsResponse,
    ExtractRequest,
    ExtractResponse,
    FetchConfig,
    FetchContentType,
    FormatConfig,
    HealthResponse,
    HistoryEntry,
    HistoryFilter,
    HistoryPage,
    HtmlMode,
    MonitorActivityRequest,
    MonitorActivityResponse,
    MonitorCreateRequest,
    MonitorResponse,
    MonitorUpdateRequest,
    ScrapeRequest,
    ScrapeResponse,
    SearchRequest,
    SearchResponse,
    Service,
    TimeRange,
)

_SERVER_TIMING_RE = re.compile(r"dur=(\d+(?:\.\d+)?)")


def _debug(label: str, data: object = None) -> None:
    if not env.debug:
        return
    ts = datetime.now().isoformat()
    if data is not None:
        print(f"[{ts}] {label}", json.dumps(data, indent=2, default=str), file=sys.stderr)
    else:
        print(f"[{ts}] {label}", file=sys.stderr)


def _map_http_error(status: int) -> str:
    match status:
        case 401:
            return "Invalid or missing API key"
        case 402:
            return "Insufficient credits - purchase more at https://dashboard.scrapegraphai.com"
        case 422:
            return "Invalid parameters - check your request"
        case 429:
            return "Rate limited - slow down and retry"
        case 500:
            return "Server error - try again later"
        case _:
            return f"HTTP {status}"


def _serialize(model: BaseModel) -> dict:
    return model.model_dump(mode="json", exclude_none=True, by_alias=True)


# Strips None kwargs so Pydantic fields with non-None defaults (formats, max_depth, etc.)
# fall back to their defaults instead of raising a ValidationError on None.
def _compact(**kwargs) -> dict:
    return {k: v for k, v in kwargs.items() if v is not None}


class CrawlResource:
    def __init__(self, client: ScrapeGraphAI):
        self._client = client

    def start(
        self,
        url: str,
        *,
        formats: list[FormatConfig] | None = None,
        max_depth: int | None = None,
        max_pages: int | None = None,
        max_links_per_page: int | None = None,
        allow_external: bool | None = None,
        include_patterns: list[str] | None = None,
        exclude_patterns: list[str] | None = None,
        content_types: list[FetchContentType] | None = None,
        fetch_config: FetchConfig | None = None,
    ) -> ApiResult[CrawlResponse]:
        req = CrawlRequest(
            **_compact(
                url=url,
                formats=formats,
                max_depth=max_depth,
                max_pages=max_pages,
                max_links_per_page=max_links_per_page,
                allow_external=allow_external,
                include_patterns=include_patterns,
                exclude_patterns=exclude_patterns,
                content_types=content_types,
                fetch_config=fetch_config,
            )
        )
        return self._client._post("/crawl", req, CrawlResponse)

    def get(self, id: str) -> ApiResult[CrawlResponse]:
        return self._client._get(f"/crawl/{id}", CrawlResponse)

    def pages(
        self,
        id: str,
        *,
        cursor: int | None = None,
        limit: int | None = None,
    ) -> ApiResult[CrawlPagesResponse]:
        kwargs = _compact(cursor=cursor, limit=limit)
        query = CrawlPagesQuery(**kwargs) if kwargs else None
        qs = {key: getattr(query, key) for key in kwargs} if query else None
        return self._client._get(f"/crawl/{id}/pages", CrawlPagesResponse, params=qs or None)

    def stop(self, id: str) -> ApiResult[dict]:
        return self._client._post_empty(f"/crawl/{id}/stop")

    def resume(self, id: str) -> ApiResult[dict]:
        return self._client._post_empty(f"/crawl/{id}/resume")

    def delete(self, id: str) -> ApiResult[dict]:
        return self._client._delete(f"/crawl/{id}")


class MonitorResource:
    def __init__(self, client: ScrapeGraphAI):
        self._client = client

    def create(
        self,
        url: str,
        interval: str,
        *,
        name: str | None = None,
        formats: list[FormatConfig] | None = None,
        webhook_url: str | None = None,
        fetch_config: FetchConfig | None = None,
    ) -> ApiResult[MonitorResponse]:
        req = MonitorCreateRequest(
            **_compact(
                url=url,
                interval=interval,
                name=name,
                formats=formats,
                webhook_url=webhook_url,
                fetch_config=fetch_config,
            )
        )
        return self._client._post("/monitor", req, MonitorResponse)

    def list(self) -> ApiResult[list[MonitorResponse]]:
        return self._client._get("/monitor", list[MonitorResponse])

    def get(self, id: str) -> ApiResult[MonitorResponse]:
        return self._client._get(f"/monitor/{id}", MonitorResponse)

    def update(
        self,
        id: str,
        *,
        name: str | None = None,
        formats: list[FormatConfig] | None = None,
        webhook_url: str | None = None,
        interval: str | None = None,
        fetch_config: FetchConfig | None = None,
    ) -> ApiResult[MonitorResponse]:
        req = MonitorUpdateRequest(
            **_compact(
                name=name,
                formats=formats,
                webhook_url=webhook_url,
                interval=interval,
                fetch_config=fetch_config,
            )
        )
        return self._client._patch(f"/monitor/{id}", req, MonitorResponse)

    def delete(self, id: str) -> ApiResult[dict]:
        return self._client._delete(f"/monitor/{id}")

    def pause(self, id: str) -> ApiResult[MonitorResponse]:
        return self._client._post_empty(f"/monitor/{id}/pause", MonitorResponse)

    def resume(self, id: str) -> ApiResult[MonitorResponse]:
        return self._client._post_empty(f"/monitor/{id}/resume", MonitorResponse)

    def activity(
        self,
        id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> ApiResult[MonitorActivityResponse]:
        kwargs = _compact(limit=limit, cursor=cursor)
        qs = (
            MonitorActivityRequest(**kwargs).model_dump(
                by_alias=True, exclude_none=True, exclude_defaults=True
            )
            if kwargs
            else None
        )
        return self._client._get(
            f"/monitor/{id}/activity", MonitorActivityResponse, params=qs or None
        )


class HistoryResource:
    def __init__(self, client: ScrapeGraphAI):
        self._client = client

    def list(
        self,
        *,
        page: int | None = None,
        limit: int | None = None,
        service: Service | None = None,
    ) -> ApiResult[HistoryPage]:
        kwargs = _compact(page=page, limit=limit, service=service)
        if not kwargs:
            return self._client._get("/history", HistoryPage)
        params = HistoryFilter(**kwargs)
        qs: dict[str, str] = {}
        if page is not None:
            qs["page"] = str(params.page)
        if limit is not None:
            qs["limit"] = str(params.limit)
        if service is not None:
            qs["service"] = params.service
        return self._client._get("/history", HistoryPage, params=qs or None)

    def get(self, id: str) -> ApiResult[HistoryEntry]:
        return self._client._get(f"/history/{id}", HistoryEntry)


class ScrapeGraphAI:
    def __init__(self, *, api_key: str | None = None):
        self._api_key = api_key or os.environ.get("SGAI_API_KEY")
        if not self._api_key:
            raise ValueError("API key required: pass api_key or set SGAI_API_KEY env var")

        self._http = httpx.Client(
            base_url=env.base_url,
            timeout=env.timeout,
            headers={"SGAI-APIKEY": self._api_key},
        )

        self.crawl = CrawlResource(self)
        self.monitor = MonitorResource(self)
        self.history = HistoryResource(self)

    def _request[T](
        self,
        method: str,
        path: str,
        response_type: type[T],
        body: BaseModel | None = None,
        params: dict | None = None,
        base_url: str | None = None,
    ) -> ApiResult[T]:
        url = path if base_url is None else f"{base_url}{path}"
        json_body = _serialize(body) if body else None
        _debug(f"-> {method} {url}", json_body)

        try:
            start = time.perf_counter()

            if base_url:
                resp = httpx.request(
                    method,
                    url,
                    json=json_body,
                    params=params,
                    headers={"SGAI-APIKEY": self._api_key},
                    timeout=env.timeout,
                )
            else:
                resp = self._http.request(method, path, json=json_body, params=params)

            server_timing = resp.headers.get("Server-Timing")
            if server_timing and (match := _SERVER_TIMING_RE.search(server_timing)):
                elapsed_ms = int(float(match.group(1)))
            else:
                elapsed_ms = int((time.perf_counter() - start) * 1000)

            if not resp.is_success:
                error = _map_http_error(resp.status_code)
                try:
                    err_body = resp.json()
                    _debug(f"<- {resp.status_code}", err_body)
                    if "detail" in err_body:
                        d = err_body["detail"]
                        detail = d if isinstance(d, str) else str(d)
                        error = f"{error}: {detail}"
                except Exception as e:
                    _debug(f"Failed to parse error response: {e}")
                return ApiResult(status="error", data=None, error=error, elapsed_ms=elapsed_ms)

            raw = resp.json()
            _debug(f"<- {resp.status_code} ({elapsed_ms}ms)", raw)
            parsed = TypeAdapter(response_type).validate_python(raw)
            return ApiResult(status="success", data=parsed, elapsed_ms=elapsed_ms)

        except httpx.TimeoutException:
            return ApiResult(status="error", data=None, error="Request timed out", elapsed_ms=0)
        except Exception as e:
            return ApiResult(status="error", data=None, error=str(e), elapsed_ms=0)

    def _get[T](
        self, path: str, response_type: type[T], params: dict | None = None
    ) -> ApiResult[T]:
        return self._request("GET", path, response_type, params=params)

    def _post[T](self, path: str, body: BaseModel, response_type: type[T]) -> ApiResult[T]:
        return self._request("POST", path, response_type, body=body)

    def _post_empty[T](self, path: str, response_type: type[T] = dict) -> ApiResult[T]:
        return self._request("POST", path, response_type)

    def _patch[T](self, path: str, body: BaseModel, response_type: type[T]) -> ApiResult[T]:
        return self._request("PATCH", path, response_type, body=body)

    def _delete(self, path: str) -> ApiResult[dict]:
        return self._request("DELETE", path, dict)

    def scrape(
        self,
        url: str,
        *,
        formats: list[FormatConfig] | None = None,
        fetch_config: FetchConfig | None = None,
        content_type: FetchContentType | None = None,
    ) -> ApiResult[ScrapeResponse]:
        req = ScrapeRequest(
            **_compact(
                url=url,
                formats=formats,
                fetch_config=fetch_config,
                content_type=content_type,
            )
        )
        return self._post("/scrape", req, ScrapeResponse)

    def extract(
        self,
        prompt: str,
        *,
        url: str | None = None,
        html: str | None = None,
        markdown: str | None = None,
        schema: dict[str, object] | None = None,
        mode: HtmlMode | None = None,
        fetch_config: FetchConfig | None = None,
        content_type: FetchContentType | None = None,
    ) -> ApiResult[ExtractResponse]:
        req = ExtractRequest(
            **_compact(
                prompt=prompt,
                url=url,
                html=html,
                markdown=markdown,
                schema=schema,
                mode=mode,
                fetch_config=fetch_config,
                content_type=content_type,
            )
        )
        return self._post("/extract", req, ExtractResponse)

    def search(
        self,
        query: str,
        *,
        num_results: int | None = None,
        format: Literal["html", "markdown"] | None = None,
        mode: HtmlMode | None = None,
        prompt: str | None = None,
        schema: dict[str, object] | None = None,
        fetch_config: FetchConfig | None = None,
        location_geo_code: str | None = None,
        time_range: TimeRange | None = None,
    ) -> ApiResult[SearchResponse]:
        req = SearchRequest(
            **_compact(
                query=query,
                num_results=num_results,
                format=format,
                mode=mode,
                prompt=prompt,
                schema=schema,
                fetch_config=fetch_config,
                location_geo_code=location_geo_code,
                time_range=time_range,
            )
        )
        return self._post("/search", req, SearchResponse)

    def credits(self) -> ApiResult[CreditsResponse]:
        return self._get("/credits", CreditsResponse)

    def health(self) -> ApiResult[HealthResponse]:
        return self._get("/health", HealthResponse)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> ScrapeGraphAI:
        return self

    def __exit__(self, *args) -> None:
        self.close()
