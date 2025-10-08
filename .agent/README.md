# ScrapeGraphAI SDK Documentation

Welcome to the ScrapeGraphAI SDK documentation hub. This directory contains comprehensive documentation for understanding, developing, and maintaining the official Python and JavaScript SDKs for the ScrapeGraph AI API.

## 📚 Available Documentation

### System Documentation (`system/`)

#### [Project Architecture](./system/project_architecture.md)
Complete SDK architecture documentation including:
- **Monorepo Structure** - How Python and JavaScript SDKs are organized
- **Python SDK Architecture** - Client structure, async/sync support, models
- **JavaScript SDK Architecture** - Function-based API, async design
- **API Endpoints Coverage** - All supported endpoints across SDKs
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
   - [JavaScript SDK README](../scrapegraph-js/README.md) - JavaScript SDK guide

2. **Choose Your SDK:**

   **Python SDK:**
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

   **JavaScript SDK:**
   ```bash
   cd scrapegraph-js

   # Install dependencies
   npm install

   # Run tests
   npm test
   ```

3. **Run Tests:**

   **Python:**
   ```bash
   cd scrapegraph-py
   pytest tests/ -v
   ```

   **JavaScript:**
   ```bash
   cd scrapegraph-js
   npm test
   ```

4. **Explore the Codebase:**
   - **Python**: `scrapegraph_py/client.py` - Sync client, `scrapegraph_py/async_client.py` - Async client
   - **JavaScript**: `src/` directory - Individual endpoint modules
   - **Examples**: `scrapegraph-py/examples/` and `scrapegraph-js/examples/`

---

## 🔍 Finding Information

### I want to understand...

**...how to add a new endpoint:**
- Read: Python SDK - `scrapegraph_py/client.py`, `scrapegraph_py/async_client.py`
- Read: JavaScript SDK - Create new file in `src/`
- Examples: Look at existing endpoint implementations

**...how authentication works:**
- Read: Python SDK - `scrapegraph_py/client.py` (initialization)
- Read: JavaScript SDK - Each function accepts `apiKey` parameter
- Both SDKs support `SGAI_API_KEY` environment variable

**...how error handling works:**
- Read: Python SDK - `scrapegraph_py/exceptions.py`
- Read: JavaScript SDK - Try/catch blocks in each endpoint

**...how testing works:**
- Read: Python SDK - `tests/` directory, `pytest.ini`
- Read: JavaScript SDK - `test/` directory
- Run: Follow test commands in README

**...how releases work:**
- Read: Python SDK - `.releaserc.yml` (semantic-release config)
- Read: JavaScript SDK - `.releaserc` (semantic-release config)
- GitHub Actions: `.github/workflows/` for automated releases

---

## 🛠️ Development Workflows

### Running Tests

**Python SDK:**
```bash
cd scrapegraph-py

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_smartscraper.py -v

# Run with coverage
pytest --cov=scrapegraph_py --cov-report=html tests/
```

**JavaScript SDK:**
```bash
cd scrapegraph-js

# Run all tests
npm test

# Run specific test
node test/test_smartscraper.js
```

### Code Quality

**Python SDK:**
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

**JavaScript SDK:**
```bash
cd scrapegraph-js

# Format code
npm run format

# Lint code
npm run lint
```

### Building & Publishing

**Python SDK:**
```bash
cd scrapegraph-py

# Build package
python -m build

# Publish to PyPI (automated via GitHub Actions)
twine upload dist/*
```

**JavaScript SDK:**
```bash
cd scrapegraph-js

# Build package (if needed)
npm run build

# Publish to npm (automated via GitHub Actions)
npm publish
```

---

## 📊 SDK Endpoint Reference

Both SDKs support the following endpoints:

| Endpoint | Python SDK | JavaScript SDK | Purpose |
|----------|-----------|----------------|---------|
| SmartScraper | ✅ | ✅ | AI-powered data extraction |
| SearchScraper | ✅ | ✅ | Multi-website search extraction |
| Markdownify | ✅ | ✅ | HTML to Markdown conversion |
| SmartCrawler | ✅ | ✅ | Sitemap generation & crawling |
| AgenticScraper | ✅ | ✅ | Browser automation |
| Scrape | ✅ | ✅ | Basic HTML extraction |
| Scheduled Jobs | ✅ | ✅ | Cron-based job scheduling |
| Credits | ✅ | ✅ | Credit balance management |
| Feedback | ✅ | ✅ | Rating and feedback |

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

### JavaScript SDK

**Entry Points:**
- `index.js` - Main package entry
- `src/` - Individual endpoint modules
  - `smartScraper.js`
  - `searchScraper.js`
  - `crawl.js`
  - `markdownify.js`
  - `agenticScraper.js`
  - `scrape.js`
  - `scheduledJobs.js`
  - `credits.js`
  - `feedback.js`
  - `schema.js`

**Utilities:**
- `src/utils/` - Helper functions

**Configuration:**
- `package.json` - Package metadata and scripts
- `eslint.config.js` - ESLint configuration
- `.prettierrc.json` - Prettier configuration

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

### JavaScript SDK Test Structure

```
scrapegraph-js/test/
├── test_smartscraper.js
├── test_searchscraper.js
├── test_crawl.js
└── test_*.js
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

**JavaScript Example:**
```javascript
import { smartScraper } from 'scrapegraph-js';

(async () => {
  try {
    const response = await smartScraper(
      'test-key',
      'https://example.com',
      'Extract title'
    );
    console.log('Success:', response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
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

**Issue: Module not found in JavaScript SDK**
- **Cause:** Dependencies not installed
- **Solution:**
  ```bash
  cd scrapegraph-js
  npm install
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
- [JavaScript SDK Documentation](https://docs.scrapegraphai.com/sdks/javascript)

### Package Repositories
- [PyPI - scrapegraph-py](https://pypi.org/project/scrapegraph-py/)
- [npm - scrapegraph-js](https://www.npmjs.com/package/scrapegraph-js)

### Development Tools
- [pytest Documentation](https://docs.pytest.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [ESLint Documentation](https://eslint.org/docs/latest/)
- [Prettier Documentation](https://prettier.io/docs/en/)

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

**JavaScript SDK:**
- **Prettier** - Code formatting
- **ESLint** - Linting
- **JSDoc** - Function documentation
- **Async/await** - Use promises for all async operations

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

Both SDKs use **semantic-release** for automated versioning and publishing:

### Release Workflow

1. **Make changes** - Develop and test new features
2. **Commit with semantic messages** - `feat:`, `fix:`, etc.
3. **Merge to main** - Pull request approved and merged
4. **Automated release** - GitHub Actions:
   - Determines version bump (major/minor/patch)
   - Updates version in `package.json` / `pyproject.toml`
   - Generates CHANGELOG.md
   - Creates GitHub release
   - Publishes to npm / PyPI

### Version Bumping Rules

- `feat:` → **Minor** version bump (0.x.0)
- `fix:` → **Patch** version bump (0.0.x)
- `BREAKING CHANGE:` → **Major** version bump (x.0.0)

---

## 🔗 Quick Links

- [Main README](../README.md) - Project overview
- [Python SDK README](../scrapegraph-py/README.md) - Python guide
- [JavaScript SDK README](../scrapegraph-js/README.md) - JavaScript guide
- [Cookbook](../cookbook/) - Usage examples
- [API Documentation](https://docs.scrapegraphai.com) - Full API docs

---

## 📧 Support

For questions or issues:
1. Check this documentation first
2. Review SDK-specific READMEs
3. Search existing GitHub issues
4. Create a new issue with:
   - SDK version
   - Error message
   - Minimal reproducible example

---

**Happy Coding! 🚀**
