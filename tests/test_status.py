import pytest
import os
from dotenv import load_dotenv
from scrapegraphaiapisdk.status import status

# Load environment variables from .env file
load_dotenv()

def test_status_successful():
    api_key = os.getenv("SCRAPEGRAPH_API_KEY")
    
    # Mock the response
    with pytest.mock.patch('requests.get') as mock_get:
        mock_get.return_value.text = '{"status": "ok"}'
        mock_get.return_value.raise_for_status.return_value = None
        
        result = status(api_key)
        assert isinstance(result, str)
        assert "ok" in result

def test_status_invalid_api_key():
    api_key = "invalid_key"
    
    with pytest.mock.patch('requests.get') as mock_get:
        mock_get.side_effect = Exception("Invalid API key")
        
        with pytest.raises(Exception):
            status(api_key) 