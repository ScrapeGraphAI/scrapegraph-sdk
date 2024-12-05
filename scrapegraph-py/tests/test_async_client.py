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
async def test_smartscraper(mock_api_key):
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
async def test_localscraper(mock_api_key):
    with aioresponses() as mocked:
        mocked.post(
            "https://api.scrapegraphai.com/v1/localscraper",
            payload={
                "request_id": str(uuid4()),
                "status": "completed",
                "result": {"extracted_info": "Test content"},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.localscraper(
                user_prompt="Extract info",
                website_html="<html><body><p>Test content</p></body></html>",
            )
            assert response["status"] == "completed"
            assert "extracted_info" in response["result"]


@pytest.mark.asyncio
async def test_get_localscraper(mock_api_key, mock_uuid):
    with aioresponses() as mocked:
        mocked.get(
            f"https://api.scrapegraphai.com/v1/localscraper/{mock_uuid}",
            payload={
                "request_id": mock_uuid,
                "status": "completed",
                "result": {"extracted_info": "Test content"},
            },
        )

        async with AsyncClient(api_key=mock_api_key) as client:
            response = await client.get_localscraper(mock_uuid)
            assert response["status"] == "completed"
            assert response["request_id"] == mock_uuid
