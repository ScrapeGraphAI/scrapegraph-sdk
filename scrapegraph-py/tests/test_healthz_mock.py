"""
Test health check endpoint with mock mode enabled
This ensures the health check works correctly in both mock and real modes
"""

import pytest
from scrapegraph_py.client import Client
from scrapegraph_py.async_client import AsyncClient

# Use a valid mock API key format (sgai- followed by UUID)
MOCK_API_KEY = "sgai-00000000-0000-0000-0000-000000000000"


def test_healthz_mock_sync():
    """Test synchronous health check with mock mode"""
    client = Client(api_key=MOCK_API_KEY, mock=True)
    
    try:
        result = client.healthz()
        
        # Validate response
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "healthy"
        assert "message" in result
        
        print("✓ Sync health check mock test passed")
    finally:
        client.close()


@pytest.mark.asyncio
async def test_healthz_mock_async():
    """Test asynchronous health check with mock mode"""
    async with AsyncClient(api_key=MOCK_API_KEY, mock=True) as client:
        result = await client.healthz()
        
        # Validate response
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "healthy"
        assert "message" in result
        
        print("✓ Async health check mock test passed")


def test_healthz_custom_mock_response_sync():
    """Test synchronous health check with custom mock response"""
    custom_response = {
        "status": "degraded",
        "message": "Custom mock response",
        "uptime": 12345
    }
    
    client = Client(
        api_key=MOCK_API_KEY,
        mock=True,
        mock_responses={"/v1/healthz": custom_response}
    )
    
    try:
        result = client.healthz()
        
        # Validate custom response
        assert result["status"] == "degraded"
        assert result["message"] == "Custom mock response"
        assert result["uptime"] == 12345
        
        print("✓ Sync custom mock response test passed")
    finally:
        client.close()


@pytest.mark.asyncio
async def test_healthz_custom_mock_response_async():
    """Test asynchronous health check with custom mock response"""
    custom_response = {
        "status": "degraded",
        "message": "Custom mock response",
        "uptime": 12345
    }
    
    async with AsyncClient(
        api_key=MOCK_API_KEY,
        mock=True,
        mock_responses={"/v1/healthz": custom_response}
    ) as client:
        result = await client.healthz()
        
        # Validate custom response
        assert result["status"] == "degraded"
        assert result["message"] == "Custom mock response"
        assert result["uptime"] == 12345
        
        print("✓ Async custom mock response test passed")


def test_healthz_from_env_mock():
    """Test health check using from_env with SGAI_MOCK environment variable"""
    import os
    
    # Set mock mode via environment
    os.environ["SGAI_MOCK"] = "true"
    os.environ["SGAI_API_KEY"] = MOCK_API_KEY
    
    try:
        client = Client.from_env()
        result = client.healthz()
        
        # Validate response
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "healthy"
        
        client.close()
        print("✓ from_env mock test passed")
    finally:
        # Clean up environment
        if "SGAI_MOCK" in os.environ:
            del os.environ["SGAI_MOCK"]


if __name__ == "__main__":
    print("Running health check mock tests...")
    print("=" * 60)
    
    test_healthz_mock_sync()
    test_healthz_custom_mock_response_sync()
    test_healthz_from_env_mock()
    
    print("\n" + "=" * 60)
    print("✅ All synchronous tests passed!")
    print("\nRun with pytest for async tests:")
    print("  pytest tests/test_healthz_mock.py")

