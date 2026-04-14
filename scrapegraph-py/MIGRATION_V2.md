# Migration Guide: scrapegraph-py v1 → v2

This guide covers all breaking changes when upgrading from `scrapegraph-py` v1.x to v2.0.

## Installation

```bash
pip install scrapegraph-py==2.0.0
```

## Overview of Changes

| Area | v1 | v2 |
|------|----|----|
| **Package version** | 1.x | 2.0.0 |
| **API base URL** | `https://api.scrapegraphai.com/v1` | `https://api.scrapegraphai.com/api/v2` |
| **Auth header** | `SGAI-APIKEY: <key>` | `Authorization: Bearer <key>` (+ `SGAI-APIKEY` for backwards compat) |
| **SDK version header** | None | `X-SDK-Version: python@2.0.0` |
| **Client init** | `Client(api_key=...)` | `Client(api_key=..., base_url=...)` |
| **Crawl methods** | `client.crawl(...)` | `client.crawl.start(...)` (namespaced) |
| **Scheduled jobs** | `client.create_scheduled_job(...)` | `client.monitor.create(...)` (namespaced) |

---

## Client Initialization

The `Client` and `AsyncClient` constructors now accept an optional `base_url` parameter and no longer support `mock`, `mock_handler`, or `mock_responses`.

### v1

```python
from scrapegraph_py import Client

client = Client(
    api_key="sgai-...",
    verify_ssl=True,
    timeout=30,
    max_retries=3,
    retry_delay=1.0,
    mock=False,
    mock_handler=None,
    mock_responses=None,
)
```

### v2

```python
from scrapegraph_py import Client

client = Client(
    api_key="sgai-...",
    base_url="https://api.scrapegraphai.com/api/v2",  # optional override
    verify_ssl=True,
    timeout=30,
    max_retries=3,
    retry_delay=1.0,
)
```

> **Note:** The `mock`, `mock_handler`, and `mock_responses` parameters have been removed. Use standard mocking libraries (`responses`, `aioresponses`, `unittest.mock`) for testing instead.

---

## Endpoint Migration Reference

### SmartScraper → `extract()`

The `smartscraper()` method has been renamed to `extract()`. The parameter names have changed.

#### v1

```python
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the main heading and description",
    output_schema=MyPydanticModel,
    headers={"User-Agent": "MyBot"},
    cookies={"session": "abc123"},
    number_of_scrolls=3,
    render_heavy_js=True,
    stealth=True,
    wait_ms=2000,
)

# Get result by ID
result = client.get_smartscraper(request_id)
```

#### v2

```python
from scrapegraph_py import FetchConfig

response = client.extract(
    url="https://example.com",
    prompt="Extract the main heading and description",
    schema=MyPydanticModel,
    fetch_config=FetchConfig(
        mode="js",
        stealth=True,
        headers={"User-Agent": "MyBot"},
        cookies={"session": "abc123"},
        scrolls=3,
        wait=2000,
    ),
)
```

| v1 parameter | v2 equivalent |
|---|---|
| `website_url` | `url` |
| `user_prompt` | `prompt` |
| `output_schema` | `schema` |
| `headers` | `fetch_config=FetchConfig(headers=...)` |
| `cookies` | `fetch_config=FetchConfig(cookies=...)` |
| `number_of_scrolls` | `fetch_config=FetchConfig(scrolls=...)` |
| `render_heavy_js` | `fetch_config=FetchConfig(mode="js")` |
| `stealth` | `fetch_config=FetchConfig(stealth=True)` |
| `wait_ms` | `fetch_config=FetchConfig(wait=...)` |
| `mock` | Removed |
| `plain_text` | Removed |
| `total_pages` | Removed |
| `website_html` | Removed (URL only) |
| `website_markdown` | Removed (URL only) |
| `return_toon` | Removed |

> **Note:** `get_smartscraper()` has been removed. The `extract()` response is returned directly.

---

### SearchScraper → `search()`

#### v1

```python
response = client.searchscraper(
    user_prompt="What is the latest version of Python?",
    num_results=5,
    output_schema=MyModel,
    extraction_mode=True,
    stealth=True,
    location_geo_code="us",
    time_range=TimeRange.PAST_WEEK,
)

result = client.get_searchscraper(request_id)
```

#### v2

```python
response = client.search(
    query="What is the latest version of Python?",
    num_results=5,
    prompt="Extract key findings",
    schema=MyModel,
    country="us",
    time_range="past_week",
)
```

| v1 parameter | v2 equivalent |
|---|---|
| `user_prompt` | `query` |
| `num_results` | `num_results` (unchanged, default changed from 5 to 3) |
| `output_schema` | `schema` (now requires `prompt`) |
| `extraction_mode` | Removed (always AI extraction) |
| `stealth` | Removed (use `fetch_config=FetchConfig(mode=...)`) |
| `location_geo_code` | `country` (renamed, matches `FetchConfig.country`) |
| `time_range` | `time_range` (values: `past_hour`, `past_24_hours`, `past_week`, `past_month`, `past_year`) |
| `mock` | Removed |
| `return_toon` | Removed |

New parameters in v2: `format`, `mode`, `prompt`, `fetch_config`.

> **Note:** `get_searchscraper()` has been removed.

---

### Scrape → `scrape()`

The `scrape()` method name stays the same but the parameters and request format have changed. v2 uses a format-based approach (markdown, html, screenshot, branding).

#### v1

```python
response = client.scrape(
    website_url="https://example.com",
    render_heavy_js=True,
    branding=True,
    headers={"User-Agent": "MyBot"},
    stealth=True,
    wait_ms=2000,
)

result = client.get_scrape(request_id)
```

#### v2

```python
from scrapegraph_py import FetchConfig

# Get markdown (default)
response = client.scrape("https://example.com")

# Get HTML
response = client.scrape("https://example.com", format="html")

# Get screenshot
response = client.scrape("https://example.com", format="screenshot")

# With fetch config
response = client.scrape(
    "https://example.com",
    format="markdown",
    fetch_config=FetchConfig(
        mode="js",
        stealth=True,
        wait=2000,
        headers={"User-Agent": "MyBot"},
    ),
)
```

| v1 parameter | v2 equivalent |
|---|---|
| `website_url` | `url` (positional) |
| `render_heavy_js` | `fetch_config=FetchConfig(mode="js")` |
| `branding` | `format="branding"` |
| `headers` | `fetch_config=FetchConfig(headers=...)` |
| `stealth` | `fetch_config=FetchConfig(stealth=True)` |
| `wait_ms` | `fetch_config=FetchConfig(wait=...)` |
| `mock` | Removed |
| `return_toon` | Removed |

> **Note:** `get_scrape()` has been removed.

---

### Markdownify → `scrape(format="markdown")`

The `markdownify()` endpoint has been replaced by `scrape()` with `format="markdown"`.

#### v1

```python
response = client.markdownify(
    website_url="https://example.com",
    render_heavy_js=True,
    stealth=True,
)
```

#### v2

```python
response = client.scrape(
    "https://example.com",
    format="markdown",
    fetch_config=FetchConfig(mode="js", stealth=True),
)
```

---

### Crawl → `crawl.start()` / `crawl.status()` / `crawl.stop()` / `crawl.resume()`

Crawl methods are now **namespaced** under `client.crawl.*`. The parameter names have been simplified.

#### v1

```python
# Start a crawl
response = client.crawl(
    url="https://example.com",
    prompt="Extract page titles",
    data_schema={"type": "object", "properties": {"title": {"type": "string"}}},
    extraction_mode=True,
    depth=2,
    max_pages=10,
    same_domain_only=True,
    batch_size=5,
    sitemap=False,
    headers={"User-Agent": "MyBot"},
    render_heavy_js=True,
    stealth=True,
    include_paths=["/blog/*"],
    exclude_paths=["/admin/*"],
    webhook_url="https://example.com/webhook",
    wait_ms=1000,
)

# Get status
result = client.get_crawl(crawl_id)
```

#### v2

```python
from scrapegraph_py import FetchConfig

# Start a crawl
response = client.crawl.start(
    "https://example.com",
    depth=2,
    max_pages=10,
    format="markdown",  # or "html"
    include_patterns=["/blog/*"],
    exclude_patterns=["/admin/*"],
    fetch_config=FetchConfig(
        mode="js",
        stealth=True,
        wait=1000,
        headers={"User-Agent": "MyBot"},
    ),
)

# Get status
result = client.crawl.status(crawl_id)

# Stop a running crawl (NEW)
client.crawl.stop(crawl_id)

# Resume a stopped crawl (NEW)
client.crawl.resume(crawl_id)
```

| v1 parameter | v2 equivalent |
|---|---|
| `url` | `url` (positional) |
| `prompt` | Removed (use `format` instead) |
| `data_schema` | Removed (use `format` instead) |
| `extraction_mode` | Replaced by `format` ("markdown" or "html") |
| `depth` | `depth` (unchanged) |
| `max_pages` | `max_pages` (unchanged) |
| `include_paths` | `include_patterns` |
| `exclude_paths` | `exclude_patterns` |
| `headers`, `stealth`, `render_heavy_js`, `wait_ms` | Moved to `fetch_config=FetchConfig(mode=..., wait=..., headers=...)` |
| `same_domain_only` | Removed |
| `batch_size` | Removed |
| `sitemap` | Removed |
| `cache_website` | Removed |
| `breadth` | Removed |
| `webhook_url` | Removed |
| `return_toon` | Removed |

| v1 method | v2 method |
|---|---|
| `client.crawl(...)` | `client.crawl.start(...)` |
| `client.get_crawl(id)` | `client.crawl.status(id)` |
| — | `client.crawl.stop(id)` **(NEW)** |
| — | `client.crawl.resume(id)` **(NEW)** |

---

### Scheduled Jobs → `monitor.*`

The entire scheduled jobs API has been replaced by the **monitor** namespace. Monitors are simpler: instead of configuring a `service_type` + `job_config`, you directly provide a `url`, `prompt`, and `interval` (a cron expression).

#### v1

```python
# Create
job = client.create_scheduled_job(
    job_name="Daily Scraper",
    service_type="smartscraper",
    cron_expression="0 9 * * *",
    job_config={
        "website_url": "https://example.com",
        "user_prompt": "Extract company info",
    },
    is_active=True,
)

# List
jobs = client.get_scheduled_jobs(page=1, page_size=20)

# Get one
job = client.get_scheduled_job(job_id)

# Update
client.update_scheduled_job(job_id, job_name="Updated Name")

# Pause / Resume / Delete
client.pause_scheduled_job(job_id)
client.resume_scheduled_job(job_id)
client.delete_scheduled_job(job_id)

# Trigger manually
client.trigger_scheduled_job(job_id)

# Execution history
execs = client.get_job_executions(job_id, page=1, page_size=20)
```

#### v2

```python
from scrapegraph_py import FetchConfig

# Create
monitor = client.monitor.create(
    name="Daily Scraper",
    url="https://example.com",
    prompt="Extract company info",
    interval="0 9 * * *",
    schema={"type": "object", "properties": {"name": {"type": "string"}}},
    fetch_config=FetchConfig(stealth=True),
)

# List
monitors = client.monitor.list()

# Get one
monitor = client.monitor.get(monitor_id)

# Pause / Resume / Delete
client.monitor.pause(monitor_id)
client.monitor.resume(monitor_id)
client.monitor.delete(monitor_id)
```

| v1 method | v2 method |
|---|---|
| `client.create_scheduled_job(...)` | `client.monitor.create(...)` |
| `client.get_scheduled_jobs(...)` | `client.monitor.list()` |
| `client.get_scheduled_job(id)` | `client.monitor.get(id)` |
| `client.pause_scheduled_job(id)` | `client.monitor.pause(id)` |
| `client.resume_scheduled_job(id)` | `client.monitor.resume(id)` |
| `client.delete_scheduled_job(id)` | `client.monitor.delete(id)` |
| `client.update_scheduled_job(...)` | Removed |
| `client.replace_scheduled_job(...)` | Removed |
| `client.trigger_scheduled_job(id)` | Removed |
| `client.get_job_executions(...)` | Removed |

---

### Schema Generation → `schema()`

#### v1

```python
response = client.generate_schema(
    user_prompt="Product with name, price, and rating",
    existing_schema=None,
)

status = client.get_schema_status(request_id)
```

#### v2

```python
response = client.schema(
    prompt="Product with name, price, and rating",
    existing_schema=None,
)
```

| v1 parameter | v2 equivalent |
|---|---|
| `user_prompt` | `prompt` |
| `existing_schema` | `existing_schema` (unchanged) |

> **Note:** `get_schema_status()` has been removed.

---

### Credits → `credits()`

#### v1

```python
credits = client.get_credits()
```

#### v2

```python
credits = client.credits()
```

---

### New Endpoints in v2

#### `history()`

Retrieve your API request history with optional filters. This is new in v2.

```python
# Get all recent history
history = client.history()

# With filters
history = client.history(
    endpoint="scrape",
    status="completed",
    limit=10,
    offset=0,
)
```

---

## Removed Endpoints

The following v1 endpoints have been **removed** in v2:

| Removed endpoint | Replacement |
|---|---|
| `client.markdownify()` | `client.scrape(url, format="markdown")` |
| `client.get_markdownify(id)` | Removed (response is direct) |
| `client.agenticscraper()` | Removed |
| `client.get_agenticscraper(id)` | Removed |
| `client.sitemap(url)` | Removed |
| `client.healthz()` | Removed |
| `client.submit_feedback(...)` | Removed |
| All `get_*` polling methods | Removed (responses are direct) |

---

## Shared Configuration Models

v2 introduces `FetchConfig` — a reusable configuration object that replaces the scattered per-method fetch parameters from v1.

### FetchConfig

Controls how pages are fetched. Used by `scrape()`, `extract()`, `crawl.start()`, and `monitor.create()`.

```python
from scrapegraph_py import FetchConfig

config = FetchConfig(
    mode="js",           # Fetch mode: auto, fast, js
    stealth=True,        # Use residential proxies (+5 credits)
    timeout=30000,       # Request timeout in ms (1000-60000)
    wait=2000,           # Wait after page load in ms (0-30000)
    headers={"k": "v"},  # Custom HTTP headers
    cookies={"k": "v"},  # Cookies to send
    country="us",        # Two-letter country code for geo-located requests
    scrolls=3,           # Number of page scrolls (0-100)
    mock=False,          # Use mock mode for testing
)
```

**Available fetch modes:**

| Mode | Description |
|---|---|
| `auto` | Automatically selects the best provider chain (default) |
| `fast` | Direct HTTP fetch via impit — fastest, no JS rendering |
| `js` | Headless browser rendering for JavaScript-heavy pages |

**Stealth:** Set `stealth=True` to use residential proxies for bot detection bypass (+5 credits per request). Selecting a `country` automatically enables stealth.

---

## Removed Features

| Feature | Notes |
|---|---|
| **Mock mode** (`mock=True`) | Use `responses` / `aioresponses` / `unittest.mock` for testing |
| **TOON format** (`return_toon=True`) | Removed entirely |
| **`from_env()` mock support** | `from_env()` no longer accepts `mock`, `mock_handler`, `mock_responses` |
| **`website_html` / `website_markdown` input** | `extract()` only accepts URLs, not raw HTML/markdown |
| **`TimeRange` enum** | Removed (was used by `searchscraper`) |
| **`SitemapRequest` / `SitemapResponse`** | Removed |
| **All `Get*Request` models** | Removed (no more polling by ID) |

---

## Async Client

The `AsyncClient` has the exact same API surface as `Client` — all the same changes apply. Every method is `async` and crawl/monitor namespaces use `await`:

```python
import asyncio
from scrapegraph_py import AsyncClient

async def main():
    async with AsyncClient(api_key="sgai-...") as client:
        # All the same methods, just with await
        result = await client.scrape("https://example.com")
        result = await client.extract("https://example.com", prompt="Extract title")
        result = await client.search("python web scraping")

        # Namespaced methods also use await
        job = await client.crawl.start("https://example.com", depth=2)
        status = await client.crawl.status(job["id"])

        monitor = await client.monitor.create(
            name="Tracker",
            url="https://example.com",
            prompt="Extract prices",
            interval="0 9 * * *",
        )

asyncio.run(main())
```

---

## Quick Find-and-Replace Cheatsheet

For a fast migration, search your codebase for these patterns:

| Search for | Replace with |
|---|---|
| `client.smartscraper(` | `client.extract(` |
| `website_url=` | `url=` |
| `user_prompt=` | `prompt=` (in extract/schema) or `query=` (in search) |
| `client.searchscraper(` | `client.search(` |
| `client.markdownify(` | `client.scrape(` |
| `client.get_smartscraper(` | Remove (response is direct) |
| `client.get_searchscraper(` | Remove |
| `client.get_scrape(` | Remove |
| `client.get_markdownify(` | Remove |
| `client.get_crawl(` | `client.crawl.status(` |
| `client.crawl(` | `client.crawl.start(` |
| `client.agenticscraper(` | Remove |
| `client.get_agenticscraper(` | Remove |
| `client.sitemap(` | Remove |
| `client.healthz()` | Remove |
| `client.submit_feedback(` | Remove |
| `client.get_credits()` | `client.credits()` |
| `client.generate_schema(` | `client.schema(` |
| `client.get_schema_status(` | Remove |
| `client.create_scheduled_job(` | `client.monitor.create(` |
| `client.get_scheduled_jobs(` | `client.monitor.list()` |
| `client.get_scheduled_job(` | `client.monitor.get(` |
| `client.pause_scheduled_job(` | `client.monitor.pause(` |
| `client.resume_scheduled_job(` | `client.monitor.resume(` |
| `client.delete_scheduled_job(` | `client.monitor.delete(` |
| `client.trigger_scheduled_job(` | Remove |
| `client.update_scheduled_job(` | Remove |
| `client.replace_scheduled_job(` | Remove |
| `client.get_job_executions(` | Remove |
| `return_toon=True` | Remove |
| `render_heavy_js=` | `fetch_config=FetchConfig(mode="js")` |
| `from scrapegraph_py.models.smartscraper import` | Remove |
| `from scrapegraph_py.models.searchscraper import` | Remove |
| `from scrapegraph_py.models.markdownify import` | Remove |
| `from scrapegraph_py.models.agenticscraper import` | Remove |
| `from scrapegraph_py.models.sitemap import` | Remove |
| `from scrapegraph_py.models.feedback import` | Remove |
| `from scrapegraph_py.models.scheduled_jobs import` | Remove |
