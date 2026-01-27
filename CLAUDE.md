# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# DOCS
We keep all important docs in .agent folder and keep updating them, structure like below:
- `.agent/`
  - `Tasks`: PRD & implementation plan for each feature
  - `System`: Document the current state of the system (project structure, tech stack, SDK architecture, etc.)
  - `SOP`: Best practices of execute certain tasks (e.g. how to add a new endpoint, how to release a version, etc.)
  - `README.md`: an index of all the documentations we have so people know what & where to look for things

We should always update `.agent` docs after we implement certain feature, to make sure it fully reflects the up-to-date information.

Before you plan any implementation, always read the `.agent/README.md` first to get context.

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

## Project Overview

**scrapegraph-sdk** is a repository containing the official Python SDK for the ScrapeGraph AI API. It provides a Python client for intelligent web scraping powered by AI.

## Repository Structure

```
scrapegraph-sdk/
├── scrapegraph-py/         # Python SDK
├── cookbook/               # Usage examples and tutorials
├── .github/workflows/      # GitHub Actions for CI/CD
├── .agent/                 # Documentation hub (read this!)
├── package.json            # Root package config (semantic-release)
└── README.md              # Main repository README
```

## Tech Stack

### Python SDK
- **Language**: Python 3.10+
- **Package Manager**: uv (recommended) or pip
- **Core Dependencies**: requests, pydantic, python-dotenv, aiohttp
- **Optional Dependencies**:
  - `html`: beautifulsoup4 (for HTML validation when using `website_html`)
  - `langchain`: langchain, langchain-community, langchain-scrapegraph (for Langchain integrations)
- **Testing**: pytest, pytest-asyncio, pytest-mock, aioresponses
- **Code Quality**: black, isort, ruff, mypy, pre-commit
- **Documentation**: mkdocs, mkdocs-material
- **Build**: hatchling
- **Release**: semantic-release

## Common Development Commands

### Python SDK

```bash
# Navigate to Python SDK
cd scrapegraph-py

# Install dependencies (recommended - using uv)
pip install uv
uv sync

# Install dependencies (alternative - using pip)
pip install -e .

# Install pre-commit hooks
uv run pre-commit install
# or: pre-commit install

# Run all tests
uv run pytest tests/ -v
# or: pytest tests/ -v

# Run specific test
uv run pytest tests/test_smartscraper.py -v

# Run tests with coverage
uv run pytest --cov=scrapegraph_py --cov-report=html tests/

# Format code
uv run black scrapegraph_py tests
# or: make format

# Sort imports
uv run isort scrapegraph_py tests

# Lint code
uv run ruff check scrapegraph_py tests
# or: make lint

# Type check
uv run mypy scrapegraph_py
# or: make type-check

# Build documentation
uv run mkdocs build
# or: make docs

# Serve documentation locally
uv run mkdocs serve
# or: make serve-docs

# Run all checks (lint + type-check + test + docs)
make all

# Build package
uv build
# or: make build

# Clean build artifacts
make clean
```

## Project Architecture

### Python SDK (`scrapegraph-py/`)

**Core Components:**

1. **Client Classes** (`scrapegraph_py/`):
   - `client.py` - Synchronous client with all endpoint methods
   - `async_client.py` - Asynchronous client (same interface, async/await)
   - Both clients support the same API surface

2. **Models** (`scrapegraph_py/models/`):
   - Pydantic models for request/response validation
   - `smartscraper.py` - SmartScraper request/response schemas
   - `searchscraper.py` - SearchScraper schemas
   - `crawl.py` - Crawler schemas
   - `markdownify.py` - Markdownify schemas
   - `agenticscraper.py` - AgenticScraper schemas
   - `scrape.py` - Scrape schemas
   - `scheduled_jobs.py` - Scheduled Jobs schemas
   - `schema.py` - Schema generation models
   - `feedback.py` - Feedback models

3. **Utilities** (`scrapegraph_py/`):
   - `config.py` - Configuration constants (API base URL, timeouts)
   - `logger.py` - Logging configuration with colored output
   - `exceptions.py` - Custom exception classes
   - `utils/` - Helper functions

4. **Testing** (`tests/`):
   - `test_client.py` - Sync client tests
   - `test_async_client.py` - Async client tests
   - Individual endpoint tests
   - Uses pytest with mocking (aioresponses, responses)

5. **Documentation** (`docs/`):
   - MkDocs-based documentation
   - Auto-generated API reference from docstrings

**Key Patterns:**
- **Dual Client Design**: Sync and async clients with identical APIs
- **Pydantic Validation**: Strong typing for all request/response data
- **Environment Variables**: Support `SGAI_API_KEY` env var for auth
- **Comprehensive Logging**: Detailed logs with configurable levels
- **Type Safety**: Full mypy strict mode compliance

## API Coverage

The SDK supports all ScrapeGraph AI API endpoints:

| Endpoint | Python Method | Purpose |
|----------|---------------|---------|
| SmartScraper | `client.smartscraper()` | AI data extraction |
| SearchScraper | `client.searchscraper()` | Multi-URL search |
| Markdownify | `client.markdownify()` | HTML to Markdown |
| Crawler | `client.crawler()` | Sitemap & crawling |
| AgenticScraper | `client.agentic_scraper()` | Browser automation |
| Scrape | `client.scrape()` | Basic HTML fetch |
| Scheduled Jobs | `client.create_scheduled_job()`, etc. | Cron scheduling |
| Credits | `client.get_credits()` | Balance check |
| Feedback | `client.send_feedback()` | Rating/feedback |
| Schema Gen | `client.generate_schema()` | AI schema creation |

## Development Workflow

### Adding a New Endpoint

1. Add request/response models in `scrapegraph_py/models/new_endpoint.py`
2. Add sync method to `scrapegraph_py/client.py`
3. Add async method to `scrapegraph_py/async_client.py`
4. Export models in `scrapegraph_py/models/__init__.py`
5. Add tests in `tests/test_new_endpoint.py`
6. Update examples in `examples/`
7. Update README.md with usage examples

### Testing Strategy

- Unit tests for models (Pydantic validation)
- Integration tests for client methods (mocked HTTP)
- Use `aioresponses` for async client testing
- Use `responses` for sync client testing
- Mock API responses to avoid real API calls in CI
- Run `pytest --cov` for coverage reports

### Release Process

The SDK uses **semantic-release** for automated versioning:

1. **Commit with semantic messages:**
   - `feat: add new endpoint` → Minor bump (0.x.0)
   - `fix: handle timeout errors` → Patch bump (0.0.x)
   - `feat!: breaking API change` → Major bump (x.0.0)

2. **Merge to main branch**

3. **GitHub Actions automatically:**
   - Determines version bump
   - Updates version in `pyproject.toml`
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Publishes to PyPI

Configuration files:
- Python: `.releaserc.yml`
- GitHub workflow: `.github/workflows/release.yml`

## Important Conventions

### Python SDK

- **Code Style**:
  - Black formatting (line-length: 88)
  - isort for imports (Black profile)
  - Ruff for linting
  - mypy strict mode for type checking

- **Type Hints**:
  - All functions have type annotations
  - Use Pydantic models for complex data
  - Use `Optional[T]` for nullable values

- **Docstrings**:
  - Google-style docstrings
  - Document all public methods
  - Include examples in docstrings

- **Testing**:
  - Pytest for all tests
  - Mock external HTTP calls
  - Aim for >80% coverage

## Environment Variables

The SDK supports API key via environment variable:

- **Python**: `SGAI_API_KEY`

Usage:
```bash
export SGAI_API_KEY="your-api-key-here"
```

Then initialize client without passing API key:
```python
from scrapegraph_py import Client
client = Client()  # Uses SGAI_API_KEY env var
```

## Common Patterns

### Using Sync Client

```python
from scrapegraph_py import Client

client = Client(api_key="your-key")

response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract title and description"
)

print(response.result)
```

### Using Async Client

```python
from scrapegraph_py import AsyncClient
import asyncio

async def main():
    async with AsyncClient(api_key="your-key") as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract title"
        )
        print(response.result)

asyncio.run(main())
```

### Using Output Schema

```python
from pydantic import BaseModel, Field
from scrapegraph_py import Client

class Article(BaseModel):
    title: str = Field(description="Article title")
    author: str = Field(description="Author name")

client = Client(api_key="your-key")
response = client.smartscraper(
    website_url="https://news.example.com",
    user_prompt="Extract article data",
    output_schema=Article
)
```

## File Locations Reference

### Python SDK Key Files

- Entry points: `scrapegraph_py/__init__.py`, `scrapegraph_py/client.py`, `scrapegraph_py/async_client.py`
- Models: `scrapegraph_py/models/`
- Config: `pyproject.toml`, `pytest.ini`, `Makefile`
- Tests: `tests/`
- Examples: `examples/`
- Docs: `docs/` (MkDocs)

### Root Level

- Monorepo config: `package.json` (semantic-release)
- Documentation: `.agent/README.md` (read this!)
- Examples: `cookbook/`
- CI/CD: `.github/workflows/`

## Debugging

### Python SDK Debug Mode

Enable detailed logging:
```python
import logging
from scrapegraph_py import Client

logging.basicConfig(level=logging.DEBUG)
client = Client(api_key="your-key")
```

## Cookbook

The `cookbook/` directory contains practical examples:
- Authentication patterns
- Error handling
- Pagination
- Scheduled jobs
- Advanced features

Refer to cookbook for real-world usage patterns.

## External Documentation

- [ScrapeGraph AI API Documentation](https://docs.scrapegraphai.com)
- [Python SDK on PyPI](https://pypi.org/project/scrapegraph-py/)
- [GitHub Repository](https://github.com/ScrapeGraphAI/scrapegraph-sdk)

## Support

- Email: support@scrapegraphai.com
- GitHub Issues: https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues
- Documentation: https://docs.scrapegraphai.com
