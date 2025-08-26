from uuid import uuid4

import pytest
import responses
from pydantic import BaseModel

from scrapegraph_py.client import Client
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


@responses.activate
def test_smartscraper_with_url(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"description": "Example domain."},
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com", user_prompt="Describe this page."
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_html(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"description": "Test content."},
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_html="<html><body><p>Test content</p></body></html>",
            user_prompt="Extract info",
        )
        assert response["status"] == "completed"


@responses.activate
def test_smartscraper_with_headers(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"description": "Example domain."},
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Describe this page.",
            headers=headers,
        )
        assert response["status"] == "completed"


@responses.activate
def test_get_smartscraper(mock_api_key, mock_uuid):
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/smartscraper/{mock_uuid}",
        json={
            "request_id": mock_uuid,
            "status": "completed",
            "result": {"data": "test"},
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_smartscraper(mock_uuid)
        assert response["status"] == "completed"
        assert response["request_id"] == mock_uuid


@responses.activate
def test_smartscraper_with_pagination(mock_api_key):
    # Mock the API response for pagination request
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
                    {"name": "Product 3", "price": "$30"},
                ]
            },
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com/products",
            user_prompt="Extract product information",
            total_pages=3,
        )
        assert response["status"] == "completed"
        assert "products" in response["result"]
        assert len(response["result"]["products"]) == 3


@responses.activate
def test_smartscraper_with_pagination_and_scrolls(mock_api_key):
    # Mock the API response for pagination with scrolls
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
                    {"name": "Product 3", "price": "$30"},
                    {"name": "Product 4", "price": "$40"},
                    {"name": "Product 5", "price": "$50"},
                ]
            },
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com/products",
            user_prompt="Extract product information from paginated results",
            total_pages=5,
            number_of_scrolls=10,
        )
        assert response["status"] == "completed"
        assert "products" in response["result"]
        assert len(response["result"]["products"]) == 5


@responses.activate
def test_smartscraper_with_pagination_and_all_features(mock_api_key):
    # Mock the API response for pagination with all features
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {
                "products": [
                    {"name": "Product 1", "price": "$10", "rating": 4.5},
                    {"name": "Product 2", "price": "$20", "rating": 4.0},
                ]
            },
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }

    class ProductSchema(BaseModel):
        name: str
        price: str
        rating: float

    with Client(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com/products",
            user_prompt="Extract product information with ratings",
            headers=headers,
            output_schema=ProductSchema,
            number_of_scrolls=5,
            total_pages=2,
        )
        assert response["status"] == "completed"
        assert "products" in response["result"]


@responses.activate
def test_get_credits(mock_api_key):
    responses.add(
        responses.GET,
        "https://api.scrapegraphai.com/v1/credits",
        json={"remaining_credits": 100, "total_credits_used": 50},
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_credits()
        assert response["remaining_credits"] == 100
        assert response["total_credits_used"] == 50


@responses.activate
def test_submit_feedback(mock_api_key):
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/feedback",
        json={"status": "success"},
    )

    with Client(api_key=mock_api_key) as client:
        response = client.submit_feedback(
            request_id=str(uuid4()), rating=5, feedback_text="Great service!"
        )
        assert response["status"] == "success"


@responses.activate
def test_network_error(mock_api_key):
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/smartscraper",
        body=ConnectionError("Network error"),
    )

    with Client(api_key=mock_api_key) as client:
        with pytest.raises(ConnectionError):
            client.smartscraper(
                website_url="https://example.com", user_prompt="Describe this page."
            )


@responses.activate
def test_markdownify(mock_api_key):
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": "# Example Page\n\nThis is markdown content.",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.markdownify(website_url="https://example.com")
        assert response["status"] == "completed"
        assert "# Example Page" in response["result"]


@responses.activate
def test_markdownify_with_headers(mock_api_key):
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/markdownify",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": "# Example Page\n\nThis is markdown content.",
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }

    with Client(api_key=mock_api_key) as client:
        response = client.markdownify(
            website_url="https://example.com", headers=headers
        )
        assert response["status"] == "completed"
        assert "# Example Page" in response["result"]


@responses.activate
def test_get_markdownify(mock_api_key, mock_uuid):
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/markdownify/{mock_uuid}",
        json={
            "request_id": mock_uuid,
            "status": "completed",
            "result": "# Example Page\n\nThis is markdown content.",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_markdownify(mock_uuid)
        assert response["status"] == "completed"
        assert response["request_id"] == mock_uuid


@responses.activate
def test_searchscraper(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"answer": "Python 3.12 is the latest version."},
            "reference_urls": ["https://www.python.org/downloads/"],
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="What is the latest version of Python?"
        )
        assert response["status"] == "completed"
        assert "answer" in response["result"]
        assert "reference_urls" in response
        assert isinstance(response["reference_urls"], list)


@responses.activate
def test_searchscraper_with_headers(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/searchscraper",
        json={
            "request_id": str(uuid4()),
            "status": "completed",
            "result": {"answer": "Python 3.12 is the latest version."},
            "reference_urls": ["https://www.python.org/downloads/"],
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cookie": "session=123",
    }

    with Client(api_key=mock_api_key) as client:
        response = client.searchscraper(
            user_prompt="What is the latest version of Python?",
            headers=headers,
        )
        assert response["status"] == "completed"
        assert "answer" in response["result"]
        assert "reference_urls" in response
        assert isinstance(response["reference_urls"], list)


@responses.activate
def test_get_searchscraper(mock_api_key, mock_uuid):
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/searchscraper/{mock_uuid}",
        json={
            "request_id": mock_uuid,
            "status": "completed",
            "result": {"answer": "Python 3.12 is the latest version."},
            "reference_urls": ["https://www.python.org/downloads/"],
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_searchscraper(mock_uuid)
        assert response["status"] == "completed"
        assert response["request_id"] == mock_uuid
        assert "answer" in response["result"]
        assert "reference_urls" in response
        assert isinstance(response["reference_urls"], list)


@responses.activate
def test_crawl(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": str(uuid4()),
            "status": "processing",
            "message": "Crawl job started",
        },
    )

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Test Schema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
        "required": ["name"],
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
            cache_website=True,
            depth=2,
            max_pages=5,
            same_domain_only=True,
            batch_size=1,
        )
        assert response["status"] == "processing"
        assert "id" in response


@responses.activate
def test_crawl_with_minimal_params(mock_api_key):
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": str(uuid4()),
            "status": "processing",
            "message": "Crawl job started",
        },
    )

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Test Schema",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": ["name"],
    }

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            prompt="Extract company information",
            data_schema=schema,
        )
        assert response["status"] == "processing"
        assert "id" in response


@responses.activate
def test_get_crawl(mock_api_key, mock_uuid):
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/crawl/{mock_uuid}",
        json={
            "id": mock_uuid,
            "status": "completed",
            "result": {
                "llm_result": {
                    "company": {
                        "name": "Example Corp",
                        "description": "A technology company",
                    },
                    "services": [
                        {
                            "service_name": "Web Development",
                            "description": "Custom web solutions",
                        }
                    ],
                    "legal": {
                        "privacy_policy": "Privacy policy content",
                        "terms_of_service": "Terms of service content",
                    },
                }
            },
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_crawl(mock_uuid)
        assert response["status"] == "completed"
        assert response["id"] == mock_uuid
        assert "result" in response
        assert "llm_result" in response["result"]


@responses.activate
def test_crawl_markdown_mode(mock_api_key):
    """Test crawl in markdown conversion mode (no AI processing)"""
    # Mock the API response
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": str(uuid4()),
            "status": "processing",
            "message": "Markdown crawl job started",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.crawl(
            url="https://example.com",
            extraction_mode=False,  # Markdown conversion mode
            depth=2,
            max_pages=3,
            same_domain_only=True,
            sitemap=True,
        )
        assert response["status"] == "processing"
        assert "id" in response


@responses.activate
def test_crawl_markdown_mode_validation(mock_api_key):
    """Test that markdown mode rejects prompt and data_schema parameters"""
    with Client(api_key=mock_api_key) as client:
        # Should raise validation error when prompt is provided in markdown mode
        try:
            client.crawl(
                url="https://example.com",
                extraction_mode=False,
                prompt="This should not be allowed",
            )
            assert False, "Should have raised validation error"
        except Exception as e:
            assert "Prompt should not be provided when extraction_mode=False" in str(e)

        # Should raise validation error when data_schema is provided in markdown mode
        try:
            client.crawl(
                url="https://example.com",
                extraction_mode=False,
                data_schema={"type": "object"},
            )
            assert False, "Should have raised validation error"
        except Exception as e:
            assert (
                "Data schema should not be provided when extraction_mode=False"
                in str(e)
            )


# ============================================================================
# SCRAPE TESTS
# ============================================================================


@responses.activate
def test_scrape_basic(mock_api_key):
    """Test basic scrape request"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><h1>Example Page</h1><p>This is HTML content.</p></body></html>",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(website_url="https://example.com")
        assert response["status"] == "completed"
        assert "html" in response
        assert "<h1>Example Page</h1>" in response["html"]


@responses.activate
def test_scrape_with_heavy_js(mock_api_key):
    """Test scrape request with heavy JavaScript rendering"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><div id='app'>JavaScript rendered content</div></body></html>",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(
            website_url="https://example.com",
            render_heavy_js=True
        )
        assert response["status"] == "completed"
        assert "html" in response
        assert "JavaScript rendered content" in response["html"]


@responses.activate
def test_scrape_with_headers(mock_api_key):
    """Test scrape request with custom headers"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><p>Content with custom headers</p></body></html>",
        },
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": "session=123"
    }

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(
            website_url="https://example.com",
            headers=headers
        )
        assert response["status"] == "completed"
        assert "html" in response


@responses.activate
def test_scrape_with_all_options(mock_api_key):
    """Test scrape request with all options enabled"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": "<html><body><div>Full featured content</div></body></html>",
        },
    )

    headers = {
        "User-Agent": "Custom Agent",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(
            website_url="https://example.com",
            render_heavy_js=True,
            headers=headers
        )
        assert response["status"] == "completed"
        assert "html" in response


@responses.activate
def test_get_scrape(mock_api_key, mock_uuid):
    """Test get scrape result"""
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/scrape/{mock_uuid}",
        json={
            "scrape_request_id": mock_uuid,
            "status": "completed",
            "html": "<html><body><p>Retrieved HTML content</p></body></html>",
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.get_scrape(mock_uuid)
        assert response["status"] == "completed"
        assert response["scrape_request_id"] == mock_uuid
        assert "html" in response


@responses.activate
def test_scrape_error_response(mock_api_key):
    """Test scrape error response handling"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "error": "Website not accessible",
            "status": "error"
        },
        status=400
    )

    with Client(api_key=mock_api_key) as client:
        with pytest.raises(Exception):
            client.scrape(website_url="https://inaccessible-site.com")


@responses.activate
def test_scrape_processing_status(mock_api_key):
    """Test scrape processing status response"""
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "processing",
            "message": "Scrape job started"
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(website_url="https://example.com")
        assert response["status"] == "processing"
        assert "scrape_request_id" in response


@responses.activate
def test_scrape_complex_html_response(mock_api_key):
    """Test scrape with complex HTML response"""
    complex_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Complex Page</title>
        <style>
            body { font-family: Arial, sans-serif; }
        </style>
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>Welcome</h1>
            <p>This is a complex HTML page with multiple elements.</p>
            <div class="content">
                <img src="image.jpg" alt="Sample image">
                <table>
                    <tr><td>Data 1</td><td>Data 2</td></tr>
                </table>
            </div>
        </main>
        <script>
            console.log('JavaScript loaded');
        </script>
    </body>
    </html>
    """
    
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/scrape",
        json={
            "scrape_request_id": str(uuid4()),
            "status": "completed",
            "html": complex_html,
        },
    )

    with Client(api_key=mock_api_key) as client:
        response = client.scrape(website_url="https://complex-example.com")
        assert response["status"] == "completed"
        assert "html" in response
        assert "<!DOCTYPE html>" in response["html"]
        assert "<title>Complex Page</title>" in response["html"]
        assert "<script>" in response["html"]
        assert "<style>" in response["html"]
