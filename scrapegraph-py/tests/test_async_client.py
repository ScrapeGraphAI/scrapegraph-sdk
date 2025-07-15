from uuid import uuid4

import pytest
from aioresponses import aioresponses

from scrapegraph_py.async_client import AsyncClient
from scrapegraph_py.exceptions import APIError
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


@pytest.mark.asyncio
async def test_smartscraper_with_url(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"description": "Example domain."},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_url="https://example.com", user_prompt="Describe this page."
            )
            assert response["status"] == "completed"
            assert "description" in response["result"]


@pytest.mark.asyncio
async def test_smartscraper_with_html(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"description": "Test content."},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_html="<html><body><p>Test content</p></body></html>",
                user_prompt="Extract info",
            )
            assert response["status"] == "completed"
            assert "description" in response["result"]


@pytest.mark.asyncio
async def test_smartscraper_with_headers(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"description": "Example domain."},
            },
        )

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": "session=123",
        }

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Describe this page.",
                headers=headers,
            )
            assert response["status"] == "completed"
            assert "description" in response["result"]


@pytest.mark.asyncio
async def test_get_credits(mock_api_key):
    with aioresponses() as mocked:
        mocked.get(
            "https://api.scrapegraphai.com/v1/credits",
            payload={"remaining_credits": 100, "total_credits_used": 50},
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_credits()
            assert response["remaining_credits"] == 100
            assert response["total_credits_used"] == 50


@pytest.mark.asyncio
async def test_submit_feedback(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/feedback", payload={"status": "success"}
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.submit_feedback(
                request_id=str(uuid4()), rating=5, feedback_text="Great service!"
            )
            assert response["status"] == "success"


@pytest.mark.asyncio
async def test_get_smartscraper(mock_api_key, mock_uuid):
    with aioresponses() as mocked:
        mocked.get(
            f"https://api.scrapegraphai.com/v1/smartscraper/{mock_uuid}",
            payload={
                "request_id": mock_uuid,
                "status": "completed",
                "result": {"data": "test"},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_smartscraper(mock_uuid)
            assert response["status"] == "completed"
            assert response["request_id"] == mock_uuid


@pytest.mark.asyncio
async def test_api_error(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            status=400,
            payload={"error": "Bad request"},
            exception=APIError("Bad request", status_code=400),
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            with pytest.raises(APIError) as exc_info:
                await client.smartscraper(
                    website_url="https://example.com", user_prompt="Describe this page."
                )
            assert exc_info.value.status_code == 400
            assert "Bad request" in str(exc_info.value)


@pytest.mark.asyncio
async def test_markdownify(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Example Page\n\nThis is markdown content.",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.markdownify(website_url="https://example.com")
            assert response["status"] == "completed"
            assert "# Example Page" in response["result"]


@pytest.mark.asyncio
async def test_markdownify_with_headers(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Example Page\n\nThis is markdown content.",
            },
        )

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": "session=123",
        }

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.markdownify(
                website_url="https://example.com", headers=headers
            )
            assert response["status"] == "completed"
            assert "# Example Page" in response["result"]


@pytest.mark.asyncio
async def test_get_markdownify(mock_api_key, mock_uuid):
    with aioresponses() as mocked:
        mocked.get(
            f"https://api.scrapegraphai.com/v1/markdownify/{mock_uuid}",
            payload={
                "request_id": mock_uuid,
                "status": "completed",
                "result": "# Example Page\n\nThis is markdown content.",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_markdownify(mock_uuid)
            assert response["status"] == "completed"
            assert response["request_id"] == mock_uuid


@pytest.mark.asyncio
async def test_searchscraper(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/searchscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"answer": "Python 3.12 is the latest version."},
                "reference_urls": ["https://www.python.org/downloads/"],
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.searchscraper(
                user_prompt="What is the latest version of Python?"
            )
            assert response["status"] == "completed"
            assert "answer" in response["result"]
            assert "reference_urls" in response
            assert isinstance(response["reference_urls"], list)


@pytest.mark.asyncio
async def test_searchscraper_with_headers(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/searchscraper",
            payload={
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

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.searchscraper(
                user_prompt="What is the latest version of Python?",
                headers=headers,
            )
            assert response["status"] == "completed"
            assert "answer" in response["result"]
            assert "reference_urls" in response
            assert isinstance(response["reference_urls"], list)


@pytest.mark.asyncio
async def test_get_searchscraper(mock_api_key, mock_uuid):
    with aioresponses() as mocked:
        mocked.get(
            f"https://api.scrapegraphai.com/v1/searchscraper/{mock_uuid}",
            payload={
                "request_id": mock_uuid,
                "status": "completed",
                "result": {"answer": "Python 3.12 is the latest version."},
                "reference_urls": ["https://www.python.org/downloads/"],
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_searchscraper(mock_uuid)
            assert response["status"] == "completed"
            assert response["request_id"] == mock_uuid
            assert "answer" in response["result"]
            assert "reference_urls" in response
            assert isinstance(response["reference_urls"], list)


@pytest.mark.asyncio
async def test_crawl(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/crawl",
            payload={
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

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.crawl(
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


@pytest.mark.asyncio
async def test_crawl_with_minimal_params(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/crawl",
            payload={
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

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.crawl(
                url="https://example.com",
                prompt="Extract company information",
                schema=schema,
            )
            assert response["status"] == "processing"
            assert "id" in response


@pytest.mark.asyncio
async def test_get_crawl(mock_api_key, mock_uuid):
    with aioresponses() as mocked:
        mocked.get(
            f"https://api.scrapegraphai.com/v1/crawl/{mock_uuid}",
            payload={
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

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_crawl(mock_uuid)
            assert response["status"] == "completed"
            assert response["id"] == mock_uuid
            assert "result" in response
            assert "llm_result" in response["result"]


@pytest.mark.asyncio
async def test_smartscraper_with_steps(mock_api_key):
    """Test async SmartScraper with interactive steps."""
    
    steps = [
        "click on search bar",
        "wait for 500ms",
        "fill email input box with user@example.com",
        "wait a sec",
        "click on the first result"
    ]
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"profile": "User profile extracted after navigation."},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract user profile",
                steps=steps
            )
            assert response["status"] == "completed"
            assert "profile" in response["result"]

        # Verify the request was made with steps
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" in request_info
        assert request_info["steps"] == steps


@pytest.mark.asyncio
async def test_smartscraper_with_steps_and_scrolls(mock_api_key):
    """Test async SmartScraper with both steps and number_of_scrolls."""
    
    steps = [
        "click on load more button",
        "wait for 2 seconds",
        "scroll to bottom"
    ]
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"data": "Combined steps and scrolls result."},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract data with navigation",
                steps=steps,
                number_of_scrolls=3
            )
            assert response["status"] == "completed"
            assert "data" in response["result"]

        # Verify the request was made with both steps and scrolls
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" in request_info
        assert "number_of_scrolls" in request_info
        assert request_info["steps"] == steps
        assert request_info["number_of_scrolls"] == 3


@pytest.mark.asyncio
async def test_smartscraper_without_steps(mock_api_key):
    """Test async SmartScraper without steps (should work as before)."""
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"description": "Normal scraping result."},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract info"
            )
            assert response["status"] == "completed"
            assert "description" in response["result"]

        # Verify the request was made without steps
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" not in request_info


@pytest.mark.asyncio
async def test_markdownify_with_steps(mock_api_key):
    """Test async Markdownify with interactive steps."""
    
    steps = [
        "click on accept cookies",
        "wait for 1 second",
        "click on main content",
        "scroll to article"
    ]
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Article Title\n\nThis is the article content after navigation.",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.markdownify(
                website_url="https://example.com/article",
                steps=steps
            )
            assert response["status"] == "completed"
            assert "Article Title" in response["result"]
            assert "article content" in response["result"]

        # Verify the request was made with steps
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" in request_info
        assert request_info["steps"] == steps


@pytest.mark.asyncio
async def test_markdownify_with_steps_and_headers(mock_api_key):
    """Test async Markdownify with both steps and headers."""
    
    steps = [
        "click on expand content",
        "wait for 500ms",
        "scroll to full article"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml"
    }
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Full Article\n\nExpanded content after navigation.",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.markdownify(
                website_url="https://example.com/article",
                headers=headers,
                steps=steps
            )
            assert response["status"] == "completed"
            assert "Full Article" in response["result"]
            assert "Expanded content" in response["result"]

        # Verify the request was made with both steps and headers
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" in request_info
        assert "headers" in request_info
        assert request_info["steps"] == steps
        assert request_info["headers"] == headers


@pytest.mark.asyncio
async def test_markdownify_without_steps(mock_api_key):
    """Test async Markdownify without steps (should work as before)."""
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Page Title\n\nNormal markdown content.",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.markdownify(
                website_url="https://example.com"
            )
            assert response["status"] == "completed"
            assert "Page Title" in response["result"]

        # Verify the request was made without steps
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" not in request_info


@pytest.mark.asyncio
async def test_smartscraper_empty_steps_list(mock_api_key):
    """Test async SmartScraper with empty steps list."""
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"description": "Result with empty steps."},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract info",
                steps=[]
            )
            assert response["status"] == "completed"
            assert "description" in response["result"]

        # Verify the request was made with empty steps
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" in request_info
        assert request_info["steps"] == []


@pytest.mark.asyncio
async def test_markdownify_empty_steps_list(mock_api_key):
    """Test async Markdownify with empty steps list."""
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Page Title\n\nContent with empty steps.",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.markdownify(
                website_url="https://example.com",
                steps=[]
            )
            assert response["status"] == "completed"
            assert "Page Title" in response["result"]

        # Verify the request was made with empty steps
        assert len(mocked.requests) == 1
        request_info = mocked.requests[0][1]
        assert "steps" in request_info
        assert request_info["steps"] == []


@pytest.mark.asyncio
async def test_concurrent_requests_with_steps(mock_api_key):
    """Test concurrent async requests with different steps."""
    
    steps1 = ["click on search", "wait for 1 second", "click first result"]
    steps2 = ["click on menu", "wait for 500ms", "click about"]
    
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/smartscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"data": "Result 1"},
            },
        )
        mocked.post(
            "https://api.scrapegraphai.com/v1/markdownify",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": "# Result 2\n\nContent",
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            # Execute concurrent requests
            import asyncio
            results = await asyncio.gather(
                client.smartscraper(
                    website_url="https://example.com",
                    user_prompt="Extract data",
                    steps=steps1
                ),
                client.markdownify(
                    website_url="https://example.com",
                    steps=steps2
                ),
                return_exceptions=True
            )
            
            # Verify both requests completed successfully
            assert len(results) == 2
            assert results[0]["status"] == "completed"
            assert results[1]["status"] == "completed"
            assert "data" in results[0]["result"]
            assert "Result 2" in results[1]["result"]

        # Verify both requests were made with their respective steps
        assert len(mocked.requests) == 2
        request1_info = mocked.requests[0][1]
        request2_info = mocked.requests[1][1]
        
        assert "steps" in request1_info
        assert "steps" in request2_info
        assert request1_info["steps"] == steps1
        assert request2_info["steps"] == steps2
