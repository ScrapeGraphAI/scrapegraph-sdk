import pytest
from unittest.mock import patch
from scrapegraph_py import SyncClient

def test_smartscraper():
    # Mock response data
    mock_response = {
        "request_id": "test-123",
        "result": {
            "heading": "Example Domain",
            "description": "This is a sample description",
            "summary": "A test webpage summary"
        }
    }

    # Create client instance with dummy API key
    client = SyncClient(api_key="test-api-key")

    # Mock the API call
    with patch.object(client, '_make_request') as mock_request:
        # Configure mock to return our test data
        mock_request.return_value = mock_response

        # Make the smartscraper request
        response = client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract the main heading, description, and summary of the webpage"
        )

        # Verify the request was made with correct parameters
        mock_request.assert_called_once()
        call_args = mock_request.call_args[0][0]
        assert call_args['method'] == 'POST'
        assert 'smartscraper' in call_args['url']
        assert call_args['json']['website_url'] == "https://example.com"
        assert call_args['json']['user_prompt'] == "Extract the main heading, description, and summary of the webpage"

        # Verify response structure and content
        assert isinstance(response, dict)
        assert response['request_id'] == "test-123"
        assert isinstance(response['result'], dict)

    # Clean up
    client.close()
