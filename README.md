# ScrapeGraphAI Python SDK

[![PyPI version](https://badge.fury.io/py/scrapegraph-py.svg)](https://badge.fury.io/py/scrapegraph-py)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <a href="https://scrapegraphai.com">
    <img src="media/banner.png" alt="ScrapeGraphAI Python SDK" style="width: 100%;">
  </a>
</p>

Official Python SDK for the [ScrapeGraphAI API](https://scrapegraphai.com).

## Install

```bash
pip install scrapegraph-py
# or
uv add scrapegraph-py
```

## Quick Start

```python
from scrapegraph_py import ScrapeGraphAI, ScrapeRequest

# reads SGAI_API_KEY from env, or pass explicitly: ScrapeGraphAI(api_key="...")
sgai = ScrapeGraphAI()

result = sgai.scrape(ScrapeRequest(
    url="https://example.com",
))

if result.status == "success":
    print(result.data["results"]["markdown"]["data"])
else:
    print(result.error)
```

Every method returns `ApiResult[T]` — no exceptions to catch:

```python
@dataclass
class ApiResult(Generic[T]):
    status: Literal["success", "error"]
    data: T | None
    error: str | None
    elapsed_ms: int
```

## API

### scrape

Scrape a webpage in multiple formats (markdown, html, screenshot, json, etc).

```python
from scrapegraph_py import (
    ScrapeGraphAI, ScrapeRequest, FetchConfig,
    MarkdownFormatConfig, ScreenshotFormatConfig, JsonFormatConfig
)

sgai = ScrapeGraphAI()

res = sgai.scrape(ScrapeRequest(
    url="https://example.com",
    formats=[
        MarkdownFormatConfig(mode="reader"),
        ScreenshotFormatConfig(full_page=True, width=1440, height=900),
        JsonFormatConfig(prompt="Extract product info"),
    ],
    content_type="text/html",           # optional, auto-detected
    fetch_config=FetchConfig(           # optional
        mode="js",                      # "auto" | "fast" | "js"
        stealth=True,
        timeout=30000,
        wait=2000,
        scrolls=3,
        headers={"Accept-Language": "en"},
        cookies={"session": "abc"},
        country="us",
    ),
))
```

**Formats:**
- `markdown` — Clean markdown (modes: `normal`, `reader`, `prune`)
- `html` — Raw HTML (modes: `normal`, `reader`, `prune`)
- `links` — All links on the page
- `images` — All image URLs
- `summary` — AI-generated summary
- `json` — Structured extraction with prompt/schema
- `branding` — Brand colors, typography, logos
- `screenshot` — Page screenshot (full_page, width, height, quality)

### extract

Extract structured data from a URL, HTML, or markdown using AI.

```python
from scrapegraph_py import ScrapeGraphAI, ExtractRequest

sgai = ScrapeGraphAI()

res = sgai.extract(ExtractRequest(
    url="https://example.com",
    prompt="Extract product names and prices",
    schema={"type": "object", "properties": {...}},  # optional
    mode="reader",                                    # optional
    fetch_config=FetchConfig(...),                   # optional
))
# Or pass html/markdown directly instead of url
```

### search

Search the web and optionally extract structured data.

```python
from scrapegraph_py import ScrapeGraphAI, SearchRequest

sgai = ScrapeGraphAI()

res = sgai.search(SearchRequest(
    query="best programming languages 2024",
    num_results=5,                      # 1-20, default 3
    format="markdown",                  # "markdown" | "html"
    prompt="Extract key points",        # optional, for AI extraction
    schema={...},                       # optional
    time_range="past_week",             # optional
    location_geo_code="us",             # optional
    fetch_config=FetchConfig(...),      # optional
))
```

### crawl

Crawl a website and its linked pages.

```python
from scrapegraph_py import ScrapeGraphAI, CrawlRequest, MarkdownFormatConfig

sgai = ScrapeGraphAI()

# Start a crawl
start = sgai.crawl.start(CrawlRequest(
    url="https://example.com",
    formats=[MarkdownFormatConfig()],
    max_pages=50,
    max_depth=2,
    max_links_per_page=10,
    include_patterns=["/blog/*"],
    exclude_patterns=["/admin/*"],
    fetch_config=FetchConfig(...),
))

# Check status
status = sgai.crawl.get(start.data["id"])

# Control
sgai.crawl.stop(crawl_id)
sgai.crawl.resume(crawl_id)
sgai.crawl.delete(crawl_id)
```

### monitor

Monitor a webpage for changes on a schedule.

```python
from scrapegraph_py import ScrapeGraphAI, MonitorCreateRequest, MarkdownFormatConfig

sgai = ScrapeGraphAI()

# Create a monitor
mon = sgai.monitor.create(MonitorCreateRequest(
    url="https://example.com",
    name="Price Monitor",
    interval="0 * * * *",               # cron expression
    formats=[MarkdownFormatConfig()],
    webhook_url="https://...",          # optional
    fetch_config=FetchConfig(...),
))

# Manage monitors
sgai.monitor.list()
sgai.monitor.get(cron_id)
sgai.monitor.update(cron_id, MonitorUpdateRequest(interval="0 */6 * * *"))
sgai.monitor.pause(cron_id)
sgai.monitor.resume(cron_id)
sgai.monitor.delete(cron_id)
```

### history

Fetch request history.

```python
from scrapegraph_py import ScrapeGraphAI, HistoryFilter

sgai = ScrapeGraphAI()

history = sgai.history.list(HistoryFilter(
    service="scrape",                   # optional filter
    page=1,
    limit=20,
))

entry = sgai.history.get("request-id")
```

### credits / health

```python
from scrapegraph_py import ScrapeGraphAI

sgai = ScrapeGraphAI()

credits = sgai.credits()
# { remaining: 1000, used: 500, plan: "pro", jobs: { crawl: {...}, monitor: {...} } }

health = sgai.health()
# { status: "ok", uptime: 12345 }
```

## Async Client

All methods have async equivalents via `AsyncScrapeGraphAI`:

```python
import asyncio
from scrapegraph_py import AsyncScrapeGraphAI, ScrapeRequest

async def main():
    async with AsyncScrapeGraphAI() as sgai:
        result = await sgai.scrape(ScrapeRequest(url="https://example.com"))
        if result.status == "success":
            print(result.data["results"]["markdown"]["data"])
        else:
            print(result.error)

asyncio.run(main())
```

### Async Extract

```python
async with AsyncScrapeGraphAI() as sgai:
    res = await sgai.extract(ExtractRequest(
        url="https://example.com",
        prompt="Extract product names and prices",
    ))
```

### Async Search

```python
async with AsyncScrapeGraphAI() as sgai:
    res = await sgai.search(SearchRequest(
        query="best programming languages 2024",
        num_results=5,
    ))
```

### Async Crawl

```python
async with AsyncScrapeGraphAI() as sgai:
    start = await sgai.crawl.start(CrawlRequest(
        url="https://example.com",
        max_pages=50,
    ))
    status = await sgai.crawl.get(start.data["id"])
```

### Async Monitor

```python
async with AsyncScrapeGraphAI() as sgai:
    mon = await sgai.monitor.create(MonitorCreateRequest(
        url="https://example.com",
        name="Price Monitor",
        interval="0 * * * *",
    ))
```

## Examples

### Sync Examples

| Service | Example | Description |
|---------|---------|-------------|
| scrape | [`scrape_basic.py`](examples/scrape/scrape_basic.py) | Basic markdown scraping |
| scrape | [`scrape_multi_format.py`](examples/scrape/scrape_multi_format.py) | Multiple formats |
| scrape | [`scrape_json_extraction.py`](examples/scrape/scrape_json_extraction.py) | Structured JSON extraction |
| scrape | [`scrape_pdf.py`](examples/scrape/scrape_pdf.py) | PDF document parsing |
| scrape | [`scrape_with_fetchconfig.py`](examples/scrape/scrape_with_fetchconfig.py) | JS rendering, stealth mode |
| extract | [`extract_basic.py`](examples/extract/extract_basic.py) | AI data extraction |
| extract | [`extract_with_schema.py`](examples/extract/extract_with_schema.py) | Extraction with JSON schema |
| search | [`search_basic.py`](examples/search/search_basic.py) | Web search |
| search | [`search_with_extraction.py`](examples/search/search_with_extraction.py) | Search + AI extraction |
| crawl | [`crawl_basic.py`](examples/crawl/crawl_basic.py) | Start and monitor a crawl |
| crawl | [`crawl_with_formats.py`](examples/crawl/crawl_with_formats.py) | Crawl with formats |
| monitor | [`monitor_basic.py`](examples/monitor/monitor_basic.py) | Create a page monitor |
| monitor | [`monitor_with_webhook.py`](examples/monitor/monitor_with_webhook.py) | Monitor with webhook |
| utilities | [`credits.py`](examples/utilities/credits.py) | Check credits and limits |
| utilities | [`health.py`](examples/utilities/health.py) | API health check |
| utilities | [`history.py`](examples/utilities/history.py) | Request history |

### Async Examples

| Service | Example | Description |
|---------|---------|-------------|
| scrape | [`scrape_basic_async.py`](examples/scrape/scrape_basic_async.py) | Basic markdown scraping |
| scrape | [`scrape_multi_format_async.py`](examples/scrape/scrape_multi_format_async.py) | Multiple formats |
| scrape | [`scrape_json_extraction_async.py`](examples/scrape/scrape_json_extraction_async.py) | Structured JSON extraction |
| scrape | [`scrape_pdf_async.py`](examples/scrape/scrape_pdf_async.py) | PDF document parsing |
| scrape | [`scrape_with_fetchconfig_async.py`](examples/scrape/scrape_with_fetchconfig_async.py) | JS rendering, stealth mode |
| extract | [`extract_basic_async.py`](examples/extract/extract_basic_async.py) | AI data extraction |
| extract | [`extract_with_schema_async.py`](examples/extract/extract_with_schema_async.py) | Extraction with JSON schema |
| search | [`search_basic_async.py`](examples/search/search_basic_async.py) | Web search |
| search | [`search_with_extraction_async.py`](examples/search/search_with_extraction_async.py) | Search + AI extraction |
| crawl | [`crawl_basic_async.py`](examples/crawl/crawl_basic_async.py) | Start and monitor a crawl |
| crawl | [`crawl_with_formats_async.py`](examples/crawl/crawl_with_formats_async.py) | Crawl with formats |
| monitor | [`monitor_basic_async.py`](examples/monitor/monitor_basic_async.py) | Create a page monitor |
| monitor | [`monitor_with_webhook_async.py`](examples/monitor/monitor_with_webhook_async.py) | Monitor with webhook |
| utilities | [`credits_async.py`](examples/utilities/credits_async.py) | Check credits and limits |
| utilities | [`health_async.py`](examples/utilities/health_async.py) | API health check |
| utilities | [`history_async.py`](examples/utilities/history_async.py) | Request history |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SGAI_API_KEY` | Your ScrapeGraphAI API key | — |
| `SGAI_API_URL` | Override API base URL | `https://v2-api.scrapegraphai.com/api/v2` |
| `SGAI_DEBUG` | Enable debug logging (`"1"`) | off |
| `SGAI_TIMEOUT` | Request timeout in seconds | `120` |

## Development

```bash
uv sync
uv run pytest tests/              # unit tests
uv run pytest tests/test_integration.py  # live API tests (requires SGAI_API_KEY)
uv run ruff check .               # lint
```

## License

MIT - [ScrapeGraphAI](https://scrapegraphai.com)
