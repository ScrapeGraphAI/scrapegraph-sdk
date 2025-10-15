from uuid import uuid4

import pytest
import responses

from scrapegraph_py.client import Client
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


# ============================================================================
# SMARTSCRAPER STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_smartscraper_with_stealth_mode(mock_api_key):
    """Test smartscraper with stealth mode enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"description": "Content extracted with stealth mode."},
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Describe this page.",
            stealth=True,
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_without_stealth_mode(mock_api_key):
    """Test smartscraper with stealth mode disabled (default)"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"description": "Content extracted without stealth."},
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Describe this page.",
            stealth=False,
        )
        assert response["status"] == "completed"


# ============================================================================
# SEARCHSCRAPER STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_searchscraper_with_stealth_mode(mock_api_key):
    """Test searchscraper with stealth mode enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"answer": "Search results with stealth mode."},
            "reference_urls": ["https://example.com"],
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for information", stealth=True
        )
        assert response["status"] == "completed"


@responses.activate
def test_searchscraper_without_stealth_mode(mock_api_key):
    """Test searchscraper with stealth mode disabled (default)"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"answer": "Search results without stealth."},
            "reference_urls": ["https://example.com"],
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search for information", stealth=False
        )
        assert response["status"] == "completed"


# ============================================================================
# MARKDOWNIFY STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_markdownify_with_stealth_mode(mock_api_key):
    """Test markdownify with stealth mode enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": "# Markdown content with stealth mode",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.markdownify(
            website_url="https://example.com", stealth=True
        )
        assert response["status"] == "completed"


@responses.activate
def test_markdownify_without_stealth_mode(mock_api_key):
    """Test markdownify with stealth mode disabled (default)"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": "# Markdown content without stealth",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.markdownify(
            website_url="https://example.com", stealth=False
        )
        assert response["status"] == "completed"


# ============================================================================
# SCRAPE STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_scrape_with_stealth_mode(mock_api_key):
    """Test scrape with stealth mode enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><h1>Content with stealth mode</h1></body></html>",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(website_url="https://example.com", stealth=True)
        assert response["status"] == "completed"
        assert "html" in response


@responses.activate
def test_scrape_without_stealth_mode(mock_api_key):
    """Test scrape with stealth mode disabled (default)"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><h1>Content without stealth</h1></body></html>",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(website_url="https://example.com", stealth=False)
        assert response["status"] == "completed"
        assert "html" in response


@responses.activate
def test_scrape_with_stealth_and_heavy_js(mock_api_key):
    """Test scrape with both stealth mode and heavy JS rendering enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><div>JS rendered with stealth</div></body></html>",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(
            website_url="https://example.com",
            render_heavy_js=True,
            stealth=True,
        )
        assert response["status"] == "completed"
        assert "html" in response


# ============================================================================
# AGENTIC SCRAPER STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_agenticscraper_with_stealth_mode(mock_api_key):
    """Test agentic scraper with stealth mode enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/agentic-scrapper",
        json={
            "request_id": str(uuid4()),
            "status": "processing",
            "message": "Agentic scraping started with stealth mode",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.agenticscraper(
            url="https://example.com",
            steps=["Click on button", "Extract data"],
            use_session=True,
            stealth=True,
        )
        assert response["status"] == "processing"


@responses.activate
def test_agenticscraper_without_stealth_mode(mock_api_key):
    """Test agentic scraper with stealth mode disabled (default)"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/agentic-scrapper",
        json={
            "request_id": str(uuid4()),
            "status": "processing",
            "message": "Agentic scraping started without stealth",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.agenticscraper(
            url="https://example.com",
            steps=["Click on button", "Extract data"],
            use_session=True,
            stealth=False,
        )
        assert response["status"] == "processing"


@responses.activate
def test_agenticscraper_with_stealth_and_ai_extraction(mock_api_key):
    """Test agentic scraper with stealth mode and AI extraction enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/agentic-scrapper",
        json={
            "request_id": str(uuid4()),
            "status": "processing",
            "message": "Agentic scraping with AI extraction and stealth",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.agenticscraper(
            url="https://example.com",
            steps=["Navigate to page", "Extract info"],
            use_session=True,
            user_prompt="Extract user data",
            ai_extraction=True,
            stealth=True,
        )
        assert response["status"] == "processing"


# ============================================================================
# CRAWL STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_crawl_with_stealth_mode(mock_api_key):
    """Test crawl with stealth mode enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": str(uuid4()),
            "status": "processing",
            "message": "Crawl started with stealth mode",
        },
    )

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Test Schema",
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"],
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract data",
            data_schema=schema,
            stealth=True,
        )
        assert response["status"] == "processing"


@responses.activate
def test_crawl_without_stealth_mode(mock_api_key):
    """Test crawl with stealth mode disabled (default)"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": str(uuid4()),
            "status": "processing",
            "message": "Crawl started without stealth",
        },
    )

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Test Schema",
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"],
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract data",
            data_schema=schema,
            stealth=False,
        )
        assert response["status"] == "processing"


@responses.activate
def test_crawl_with_stealth_and_sitemap(mock_api_key):
    """Test crawl with stealth mode and sitemap enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": str(uuid4()),
            "status": "processing",
            "message": "Crawl started with sitemap and stealth",
        },
    )

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Test Schema",
        "type": "object",
        "properties": {"title": {"type": "string"}},
        "required": ["title"],
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract data",
            data_schema=schema,
            sitemap=True,
            stealth=True,
        )
        assert response["status"] == "processing"


# ============================================================================
# COMBINED FEATURES WITH STEALTH MODE TESTS
# ============================================================================


@responses.activate
def test_smartscraper_with_stealth_and_all_features(mock_api_key):
    """Test smartscraper with stealth mode and all additional features"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {
                "products": [
                    {"name": "Product 1", "price": "$10"},
                    {"name": "Product 2", "price": "$20"},
                ]
            },
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com/products",
            user_prompt="Extract products",
            headers=headers,
            number_of_scrolls=5,
            total_pages=2,
            stealth=True,
        )
        assert response["status"] == "completed"
        assert "products" in response["result"]


@responses.activate
def test_searchscraper_with_stealth_and_all_features(mock_api_key):
    """Test searchscraper with stealth mode and all additional features"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"answer": "Complete search results with stealth"},
            "reference_urls": ["https://example1.com", "https://example2.com"],
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="Search query",
            headers=headers,
            num_results=5,
            stealth=True,
        )
        assert response["status"] == "completed"
        assert "answer" in response["result"]
