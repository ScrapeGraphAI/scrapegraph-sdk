from __future__ import annotations

from typing import Annotated, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator
from pydantic.alias_generators import to_camel

T = TypeVar("T")


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ResponseModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, extra="allow")


ApiService = Literal["scrape", "extract", "search", "monitor", "crawl"]
ApiStatus = Literal["completed", "failed"]
ApiHtmlMode = Literal["normal", "reader", "prune"]
ApiFetchMode = Literal["auto", "fast", "js"]
ApiScrapeFormat = Literal[
    "markdown", "html", "links", "images", "summary", "json", "branding", "screenshot"
]
ApiTimeRange = Literal["past_hour", "past_24_hours", "past_week", "past_month", "past_year"]
ApiCrawlStatus = Literal["running", "completed", "failed", "paused", "deleted"]
ApiCrawlPageStatus = Literal["completed", "failed", "skipped"]
ApiHistoryService = Literal["scrape", "extract", "search", "monitor", "crawl"]
ApiHistoryStatus = Literal["completed", "failed", "running", "paused", "deleted"]

ApiFetchContentType = Literal[
    "text/html",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/avif",
    "image/tiff",
    "image/heic",
    "image/bmp",
    "application/epub+zip",
    "application/rtf",
    "application/vnd.oasis.opendocument.text",
    "text/csv",
    "text/plain",
    "application/x-latex",
]


class ApiResult(BaseModel, Generic[T]):
    status: Literal["success", "error"]
    data: T | None
    error: str | None = None
    elapsed_ms: int


class MockConfig(CamelModel):
    min_kb: int = Field(default=1, ge=1, le=1000)
    max_kb: int = Field(default=5, ge=1, le=1000)
    min_sleep: int = Field(default=5, ge=0, le=30000)
    max_sleep: int = Field(default=15, ge=0, le=30000)
    write_to_bucket: bool = False


class FetchConfig(CamelModel):
    mode: ApiFetchMode = "auto"
    stealth: bool = False
    timeout: int = Field(default=30000, ge=1000, le=60000)
    wait: int = Field(default=0, ge=0, le=30000)
    headers: dict[str, str] | None = None
    cookies: dict[str, str] | None = None
    country: Annotated[str, Field(min_length=2, max_length=2)] | None = None
    scrolls: int = Field(default=0, ge=0, le=100)
    mock: bool | MockConfig = False


class MarkdownFormatConfig(CamelModel):
    type: Literal["markdown"] = "markdown"
    mode: ApiHtmlMode = "normal"


class HtmlFormatConfig(CamelModel):
    type: Literal["html"] = "html"
    mode: ApiHtmlMode = "normal"


class ScreenshotFormatConfig(CamelModel):
    type: Literal["screenshot"] = "screenshot"
    full_page: bool = False
    width: int = Field(default=1440, ge=320, le=3840)
    height: int = Field(default=900, ge=200, le=2160)
    quality: int = Field(default=80, ge=1, le=100)


class JsonFormatConfig(CamelModel):
    type: Literal["json"] = "json"
    prompt: Annotated[str, Field(min_length=1, max_length=10000)]
    schema_: dict[str, object] | None = Field(default=None, alias="schema")
    mode: ApiHtmlMode = "normal"


class LinksFormatConfig(CamelModel):
    type: Literal["links"] = "links"


class ImagesFormatConfig(CamelModel):
    type: Literal["images"] = "images"


class SummaryFormatConfig(CamelModel):
    type: Literal["summary"] = "summary"


class BrandingFormatConfig(CamelModel):
    type: Literal["branding"] = "branding"


ScrapeFormatEntry = (
    MarkdownFormatConfig
    | HtmlFormatConfig
    | ScreenshotFormatConfig
    | JsonFormatConfig
    | LinksFormatConfig
    | ImagesFormatConfig
    | SummaryFormatConfig
    | BrandingFormatConfig
)


class ScrapeRequest(CamelModel):
    url: HttpUrl
    content_type: ApiFetchContentType | None = None
    fetch_config: FetchConfig | None = None
    formats: list[ScrapeFormatEntry] = Field(default_factory=lambda: [MarkdownFormatConfig()])

    @model_validator(mode="after")
    def validate_unique_formats(self):
        types = [f.type for f in self.formats]
        if len(types) != len(set(types)):
            raise ValueError("duplicate format types not allowed")
        return self


class ExtractRequest(CamelModel):
    url: HttpUrl | None = None
    html: str | None = None
    markdown: str | None = None
    mode: ApiHtmlMode = "normal"
    prompt: Annotated[str, Field(min_length=1, max_length=10000)]
    schema_: dict[str, object] | None = Field(default=None, alias="schema")
    content_type: ApiFetchContentType | None = None
    fetch_config: FetchConfig | None = None

    @model_validator(mode="after")
    def validate_source(self):
        if not self.url and not self.html and not self.markdown:
            raise ValueError("Either url, html, or markdown is required")
        return self


class SearchRequest(CamelModel):
    query: Annotated[str, Field(min_length=1, max_length=500)]
    num_results: int = Field(default=3, ge=1, le=20)
    format: Literal["html", "markdown"] = "markdown"
    mode: ApiHtmlMode = "prune"
    fetch_config: FetchConfig | None = None
    prompt: Annotated[str, Field(min_length=1, max_length=10000)] | None = None
    schema_: dict[str, object] | None = Field(default=None, alias="schema")
    location_geo_code: Annotated[str, Field(max_length=10)] | None = None
    time_range: ApiTimeRange | None = None

    @model_validator(mode="after")
    def validate_schema_requires_prompt(self):
        if self.schema_ and not self.prompt:
            raise ValueError("schema requires prompt")
        return self


class MonitorCreateRequest(CamelModel):
    url: HttpUrl
    name: Annotated[str, Field(max_length=200)] | None = None
    formats: list[ScrapeFormatEntry] = Field(default_factory=lambda: [MarkdownFormatConfig()])
    webhook_url: HttpUrl | None = None
    interval: Annotated[str, Field(min_length=1, max_length=100)]
    fetch_config: FetchConfig | None = None

    @model_validator(mode="after")
    def validate_unique_formats(self):
        types = [f.type for f in self.formats]
        if len(types) != len(set(types)):
            raise ValueError("duplicate format types not allowed")
        return self


class MonitorUpdateRequest(CamelModel):
    name: Annotated[str, Field(max_length=200)] | None = None
    formats: list[ScrapeFormatEntry] | None = None
    webhook_url: HttpUrl | None = None
    interval: Annotated[str, Field(min_length=1, max_length=100)] | None = None
    fetch_config: FetchConfig | None = None

    @model_validator(mode="after")
    def validate_unique_formats(self):
        if self.formats:
            types = [f.type for f in self.formats]
            if len(types) != len(set(types)):
                raise ValueError("duplicate format types not allowed")
        return self


class CrawlRequest(CamelModel):
    url: HttpUrl
    formats: list[ScrapeFormatEntry] = Field(default_factory=lambda: [MarkdownFormatConfig()])
    max_depth: int = Field(default=2, ge=0)
    max_pages: int = Field(default=50, ge=1, le=1000)
    max_links_per_page: int = Field(default=10, ge=1)
    allow_external: bool = False
    include_patterns: list[str] | None = None
    exclude_patterns: list[str] | None = None
    content_types: list[ApiFetchContentType] | None = None
    fetch_config: FetchConfig | None = None

    @model_validator(mode="after")
    def validate_unique_formats(self):
        types = [f.type for f in self.formats]
        if len(types) != len(set(types)):
            raise ValueError("duplicate format types not allowed")
        return self


class HistoryFilter(CamelModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    service: ApiService | None = None


class TokenUsage(ResponseModel):
    prompt_tokens: int
    completion_tokens: int

    model_config = ConfigDict(extra="allow")


class ChunkerMetadata(ResponseModel):
    chunks: list[dict]

    model_config = ConfigDict(extra="allow")


class FetchWarning(ResponseModel):
    reason: Literal["too_short", "empty", "bot_blocked", "spa_shell", "soft_404"]
    provider: str | None = None

    model_config = ConfigDict(extra="allow")


class ScrapeMetadata(ResponseModel):
    provider: str | None = None
    content_type: str
    elapsed_ms: int | None = None
    warnings: list[FetchWarning] | None = None
    ocr: dict | None = None

    model_config = ConfigDict(extra="allow")


class ScrapeResponse(ResponseModel):
    results: dict
    metadata: ScrapeMetadata
    errors: dict | None = None

    model_config = ConfigDict(extra="allow")


class ExtractResponse(ResponseModel):
    raw: str | None
    json_data: dict | None = Field(default=None, alias="json")
    usage: TokenUsage
    metadata: dict

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class SearchResult(ResponseModel):
    url: str
    title: str
    content: str
    provider: str | None = None

    model_config = ConfigDict(extra="allow")


class SearchMetadata(ResponseModel):
    search: dict
    pages: dict
    chunker: ChunkerMetadata | None = None

    model_config = ConfigDict(extra="allow")


class SearchResponse(ResponseModel):
    results: list[SearchResult]
    json_data: dict | None = Field(default=None, alias="json")
    raw: str | None = None
    usage: TokenUsage | None = None
    metadata: SearchMetadata

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class CrawlPage(ResponseModel):
    url: str
    status: ApiCrawlPageStatus
    depth: int
    parent_url: str | None
    links: list[str]
    scrape_ref_id: str
    title: str
    content_type: str
    screenshot_url: str | None = None
    reason: str | None = None
    error: str | None = None

    model_config = ConfigDict(extra="allow")


class CrawlResponse(ResponseModel):
    id: str
    status: ApiCrawlStatus
    reason: str | None = None
    total: int
    finished: int
    pages: list[CrawlPage]

    model_config = ConfigDict(extra="allow")


class TextChange(ResponseModel):
    type: Literal["added", "removed"]
    line: int
    content: str


class JsonChange(ResponseModel):
    path: str
    old: object
    new: object


class SetChange(ResponseModel):
    added: list[str]
    removed: list[str]


class ImageChange(ResponseModel):
    size: int
    changed: int
    mask: str | None = None


class MonitorDiffs(ResponseModel):
    markdown: list[TextChange] | None = None
    html: list[TextChange] | None = None
    json_changes: list[JsonChange] | None = Field(default=None, alias="json")
    screenshot: ImageChange | None = None
    links: SetChange | None = None
    images: SetChange | None = None
    summary: list[TextChange] | None = None
    branding: list[JsonChange] | None = None

    model_config = ConfigDict(extra="allow", populate_by_name=True)


class WebhookStatus(ResponseModel):
    sent_at: str
    status_code: int | None
    error: str | None = None


class MonitorResult(ResponseModel):
    changed: bool
    diffs: MonitorDiffs
    refs: dict
    webhook_status: WebhookStatus | None = None

    model_config = ConfigDict(extra="allow")


class MonitorResponse(ResponseModel):
    cron_id: str
    schedule_id: str
    interval: str
    status: Literal["active", "paused"]
    config: dict
    created_at: str
    updated_at: str

    model_config = ConfigDict(extra="allow")


ApiMonitorTickStatus = Literal["completed", "failed", "paused", "running"]


class MonitorTickEntry(ResponseModel):
    id: str
    status: ApiMonitorTickStatus
    created_at: str
    elapsed_ms: int
    changed: bool
    diffs: MonitorDiffs
    error: str | None = None

    model_config = ConfigDict(extra="allow")


class MonitorActivityResponse(ResponseModel):
    ticks: list[MonitorTickEntry]
    next_cursor: str | None

    model_config = ConfigDict(extra="allow")


class MonitorActivityRequest(CamelModel):
    limit: int = Field(default=20, ge=1, le=100)
    cursor: str | None = None


class HistoryEntry(ResponseModel):
    id: str
    service: ApiHistoryService
    status: ApiHistoryStatus
    error: object | None
    elapsed_ms: int
    created_at: str
    request_parent_id: str | None
    params: dict
    result: dict

    model_config = ConfigDict(extra="allow")


class HistoryPagination(ResponseModel):
    page: int
    limit: int
    total: int


class HistoryPage(ResponseModel):
    data: list[HistoryEntry]
    pagination: HistoryPagination

    model_config = ConfigDict(extra="allow")


class JobsStatus(ResponseModel):
    used: int
    limit: int


class CreditsJobs(ResponseModel):
    crawl: JobsStatus
    monitor: JobsStatus


class CreditsResponse(ResponseModel):
    remaining: int
    used: int
    plan: str
    jobs: CreditsJobs

    model_config = ConfigDict(extra="allow")


class HealthServices(ResponseModel):
    redis: Literal["ok", "down"]
    db: Literal["ok", "down"]


class HealthResponse(ResponseModel):
    status: str
    uptime: int
    services: HealthServices | None = None

    model_config = ConfigDict(extra="allow")
