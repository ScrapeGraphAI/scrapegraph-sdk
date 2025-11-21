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

**scrapegraph-sdk** is a monorepo containing official SDKs for the ScrapeGraph AI API. It provides both Python and JavaScript/TypeScript clients for intelligent web scraping powered by AI.

## Repository Structure

This is a **monorepo** containing two separate SDKs:

```
scrapegraph-sdk/
├── scrapegraph-py/         # Python SDK
├── scrapegraph-js/         # JavaScript/TypeScript SDK
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

### JavaScript SDK
- **Language**: JavaScript (ES6+)
- **Runtime**: Node.js
- **Package Manager**: npm
- **Code Quality**: ESLint, Prettier
- **Testing**: Native Node.js test files
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

### JavaScript SDK

```bash
# Navigate to JavaScript SDK
cd scrapegraph-js

# Install dependencies
npm install

# Run tests
npm test

# Run specific test
node test/test_smartscraper.js

# Format code
npm run format

# Lint code
npm run lint
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

### JavaScript SDK (`scrapegraph-js/`)

**Core Components:**

1. **Endpoint Modules** (`src/`):
   - Each endpoint has its own module
   - `smartScraper.js` - SmartScraper endpoint
   - `searchScraper.js` - SearchScraper endpoint
   - `crawl.js` - Crawler endpoint
   - `markdownify.js` - Markdownify endpoint
   - `agenticScraper.js` - AgenticScraper endpoint
   - `scrape.js` - Scrape endpoint
   - `scheduledJobs.js` - Scheduled Jobs management
   - `credits.js` - Credits endpoint
   - `feedback.js` - Feedback endpoint
   - `schema.js` - Schema generation

2. **Utilities** (`src/utils/`):
   - Helper functions for HTTP requests
   - Error handling utilities

3. **Entry Point** (`index.js`):
   - Main package entry exporting all functions

4. **Testing** (`test/`):
   - Individual test files for each endpoint
   - Integration test examples

**Key Patterns:**
- **Function-Based API**: Each endpoint is a standalone async function
- **Environment Variables**: Support `SGAI_APIKEY` env var
- **Async/Await**: All functions return Promises
- **Error Handling**: Try/catch recommended for all calls
- **Minimal Dependencies**: Lean implementation

## API Coverage

Both SDKs support all ScrapeGraph AI API endpoints:

| Endpoint | Python Method | JavaScript Function | Purpose |
|----------|---------------|---------------------|---------|
| SmartScraper | `client.smartscraper()` | `smartScraper()` | AI data extraction |
| SearchScraper | `client.searchscraper()` | `searchScraper()` | Multi-URL search |
| Markdownify | `client.markdownify()` | `markdownify()` | HTML to Markdown |
| Crawler | `client.crawler()` | `crawl()` | Sitemap & crawling |
| AgenticScraper | `client.agentic_scraper()` | `agenticScraper()` | Browser automation |
| Scrape | `client.scrape()` | `scrape()` | Basic HTML fetch |
| Scheduled Jobs | `client.create_scheduled_job()`, etc. | `createScheduledJob()`, etc. | Cron scheduling |
| Credits | `client.get_credits()` | `getCredits()` | Balance check |
| Feedback | `client.send_feedback()` | `sendFeedback()` | Rating/feedback |
| Schema Gen | `client.generate_schema()` | `generateSchema()` | AI schema creation |

## Development Workflow

### Adding a New Endpoint

**Python SDK:**

1. Add request/response models in `scrapegraph_py/models/new_endpoint.py`
2. Add sync method to `scrapegraph_py/client.py`
3. Add async method to `scrapegraph_py/async_client.py`
4. Export models in `scrapegraph_py/models/__init__.py`
5. Add tests in `tests/test_new_endpoint.py`
6. Update examples in `examples/`
7. Update README.md with usage examples

**JavaScript SDK:**

1. Create `src/newEndpoint.js` with async function
2. Export function in `index.js`
3. Add tests in `test/test_newEndpoint.js`
4. Update examples in `examples/`
5. Update README.md with usage examples

### Testing Strategy

**Python:**
- Unit tests for models (Pydantic validation)
- Integration tests for client methods (mocked HTTP)
- Use `aioresponses` for async client testing
- Use `responses` for sync client testing
- Mock API responses to avoid real API calls in CI
- Run `pytest --cov` for coverage reports

**JavaScript:**
- Integration test files with real/mocked responses
- Manual testing with `.env` file for API keys
- Use try/catch to demonstrate error handling

### Release Process

Both SDKs use **semantic-release** for automated versioning:

1. **Commit with semantic messages:**
   - `feat: add new endpoint` → Minor bump (0.x.0)
   - `fix: handle timeout errors` → Patch bump (0.0.x)
   - `feat!: breaking API change` → Major bump (x.0.0)

2. **Merge to main branch**

3. **GitHub Actions automatically:**
   - Determines version bump
   - Updates version in `pyproject.toml` / `package.json`
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Publishes to PyPI / npm

Configuration files:
- Python: `.releaserc.yml`
- JavaScript: `.releaserc` (in scrapegraph-js/)
- GitHub workflow: `.github/workflows/release-*.yml`

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

### JavaScript SDK

- **Code Style**:
  - Prettier for formatting
  - ESLint for linting
  - JSDoc comments for functions

- **Async Functions**:
  - All API calls return Promises
  - Use async/await pattern
  - Handle errors with try/catch

- **Exports**:
  - Named exports in `index.js`
  - Each function should be independently usable

## Environment Variables

Both SDKs support API key via environment variable:

- **Python**: `SGAI_API_KEY`
- **JavaScript**: `SGAI_APIKEY`

Usage:
```bash
export SGAI_API_KEY="your-api-key-here"
```

Then initialize client without passing API key:
```python
# Python
from scrapegraph_py import Client
client = Client()  # Uses SGAI_API_KEY env var
```

```javascript
// JavaScript
import { smartScraper } from 'scrapegraph-js';
// API key can be passed explicitly or via SGAI_APIKEY env var
```

## Common Patterns

### Python - Using Sync Client

```python
from scrapegraph_py import Client

client = Client(api_key="your-key")

response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract title and description"
)

print(response.result)
```

### Python - Using Async Client

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

### Python - Using Output Schema

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

### JavaScript - Basic Usage

```javascript
import { smartScraper } from 'scrapegraph-js';

(async () => {
  try {
    const response = await smartScraper(
      'your-api-key',
      'https://example.com',
      'Extract the main heading'
    );
    console.log(response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## File Locations Reference

### Python SDK Key Files

- Entry points: `scrapegraph_py/__init__.py`, `scrapegraph_py/client.py`, `scrapegraph_py/async_client.py`
- Models: `scrapegraph_py/models/`
- Config: `pyproject.toml`, `pytest.ini`, `Makefile`
- Tests: `tests/`
- Examples: `examples/`
- Docs: `docs/` (MkDocs)

### JavaScript SDK Key Files

- Entry point: `index.js`
- Endpoints: `src/*.js`
- Utils: `src/utils/`
- Config: `package.json`, `eslint.config.js`, `.prettierrc.json`
- Tests: `test/`
- Examples: `examples/`

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

### JavaScript SDK Debug

Use console logs and error inspection:
```javascript
try {
  const response = await smartScraper(apiKey, url, prompt);
  console.log('Response:', JSON.stringify(response, null, 2));
} catch (error) {
  console.error('Error details:', error);
  console.error('Stack:', error.stack);
}
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
- [JavaScript SDK on npm](https://www.npmjs.com/package/scrapegraph-js/)
- [GitHub Repository](https://github.com/ScrapeGraphAI/scrapegraph-sdk)

## Support

- Email: support@scrapegraphai.com
- GitHub Issues: https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues
- Documentation: https://docs.scrapegraphai.com
