# Testing Guide for ScrapeGraph Python SDK

This document provides comprehensive information about testing the ScrapeGraph Python SDK.

## Overview

The test suite covers all APIs in the SDK with comprehensive test cases that ensure:
- All API endpoints return 200 status codes
- Both sync and async clients are tested
- Error handling scenarios are covered
- Edge cases and validation are tested

## Test Structure

### Test Files

- `tests/test_comprehensive_apis.py` - Mocked comprehensive test suite covering all APIs
- `tests/test_real_apis.py` - Real API tests using actual API calls with environment variables
- `tests/test_client.py` - Sync client tests
- `tests/test_async_client.py` - Async client tests
- `tests/test_smartscraper.py` - SmartScraper specific tests
- `tests/test_models.py` - Model validation tests
- `tests/test_exceptions.py` - Exception handling tests

### Test Categories

1. **API Tests** - Test all API endpoints with 200 responses
2. **Client Tests** - Test client initialization and context managers
3. **Model Tests** - Test Pydantic model validation
4. **Error Handling** - Test error scenarios and edge cases
5. **Async Tests** - Test async client functionality

## Running Tests

### Prerequisites

Install test dependencies:

```bash
cd scrapegraph-py
pip install -r requirements-test.txt
pip install -e .
```

### Basic Test Execution

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_comprehensive_apis.py

# Run only async tests
python -m pytest -m asyncio

# Run only sync tests
python -m pytest -m "not asyncio"
```

### Using the Test Runner Script

```bash
# Run all tests with coverage
python run_tests.py --coverage

# Run with HTML coverage report
python run_tests.py --coverage --html

# Run with XML coverage report (for CI)
python run_tests.py --coverage --xml

# Run only async tests
python run_tests.py --async-only

# Run specific test file
python run_tests.py --test-file tests/test_smartscraper.py
```

### Using the Real API Test Runner

```bash
# Run real API tests (requires SGAI_API_KEY environment variable)
python run_real_tests.py

# Run with custom API key
python run_real_tests.py --api-key your-api-key-here

# Run with verbose output
python run_real_tests.py --verbose

# Run only async real API tests
python run_real_tests.py --async-only

# Run only sync real API tests
python run_real_tests.py --sync-only
```

### Coverage Reports

```bash
# Generate coverage report
python -m pytest --cov=scrapegraph_py --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html
```

## Test Coverage

### Mocked Tests (test_comprehensive_apis.py)

1. **SmartScraper API**
   - Basic scraping with URL
   - Scraping with HTML content
   - Custom headers
   - Cookies support
   - Output schema validation
   - Infinite scrolling
   - Pagination
   - Status retrieval

2. **SearchScraper API**
   - Basic search functionality
   - Custom number of results
   - Custom headers
   - Output schema validation
   - Status retrieval

3. **Markdownify API**
   - Basic markdown conversion
   - Custom headers
   - Status retrieval

4. **Crawl API**
   - Basic crawling
   - All parameters (depth, max_pages, etc.)
   - Status retrieval

5. **Credits API**
   - Credit balance retrieval

6. **Feedback API**
   - Submit feedback with text
   - Submit feedback without text

### Real API Tests (test_real_apis.py)

The real API tests cover the same functionality as the mocked tests but use actual API calls:

1. **All API Endpoints** - Test with real API responses
2. **Error Handling** - Test with actual error scenarios
3. **Performance** - Test concurrent requests and response times
4. **Environment Variables** - Test client initialization from environment
5. **Context Managers** - Test proper resource management

**Note**: Real API tests require a valid `SGAI_API_KEY` environment variable and may consume API credits.

### Client Features Tested

1. **Sync Client**
   - Initialization from environment
   - Context manager support
   - All API methods

2. **Async Client**
   - Initialization from environment
   - Async context manager support
   - All async API methods

## Mocking Strategy

All tests use the `responses` library to mock HTTP requests:

```python
@responses.activate
def test_api_endpoint():
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/endpoint",
        json={"status": "completed", "result": "data"},
        status=200
    )
    # Test implementation
```

## GitHub Actions Workflow

The `.github/workflows/test.yml` file defines the CI/CD pipeline:

### Jobs

1. **Test Job**
   - Runs on multiple Python versions (3.8-3.12)
   - Executes all tests with coverage
   - Uploads coverage to Codecov

2. **Lint Job**
   - Runs flake8, black, isort, and mypy
   - Ensures code quality and style consistency

3. **Security Job**
   - Runs bandit and safety checks
   - Identifies potential security issues

### Triggers

- Push to main/master branch
- Pull requests to main/master branch

## Test Configuration

### pytest.ini

The `pytest.ini` file configures:
- Test discovery patterns
- Coverage settings
- Custom markers
- Warning filters

### Coverage Settings

- Minimum coverage: 80%
- Reports: term-missing, html, xml
- Coverage source: scrapegraph_py package

## Best Practices

1. **Test Naming**
   - Use descriptive test names
   - Include the expected behavior in the name
   - Use `test_` prefix for all test functions

2. **Test Organization**
   - Group related tests in classes or modules
   - Use fixtures for common setup
   - Keep tests independent

3. **Mocking**
   - Mock external dependencies
   - Use realistic mock data
   - Test both success and error scenarios

4. **Assertions**
   - Test specific behavior, not implementation
   - Use appropriate assertion methods
   - Include meaningful error messages

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -e .
   ```

2. **Missing Dependencies**
   ```bash
   pip install -r requirements-test.txt
   ```

3. **Async Test Failures**
   ```bash
   pip install pytest-asyncio
   ```

4. **Coverage Issues**
   ```bash
   pip install pytest-cov
   ```

### Debug Mode

```bash
# Run tests with debug output
python -m pytest -v -s

# Run specific test with debug
python -m pytest tests/test_comprehensive_apis.py::test_smartscraper_basic_success -v -s
```

## Contributing

When adding new tests:

1. Follow the existing test patterns
2. Ensure 200 status code responses
3. Test both sync and async versions
4. Include error handling scenarios
5. Update this documentation if needed

## Coverage Goals

- **Minimum Coverage**: 80%
- **Target Coverage**: 90%
- **Critical Paths**: 100%

## Performance

- **Test Execution Time**: < 30 seconds
- **Memory Usage**: < 500MB
- **Parallel Execution**: Supported via pytest-xdist

## Security

All tests run in isolated environments with:
- No real API calls
- Mocked external dependencies
- No sensitive data exposure
- Security scanning enabled
