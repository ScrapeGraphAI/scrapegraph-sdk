# ScrapeGraphAI SDK Documentation

Welcome to the ScrapeGraphAI SDK documentation hub. This directory contains comprehensive documentation for understanding, developing, and maintaining the official Python SDK for the ScrapeGraph AI API.

## 📚 Available Documentation

### System Documentation (`system/`)

#### [Project Architecture](./system/project_architecture.md)
Complete SDK architecture documentation including:
- **Repository Structure** - How the Python SDK is organized
- **Python SDK Architecture** - Client structure, async/sync support, models
- **API Endpoints Coverage** - All supported endpoints
- **Authentication** - API key management and security
- **Testing Strategy** - Unit tests, integration tests, CI/CD
- **Release Process** - Semantic versioning and publishing

### Task Documentation (`tasks/`)

*Future: PRD and implementation plans for specific SDK features*

### SOP Documentation (`sop/`)

*Future: Standard operating procedures (e.g., adding new endpoints, releasing versions)*

---

## 🚀 Quick Start

### For New Contributors

1. **Read First:**
   - [Main README](../README.md) - Project overview and features
   - [Python SDK README](../scrapegraph-py/README.md) - Python SDK guide

2. **Set Up Development Environment:**

   ```bash
   cd scrapegraph-py

   # Install dependencies with uv (recommended)
   pip install uv
   uv sync

   # Or use pip
   pip install -e .

   # Install pre-commit hooks
   pre-commit install
   ```

3. **Run Tests:**

   ```bash
   cd scrapegraph-py
   pytest tests/ -v
   ```

4. **Explore the Codebase:**
   - **Python**: `scrapegraph_py/client.py` - Sync client, `scrapegraph_py/async_client.py` - Async client
   - **Examples**: `scrapegraph-py/examples/`

---

## 🔍 Finding Information

### I want to understand...

**...how to add a new endpoint:**
- Read: Python SDK - `scrapegraph_py/client.py`, `scrapegraph_py/async_client.py`
- Examples: Look at existing endpoint implementations

**...how authentication works:**
- Read: Python SDK - `scrapegraph_py/client.py` (initialization)
- The SDK supports `SGAI_API_KEY` environment variable

**...how error handling works:**
- Read: Python SDK - `scrapegraph_py/exceptions.py`

**...how testing works:**
- Read: Python SDK - `tests/` directory, `pytest.ini`
- Run: Follow test commands in README

**...how releases work:**
- Read: Python SDK - `.releaserc.yml` (semantic-release config)
- GitHub Actions: `.github/workflows/` for automated releases

---

## 🛠️ Development Workflows

### Running Tests

```bash
cd scrapegraph-py

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_smartscraper.py -v

# Run with coverage
pytest --cov=scrapegraph_py --cov-report=html tests/
```

### Code Quality

```bash
cd scrapegraph-py

# Format code
black scrapegraph_py tests

# Sort imports
isort scrapegraph_py tests

# Lint code
ruff check scrapegraph_py tests

# Type check
mypy scrapegraph_py

# Run all checks via Makefile
make format
make lint
```

### Building & Publishing

```bash
cd scrapegraph-py

# Build package
python -m build

# Publish to PyPI (automated via GitHub Actions)
twine upload dist/*
```

---

## 📊 SDK Endpoint Reference

The SDK supports the following endpoints:

| Endpoint | Python SDK | Purpose |
|----------|-----------|---------|
| SmartScraper | ✅ | AI-powered data extraction |
| SearchScraper | ✅ | Multi-website search extraction |
| Markdownify | ✅ | HTML to Markdown conversion |
| SmartCrawler | ✅ | Sitemap generation & crawling |
| AgenticScraper | ✅ | Browser automation |
| Scrape | ✅ | Basic HTML extraction |
| Scheduled Jobs | ✅ | Cron-based job scheduling |
| Credits | ✅ | Credit balance management |
| Feedback | ✅ | Rating and feedback |

---

## 🔧 Key Files Reference

### Python SDK

**Entry Points:**
- `scrapegraph_py/__init__.py` - Package exports
- `scrapegraph_py/client.py` - Synchronous client
- `scrapegraph_py/async_client.py` - Asynchronous client

**Models:**
- `scrapegraph_py/models/` - Pydantic request/response models
  - `smartscraper_models.py` - SmartScraper schemas
  - `searchscraper_models.py` - SearchScraper schemas
  - `crawler_models.py` - Crawler schemas
  - `markdownify_models.py` - Markdownify schemas
  - And more...

**Utilities:**
- `scrapegraph_py/utils/` - Helper functions
- `scrapegraph_py/logger.py` - Logging configuration
- `scrapegraph_py/config.py` - Configuration constants
- `scrapegraph_py/exceptions.py` - Custom exceptions

**Configuration:**
- `pyproject.toml` - Package metadata, dependencies, tool configs
- `pytest.ini` - Pytest configuration
- `Makefile` - Common development tasks
- `.releaserc.yml` - Semantic-release configuration

---

## 🧪 Testing

### Python SDK Test Structure

```
scrapegraph-py/tests/
├── test_async_client.py      # Async client tests
├── test_client.py             # Sync client tests
├── test_smartscraper.py       # SmartScraper endpoint tests
├── test_searchscraper.py      # SearchScraper endpoint tests
├── test_crawler.py            # Crawler endpoint tests
└── conftest.py                # Pytest fixtures
```

### Writing Tests

**Python Example:**
```python
import pytest
from scrapegraph_py import Client

def test_smartscraper_basic():
    client = Client(api_key="test-key")
    response = client.smartscraper(
        website_url="https://example.com",
        user_prompt="Extract title"
    )
    assert response.request_id is not None
```

---

## 🚨 Troubleshooting

### Common Issues

**Issue: Import errors in Python SDK**
- **Cause:** Package not installed or outdated
- **Solution:**
  ```bash
  cd scrapegraph-py
  pip install -e .
  # Or with uv
  uv sync
  ```

**Issue: API key errors**
- **Cause:** Invalid or missing API key
- **Solution:**
  - Set `SGAI_API_KEY` environment variable
  - Or pass `api_key` parameter directly
  - Get API key from https://scrapegraphai.com

**Issue: Type errors in Python SDK**
- **Cause:** Using wrong model types
- **Solution:** Check `scrapegraph_py/models/` for correct Pydantic models

**Issue: Tests failing**
- **Cause:** Missing test environment variables
- **Solution:** Set `SGAI_API_KEY` for integration tests or use mocked tests

---

## 📖 External Documentation

### Official Docs
- [ScrapeGraph AI API Documentation](https://docs.scrapegraphai.com)
- [Python SDK Documentation](https://docs.scrapegraphai.com/sdks/python)

### Package Repositories
- [PyPI - scrapegraph-py](https://pypi.org/project/scrapegraph-py/)

### Development Tools
- [pytest Documentation](https://docs.pytest.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [uv Documentation](https://docs.astral.sh/uv/)

---

## 🤝 Contributing

### Before Making Changes

1. **Read relevant documentation** - Understand the SDK structure
2. **Check existing issues** - Avoid duplicate work
3. **Run tests** - Ensure current state is green
4. **Create a branch** - Use descriptive branch names (e.g., `feat/add-pagination-support`)

### Development Process

1. **Make changes** - Write clean, documented code
2. **Add tests** - Cover new functionality
3. **Run code quality checks** - Format, lint, type check
4. **Run tests** - Ensure all tests pass
5. **Update documentation** - Update README and examples
6. **Commit with semantic commit messages** - `feat:`, `fix:`, `docs:`, etc.
7. **Create pull request** - Describe changes thoroughly

### Code Style

**Python SDK:**
- **Black** - Code formatting (line length: 88)
- **isort** - Import sorting (Black profile)
- **Ruff** - Fast linting
- **mypy** - Type checking (strict mode)
- **Type hints** - Use Pydantic models and type annotations
- **Docstrings** - Document public functions and classes

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add pagination support for smartscraper
fix: handle timeout errors gracefully
docs: update README with new examples
test: add unit tests for crawler endpoint
chore: update dependencies
```

This enables automated semantic versioning and changelog generation.

---

## 📝 Documentation Maintenance

### When to Update Documentation

**Update `.agent/README.md` when:**
- Adding new SDK features
- Changing development workflows
- Updating testing procedures

**Update `README.md` (root) when:**
- Adding new endpoints
- Changing installation instructions
- Adding new features or use cases

**Update SDK-specific READMEs when:**
- Adding new endpoint methods
- Changing API surface
- Adding examples

### Documentation Best Practices

1. **Keep examples working** - Test code examples regularly
2. **Be specific** - Include version numbers, function names
3. **Include error handling** - Show try/catch patterns
4. **Cross-reference** - Link between related sections
5. **Keep changelogs** - Document all changes in CHANGELOG.md

---

## 📅 Release Process

The SDK uses **semantic-release** for automated versioning and publishing:

### Release Workflow

1. **Make changes** - Develop and test new features
2. **Commit with semantic messages** - `feat:`, `fix:`, etc.
3. **Merge to main** - Pull request approved and merged
4. **Automated release** - GitHub Actions:
   - Determines version bump (major/minor/patch)
   - Updates version in `pyproject.toml`
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Publishes to PyPI

### Version Bumping Rules

- `feat:` → **Minor** version bump (0.x.0)
- `fix:` → **Patch** version bump (0.0.x)
- `BREAKING CHANGE:` → **Major** version bump (x.0.0)

---

## 🔗 Quick Links

- [Main README](../README.md) - Project overview
- [Python SDK README](../scrapegraph-py/README.md) - Python guide
- [Cookbook](../cookbook/) - Usage examples
- [API Documentation](https://docs.scrapegraphai.com) - Full API docs

---

## 📧 Support

For questions or issues:
1. Check this documentation first
2. Review SDK-specific README
3. Search existing GitHub issues
4. Create a new issue with:
   - SDK version
   - Error message
   - Minimal reproducible example

---

**Happy Coding! 🚀**
