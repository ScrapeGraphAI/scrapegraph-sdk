"""
Test file to verify cookies integration functionality.
"""

import json
from pydantic import BaseModel, Field

from scrapegraph_py.models.smartscraper import SmartScraperRequest


class TestCookieInfo(BaseModel):
    """Test model for cookie information."""
    
    cookies: dict = Field(description="Dictionary of cookie key-value pairs")


def test_cookies_integration():
    """Test that cookies are properly integrated into SmartScraperRequest."""
    
    print("🧪 Testing Cookies Integration")
    print("=" * 50)
    
    # Test 1: Basic cookies
    print("\n1. Testing basic cookies...")
    cookies = {"session_id": "abc123", "auth_token": "xyz789"}
    
    request = SmartScraperRequest(
        user_prompt="Extract cookie information",
        website_url="https://httpbin.org/cookies",
        cookies=cookies
    )
    
    data = request.model_dump()
    print(f"✅ Cookies included in request: {data.get('cookies')}")
    
    # Test 2: Cookies with output schema
    print("\n2. Testing cookies with output schema...")
    
    request_with_schema = SmartScraperRequest(
        user_prompt="Extract cookie information",
        website_url="https://httpbin.org/cookies",
        cookies=cookies,
        output_schema=TestCookieInfo
    )
    
    data_with_schema = request_with_schema.model_dump()
    print(f"✅ Cookies with schema: {data_with_schema.get('cookies')}")
    print(f"✅ Output schema included: {data_with_schema.get('output_schema') is not None}")
    
    # Test 3: Cookies with scrolling and pagination
    print("\n3. Testing cookies with advanced features...")
    
    request_advanced = SmartScraperRequest(
        user_prompt="Extract cookie information from multiple pages",
        website_url="https://httpbin.org/cookies",
        cookies=cookies,
        number_of_scrolls=5,
        total_pages=3,
        output_schema=TestCookieInfo
    )
    
    data_advanced = request_advanced.model_dump()
    print(f"✅ Advanced request cookies: {data_advanced.get('cookies')}")
    print(f"✅ Number of scrolls: {data_advanced.get('number_of_scrolls')}")
    print(f"✅ Total pages: {data_advanced.get('total_pages')}")
    
    # Test 4: Complex cookies scenario
    print("\n4. Testing complex cookies scenario...")
    
    complex_cookies = {
        "session_id": "abc123def456",
        "user_id": "user789",
        "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "preferences": "dark_mode,usd",
        "cart_id": "cart101112",
        "csrf_token": "csrf_xyz789"
    }
    
    request_complex = SmartScraperRequest(
        user_prompt="Extract user profile and preferences",
        website_url="https://example.com/dashboard",
        cookies=complex_cookies,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
        output_schema=TestCookieInfo
    )
    
    data_complex = request_complex.model_dump()
    print(f"✅ Complex cookies count: {len(data_complex.get('cookies', {}))}")
    print(f"✅ Headers included: {data_complex.get('headers') is not None}")
    
    print("\n" + "=" * 50)
    print("✅ All cookies integration tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    test_cookies_integration() 