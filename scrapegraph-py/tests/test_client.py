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
            schema=schema,
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
            schema=schema,
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
