# ScrapeGraphAI SDK - Project Architecture

**Last Updated:** January 2025
**Version:** Python SDK 1.12.2

## Table of Contents
- [System Overview](#system-overview)
- [Repository Structure](#repository-structure)
- [Python SDK Architecture](#python-sdk-architecture)
- [API Endpoint Coverage](#api-endpoint-coverage)
- [Authentication & Configuration](#authentication--configuration)
- [Testing Strategy](#testing-strategy)
- [Release & Publishing](#release--publishing)
- [External Dependencies](#external-dependencies)

---

## System Overview

The **scrapegraph-sdk** repository contains the official Python client SDK for the ScrapeGraph AI API. The SDK provides comprehensive functionality for intelligent web scraping powered by AI, with language-specific implementations optimized for the Python ecosystem.

**Key Features:**
- ✅ **Complete API Coverage**: All 10 ScrapeGraph AI endpoints supported
- ✅ **Sync & Async**: Python supports both sync and async clients
- ✅ **Type Safety**: Pydantic models for data validation
- ✅ **Automated Releases**: Semantic versioning with semantic-release
- ✅ **Comprehensive Testing**: Unit and integration tests
- ✅ **Production Ready**: Used by thousands of developers worldwide

---

## Repository Structure

```
scrapegraph-sdk/
├── scrapegraph-py/              # Python SDK (PyPI: scrapegraph-py)
│   ├── scrapegraph_py/          # Source code
│   ├── tests/                   # Pytest tests
│   ├── examples/                # Usage examples
│   ├── docs/                    # MkDocs documentation
│   ├── pyproject.toml          # Package metadata & dependencies
│   ├── Makefile                # Development tasks
│   └── README.md               # Python SDK documentation
│
├── cookbook/                    # Cross-language usage examples
├── .github/workflows/           # GitHub Actions CI/CD
│   ├── release.yml             # Python release automation
│   └── tests.yml               # Test automation
│
├── .agent/                      # Documentation hub
│   ├── README.md               # Documentation index
│   ├── system/                 # Architecture documentation
│   ├── tasks/                  # Feature PRDs
│   └── sop/                    # Standard operating procedures
│
├── package.json                # Root package.json (semantic-release)
├── CLAUDE.md                   # Claude Code instructions
└── README.md                   # Main repository documentation
```

---

## Python SDK Architecture

### Technology Stack

**Core:**
- **Python**: 3.10+ (3.11+ recommended)
- **Package Manager**: uv (recommended) or pip
- **Build System**: hatchling 1.26.3

**Dependencies:**
- **requests** 2.32.3+ - HTTP client for sync operations
- **aiohttp** 3.10+ - Async HTTP client
- **pydantic** 2.10.2+ - Data validation and modeling
- **python-dotenv** 1.0.1+ - Environment variable management

**Optional Dependencies:**
- **beautifulsoup4** 4.12.3+ - HTML parsing (for HTML validation when using `website_html`)
  - Install with: `pip install scrapegraph-py[html]`
- **langchain** 0.3.0+ - Langchain integration for AI workflows
- **langchain-community** 0.2.11+ - Community integrations for Langchain
- **langchain-scrapegraph** 0.1.0+ - ScrapeGraph integration for Langchain
  - Install with: `pip install scrapegraph-py[langchain]`

**Development Tools:**
- **pytest** 7.4.0+ - Testing framework
- **pytest-asyncio** 0.23.8+ - Async test support
- **pytest-mock** 3.14.0 - Mocking support
- **pytest-cov** 6.0.0+ - Coverage reporting
- **aioresponses** 0.7.7+ - Async HTTP mocking
- **responses** 0.25.3+ - Sync HTTP mocking
- **black** 24.10.0+ - Code formatting
- **isort** 5.13.2+ - Import sorting
- **ruff** 0.8.0+ - Fast linting
- **mypy** 1.13.0+ - Type checking
- **pre-commit** 4.0.1+ - Git hooks

**Documentation:**
- **mkdocs** 1.6.1+ - Documentation generator
- **mkdocs-material** 9.5.46+ - Material theme
- **mkdocstrings-python** 1.12.2+ - Python API docs

### Project Structure

```
scrapegraph-py/
├── scrapegraph_py/
│   ├── __init__.py              # Package exports (Client, AsyncClient)
│   ├── client.py                # Synchronous client implementation
│   ├── async_client.py          # Asynchronous client implementation
│   ├── config.py                # Configuration constants
│   ├── logger.py                # Logging configuration
│   ├── exceptions.py            # Custom exception classes
│   │
│   ├── models/                  # Pydantic request/response models
│   │   ├── __init__.py          # Model exports
│   │   ├── smartscraper.py      # SmartScraper models
│   │   ├── searchscraper.py     # SearchScraper models
│   │   ├── crawl.py             # Crawler models
│   │   ├── markdownify.py       # Markdownify models
│   │   ├── scrape.py            # Scrape models
│   │   ├── agenticscraper.py    # AgenticScraper models
│   │   ├── scheduled_jobs.py    # Scheduled Jobs models
│   │   ├── schema.py            # Schema generation models
│   │   └── feedback.py          # Feedback models
│   │
│   └── utils/                   # Utility functions
│       └── helpers.py           # HTTP helpers, validation
│
├── tests/                       # Test suite
│   ├── conftest.py             # Pytest fixtures
│   ├── test_client.py          # Sync client tests
│   ├── test_async_client.py    # Async client tests
│   ├── test_smartscraper.py    # SmartScraper endpoint tests
│   ├── test_searchscraper.py   # SearchScraper tests
│   ├── test_crawler.py         # Crawler tests
│   └── ...                     # Other endpoint tests
│
├── examples/                    # Usage examples
│   ├── basic_usage.py
│   ├── async_usage.py
│   ├── with_schema.py
│   ├── pagination.py
│   └── ...
│
├── docs/                        # MkDocs documentation
│   ├── index.md
│   ├── api/                    # Auto-generated API docs
│   └── mkdocs.yml              # MkDocs configuration
│
├── pyproject.toml              # Package metadata & tool configs
├── pytest.ini                  # Pytest configuration
├── Makefile                    # Development tasks
├── .releaserc.yml              # Semantic-release config
├── .pre-commit-config.yaml     # Pre-commit hooks
└── README.md                   # Python SDK documentation
```

### Client Architecture

**Dual Client Design:**

The Python SDK implements two client classes with identical APIs:

1. **`Client`** (`client.py`) - Synchronous client
   - Uses `requests` library
   - Blocking operations
   - Simpler for scripts and synchronous applications

2. **`AsyncClient`** (`async_client.py`) - Asynchronous client
   - Uses `aiohttp` library
   - Non-blocking operations
   - Context manager support (`async with`)
   - Ideal for concurrent operations and async frameworks

Both clients share the same method signatures and return types, making it easy to switch between sync and async implementations.

**Client Features:**
- **Environment Variable Support**: Auto-loads `SGAI_API_KEY`
- **SSL Verification**: Configurable SSL cert verification
- **Timeouts**: Configurable request timeouts
- **Retries**: Built-in retry logic with exponential backoff
- **Logging**: Detailed debug logs with colored output
- **Error Handling**: Custom exceptions with detailed error messages

**Example Usage:**

```python
# Synchronous Client
from scrapegraph_py import Client

client = Client(api_key="your-key")
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract title"
)

# Asynchronous Client
from scrapegraph_py import AsyncClient
import asyncio

async def main():
    async with AsyncClient(api_key="your-key") as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract title"
        )

asyncio.run(main())
```

### Pydantic Models

All API requests and responses are modeled using **Pydantic v2**, providing:
- **Type Validation**: Automatic validation of input/output data
- **Serialization**: JSON encoding/decoding
- **IDE Support**: Type hints for autocomplete
- **Documentation**: Schema generation for API docs

Models are organized by endpoint in `scrapegraph_py/models/`:

**Example Model:**
```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SmartScraperRequest(BaseModel):
    website_url: Optional[str] = Field(None, description="URL to scrape")
    website_html: Optional[str] = Field(None, description="HTML content to scrape")
    user_prompt: str = Field(..., description="Natural language prompt")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="Output schema")
    # ... more fields
```

### Configuration

**Constants** (`config.py`):
```python
API_BASE_URL = "https://api.scrapegraphai.com"
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "scrapegraph-py/1.12.2"
}
```

**Environment Variables:**
- `SGAI_API_KEY` - API key for authentication

### Logging

Configurable logging with colored output (`logger.py`):
- **DEBUG**: Detailed request/response logs
- **INFO**: Key operations and progress
- **WARNING**: Deprecation warnings
- **ERROR**: Error messages

### Testing

**Test Structure:**
- **Unit Tests**: Test individual functions and models
- **Integration Tests**: Test full request/response cycles with mocked HTTP
- **Fixtures**: Reusable test data in `conftest.py`

**Mocking Strategy:**
- **Sync tests**: Use `responses` library to mock `requests`
- **Async tests**: Use `aioresponses` to mock `aiohttp`

**Running Tests:**
```bash
# All tests
pytest tests/ -v

# With coverage
pytest --cov=scrapegraph_py --cov-report=html tests/

# Specific test
pytest tests/test_smartscraper.py -v
```

---

## API Endpoint Coverage

The SDK supports all ScrapeGraph AI API endpoints:

### 1. SmartScraper
**Purpose**: AI-powered web scraping with schema extraction

```python
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract product details",
    output_schema=ProductSchema  # Optional Pydantic model
)
```

**Features:**
- URL or HTML input
- Natural language prompts
- Optional output schema for structured data
- Pagination support
- Cookie support
- Infinite scrolling
- Heavy JS rendering

### 2. SearchScraper
**Purpose**: Multi-website search and extraction

```python
response = client.searchscraper(
    user_prompt="Find AI news articles",
    num_results=5
)
```

### 3. Crawler / SmartCrawler
**Purpose**: Sitemap generation and multi-page crawling

```python
response = client.crawler(
    website_url="https://example.com",
    max_depth=3
)
```

### 4. Markdownify
**Purpose**: HTML to Markdown conversion

```python
response = client.markdownify(
    website_url="https://example.com/article"
)
```

### 5. Scrape
**Purpose**: Basic HTML extraction

```python
response = client.scrape(
    url="https://example.com"
)
```

### 6. AgenticScraper
**Purpose**: Browser automation with AI-powered actions

```python
response = client.agentic_scraper(
    website_url="https://example.com",
    steps=["click button", "scroll down"],
    user_prompt="Extract data"
)
```

### 7. Scheduled Jobs
**Purpose**: Cron-based job scheduling

```python
# Create job
job = client.create_scheduled_job(
    name="Daily scrape",
    cron_expression="0 9 * * *",
    service_type="smartscraper",
    service_params={...}
)

# List jobs
jobs = client.list_scheduled_jobs()

# Update job
updated = client.update_scheduled_job(job_id, ...)

# Delete job
client.delete_scheduled_job(job_id)
```

### 8. Credits
**Purpose**: Check credit balance

```python
balance = client.get_credits()
```

### 9. Feedback
**Purpose**: Send ratings and feedback

```python
client.send_feedback(
    request_id="...",
    rating=5,
    feedback="Great results!"
)
```

### 10. Schema Generation
**Purpose**: AI-powered schema generation from prompts

```python
schema = client.generate_schema(
    user_prompt="Generate schema for product data",
    website_url="https://example.com"
)
```

---

## Authentication & Configuration

### Python SDK

**Method 1: Environment Variable**
```python
import os
os.environ['SGAI_API_KEY'] = 'sgai-...'

from scrapegraph_py import Client
client = Client()  # Auto-loads from env
```

**Method 2: Direct Initialization**
```python
from scrapegraph_py import Client
client = Client(api_key='sgai-...')
```

**Method 3: From Environment (class method)**
```python
from scrapegraph_py import Client
client = Client.from_env()  # Reads SGAI_API_KEY
```

**Configuration Options:**
```python
client = Client(
    api_key='sgai-...',
    verify_ssl=True,        # SSL verification
    timeout=30.0,           # Request timeout (seconds)
    max_retries=3,          # Retry attempts
    retry_delay=1.0         # Delay between retries
)
```

---

## Testing Strategy

### Python SDK Testing

**Test Framework**: pytest with plugins

**Test Types:**
1. **Unit Tests**: Model validation, utility functions
2. **Integration Tests**: Full request/response cycles with mocked HTTP

**Coverage Goals**:
- Code coverage: >80%
- All endpoints covered
- Both sync and async clients tested

**Mocking Strategy:**
```python
# Sync client tests with responses
import responses
from scrapegraph_py import Client

@responses.activate
def test_smartscraper():
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={"request_id": "123", "status": "completed"},
        status=200
    )

    client = Client(api_key="test-key")
    response = client.smartscraper(
        website_url="https://example.com",
        user_prompt="Extract title"
    )
    assert response.request_id == "123"
```

```python
# Async client tests with aioresponses
import pytest
from aioresponses import aioresponses
from scrapegraph_py import AsyncClient

@pytest.mark.asyncio
async def test_async_smartscraper():
    with aioresponses() as m:
        m.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={"request_id": "123", "status": "completed"}
        )

        async with AsyncClient(api_key="test-key") as client:
            response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract title"
            )
            assert response.request_id == "123"
```

---

## Release & Publishing

The SDK uses **semantic-release** for automated versioning and publishing.

### Semantic Versioning Rules

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add new feature` → **Minor** version bump (0.x.0)
- `fix: bug fix` → **Patch** version bump (0.0.x)
- `feat!: breaking change` or `BREAKING CHANGE:` in body → **Major** bump (x.0.0)
- `docs:`, `chore:`, `style:`, `refactor:`, `test:` → No version bump

### Release Workflow

1. Merge PR to `main` branch
2. GitHub Actions workflow triggers (`release.yml`)
3. semantic-release analyzes commits
4. Version bumped in `pyproject.toml`
5. `CHANGELOG.md` updated
6. Git tag created
7. GitHub release published
8. Package published to PyPI

### Configuration Files

**Python** (`.releaserc.yml`):
```yaml
branches:
  - main
plugins:
  - "@semantic-release/commit-analyzer"
  - "@semantic-release/release-notes-generator"
  - "@semantic-release/changelog"
  - ["semantic-release-pypi", { pkgdir: "scrapegraph-py" }]
  - "@semantic-release/github"
  - "@semantic-release/git"
```

### Manual Release (Emergency)

```bash
cd scrapegraph-py
uv build
twine upload dist/*
```

---

## External Dependencies

### Python SDK Dependencies

**Core Runtime:**
- **requests**: Sync HTTP client
- **aiohttp**: Async HTTP client
- **pydantic**: Data validation
- **python-dotenv**: Environment variables

**Optional Runtime (install with extras):**
- **beautifulsoup4**: HTML parsing (required when using `website_html`)
  - Install with: `pip install scrapegraph-py[html]`
- **langchain, langchain-community, langchain-scrapegraph**: Langchain integration
  - Install with: `pip install scrapegraph-py[langchain]`

**Development:**
- **pytest & plugins**: Testing framework
- **black, isort, ruff**: Code quality
- **mypy**: Type checking
- **mkdocs**: Documentation

### API Dependencies

The SDK depends on the ScrapeGraph AI API:
- **Base URL**: `https://api.scrapegraphai.com`
- **Authentication**: API key via `SGAI-APIKEY` header
- **API Version**: v1
- **Rate Limits**: Based on plan (see dashboard)

---

**For detailed usage examples, see the [cookbook](../../cookbook/) directory.**
**For contributing guidelines, see [.agent/README.md](../README.md).**
