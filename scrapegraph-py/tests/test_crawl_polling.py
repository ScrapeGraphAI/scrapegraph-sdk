"""
Test cases for crawl functionality with polling behavior.

These tests focus on the complete crawl workflow including:
- Starting crawl jobs
- Polling for results with timeout
- Handling success/failure states
- Testing the schema used in crawl_example.py
"""

import json
import time
from unittest.mock import patch
from uuid import uuid4

import pytest
import responses

from scrapegraph_py.client import Client
from tests.utils import generate_mock_api_key


@pytest.fixture
def mock_api_key():
    return generate_mock_api_key()


@pytest.fixture
def mock_crawl_id():
    return str(uuid4())


@pytest.fixture
def founders_schema():
    """Schema used in the crawl_example.py"""
    return {
        "type": "object",
        "properties": {
            "founders": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "title": {"type": "string"},
                        "bio": {"type": "string"},
                        "linkedin": {"type": "string"},
                        "twitter": {"type": "string"},
                    },
                },
            }
        },
    }


@pytest.fixture
def mock_founders_result():
    """Mock result matching the founders schema"""
    return {
        "founders": [
            {
                "name": "Marco Vinci",
                "title": "Co-founder & CEO",
                "bio": "AI researcher and entrepreneur",
                "linkedin": "https://linkedin.com/in/marco-vinci",
                "twitter": "https://twitter.com/marco_vinci",
            },
            {
                "name": "Lorenzo Padoan",
                "title": "Co-founder & CTO",
                "bio": "Software engineer and AI expert",
                "linkedin": "https://linkedin.com/in/lorenzo-padoan",
                "twitter": "https://twitter.com/lorenzo_padoan",
            },
        ]
    }


@responses.activate
def test_crawl_polling_success(
    mock_api_key, mock_crawl_id, founders_schema, mock_founders_result
):
    """Test successful crawl with polling until completion"""

    # Mock the initial crawl request
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": mock_crawl_id,
            "status": "processing",
            "message": "Crawl job started",
        },
        status=200,
    )

    # Mock the polling responses - first few return processing, then success
    for i in range(3):
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
            json={
                "id": mock_crawl_id,
                "status": "processing",
                "message": f"Processing... {i+1}/3",
            },
            status=200,
        )

    # Final successful response
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
        json={
            "id": mock_crawl_id,
            "status": "success",
            "result": {"llm_result": mock_founders_result},
        },
        status=200,
    )

    with Client(api_key=mock_api_key) as client:
        # Start the crawl
        crawl_response = client.crawl(
            url="https://scrapegraphai.com",
            prompt="extract the founders'infos",
            data_schema=founders_schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
        )

        assert crawl_response["status"] == "processing"
        assert crawl_response["id"] == mock_crawl_id

        # Poll for results (simulating the polling logic from crawl_example.py)
        crawl_id = crawl_response.get("id")
        assert crawl_id is not None

        # Simulate polling with a shorter timeout for testing
        for i in range(10):  # Reduced from 60 for faster tests
            result = client.get_crawl(crawl_id)
            if result.get("status") == "success" and result.get("result"):
                # Verify the successful result
                assert result["id"] == mock_crawl_id
                assert result["status"] == "success"
                assert "result" in result
                assert "llm_result" in result["result"]

                # Verify the schema structure
                llm_result = result["result"]["llm_result"]
                assert "founders" in llm_result
                assert isinstance(llm_result["founders"], list)
                assert len(llm_result["founders"]) == 2

                # Verify founder data structure
                for founder in llm_result["founders"]:
                    assert "name" in founder
                    assert "title" in founder
                    assert "bio" in founder
                    assert "linkedin" in founder
                    assert "twitter" in founder

                break
            elif result.get("status") == "failed":
                pytest.fail("Crawl failed unexpectedly")
        else:
            pytest.fail("Polling timeout - crawl did not complete")


@responses.activate
def test_crawl_polling_failure(mock_api_key, mock_crawl_id, founders_schema):
    """Test crawl failure during polling"""

    # Mock the initial crawl request
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": mock_crawl_id,
            "status": "processing",
            "message": "Crawl job started",
        },
        status=200,
    )

    # Mock a few processing responses, then failure
    for i in range(2):
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
            json={
                "id": mock_crawl_id,
                "status": "processing",
                "message": f"Processing... {i+1}/2",
            },
            status=200,
        )

    # Final failure response
    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
        json={
            "id": mock_crawl_id,
            "status": "failed",
            "error": "Website unreachable",
            "message": "Failed to crawl the website",
        },
        status=200,
    )

    with Client(api_key=mock_api_key) as client:
        # Start the crawl
        crawl_response = client.crawl(
            url="https://unreachable-site.com",
            prompt="extract the founders'infos",
            data_schema=founders_schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
        )

        assert crawl_response["status"] == "processing"
        crawl_id = crawl_response.get("id")

        # Poll for results and expect failure
        for i in range(10):
            result = client.get_crawl(crawl_id)
            if result.get("status") == "success" and result.get("result"):
                pytest.fail("Expected failure but got success")
            elif result.get("status") == "failed":
                # Verify failure response
                assert result["id"] == mock_crawl_id
                assert result["status"] == "failed"
                assert "error" in result
                assert result["error"] == "Website unreachable"
                break
        else:
            pytest.fail("Expected failure status but polling timed out")


@responses.activate
def test_crawl_polling_timeout(mock_api_key, mock_crawl_id, founders_schema):
    """Test crawl polling timeout scenario"""

    # Mock the initial crawl request
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": mock_crawl_id,
            "status": "processing",
            "message": "Crawl job started",
        },
        status=200,
    )

    # Mock many processing responses to simulate timeout
    for i in range(20):  # More than our polling limit
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
            json={
                "id": mock_crawl_id,
                "status": "processing",
                "message": f"Still processing... {i+1}/20",
            },
            status=200,
        )

    with Client(api_key=mock_api_key) as client:
        # Start the crawl
        crawl_response = client.crawl(
            url="https://slow-site.com",
            prompt="extract the founders'infos",
            data_schema=founders_schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
        )

        assert crawl_response["status"] == "processing"
        crawl_id = crawl_response.get("id")

        # Poll with a very short limit to test timeout
        max_iterations = 5
        completed = False

        for i in range(max_iterations):
            result = client.get_crawl(crawl_id)
            if result.get("status") == "success" and result.get("result"):
                completed = True
                break
            elif result.get("status") == "failed":
                pytest.fail("Unexpected failure during timeout test")

        # Should not have completed within the short timeout
        assert not completed, "Crawl should not have completed within timeout period"


@responses.activate
def test_crawl_synchronous_response(
    mock_api_key, founders_schema, mock_founders_result
):
    """Test crawl that returns synchronous result (no polling needed)"""

    # Mock a synchronous response (immediate completion)
    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={"status": "success", "result": {"llm_result": mock_founders_result}},
        status=200,
    )

    with Client(api_key=mock_api_key) as client:
        crawl_response = client.crawl(
            url="https://scrapegraphai.com",
            prompt="extract the founders'infos",
            data_schema=founders_schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
        )

        # Should get immediate result without polling
        assert crawl_response["status"] == "success"
        assert "result" in crawl_response
        assert "llm_result" in crawl_response["result"]

        # Verify the schema structure
        llm_result = crawl_response["result"]["llm_result"]
        assert "founders" in llm_result
        assert isinstance(llm_result["founders"], list)
        assert len(llm_result["founders"]) == 2


@responses.activate
def test_crawl_example_exact_parameters(mock_api_key, mock_crawl_id, founders_schema):
    """Test crawl with exact parameters from crawl_example.py"""

    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": mock_crawl_id,
            "status": "processing",
            "message": "Crawl job started",
        },
        status=200,
    )

    with Client(api_key=mock_api_key) as client:
        # Use exact parameters from crawl_example.py
        response = client.crawl(
            url="https://scrapegraphai.com",
            prompt="extract the founders'infos",
            data_schema=founders_schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
            # batch_size is optional and will be excluded if not provided
        )

        assert response["status"] == "processing"
        assert "id" in response

        # Verify that the request was made with correct parameters
        request = responses.calls[0].request
        request_body = json.loads(request.body)

        assert request_body["url"] == "https://scrapegraphai.com"
        assert request_body["prompt"] == "extract the founders'infos"
        assert request_body["data_schema"] == founders_schema
        assert request_body["cache_website"] is True
        assert request_body["depth"] == 2
        assert request_body["max_pages"] == 2
        assert request_body["same_domain_only"] is True
        # batch_size should not be present when not provided
        assert "batch_size" not in request_body


@responses.activate
@patch("time.sleep")  # Mock sleep to speed up test
def test_crawl_polling_with_timing(
    mock_sleep, mock_api_key, mock_crawl_id, founders_schema, mock_founders_result
):
    """Test crawl polling with timing simulation (similar to crawl_example.py)"""

    responses.add(
        responses.POST,
        "https://api.scrapegraphai.com/v1/crawl",
        json={
            "id": mock_crawl_id,
            "status": "processing",
            "message": "Crawl job started",
        },
        status=200,
    )

    # Mock 3 processing responses, then success
    for i in range(3):
        responses.add(
            responses.GET,
            f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
            json={
                "id": mock_crawl_id,
                "status": "processing",
                "message": f"Processing... {i+1}/3",
            },
            status=200,
        )

    responses.add(
        responses.GET,
        f"https://api.scrapegraphai.com/v1/crawl/{mock_crawl_id}",
        json={
            "id": mock_crawl_id,
            "status": "success",
            "result": {"llm_result": mock_founders_result},
        },
        status=200,
    )

    with Client(api_key=mock_api_key) as client:
        crawl_response = client.crawl(
            url="https://scrapegraphai.com",
            prompt="extract the founders'infos",
            data_schema=founders_schema,
            cache_website=True,
            depth=2,
            max_pages=2,
            same_domain_only=True,
        )

        crawl_id = crawl_response.get("id")

        # Simulate the polling loop from crawl_example.py
        for i in range(60):  # Same as in the example
            time.sleep(5)  # This will be mocked out
            result = client.get_crawl(crawl_id)
            if result.get("status") == "success" and result.get("result"):
                # Verify successful completion
                assert result["result"]["llm_result"] == mock_founders_result
                break
            elif result.get("status") == "failed":
                pytest.fail("Crawl failed unexpectedly")
        else:
            pytest.fail("Crawl did not complete within timeout")

        # Verify sleep was called the expected number of times
        assert (
            mock_sleep.call_count == 4
        )  # 3 processing + 1 success = 4 polling iterations
