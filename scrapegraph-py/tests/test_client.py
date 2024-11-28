from uuid import uuid4

import pytest
import responses

from scrapegraph_py.client import SyncClient
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_uuid():
    return str(uuid4())


@responses.activate
def test_smartscraper(mock_api_key):
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

    with SyncClient(api_key=mock_api_key) as client:
        response = client.smartscraper(
            website_url="https://example.com", user_prompt="Describe this page."
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

    with SyncClient(api_key=mock_api_key) as client:
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

    with SyncClient(api_key=mock_api_key) as client:
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

    with SyncClient(api_key=mock_api_key) as client:
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

    with SyncClient(api_key=mock_api_key) as client:
        with pytest.raises(ConnectionError):
            client.smartscraper(
                website_url="https://example.com", user_prompt="Describe this page."
            )
