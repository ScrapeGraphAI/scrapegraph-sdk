#!/usr/bin/env python3
"""
SmartScraper Cookies Example (Async)

This example demonstrates how to use cookies with SmartScraper API using the asynchronous client.
Cookies are passed through the headers parameter as a Cookie header.
"""

import asyncio
import json
import logging
import os
import time
from pydantic import BaseModel, Field
from typing import Dict, Optional
from dotenv import load_dotenv

from scrapegraph_py import AsyncClient
from scrapegraph_py.exceptions import APIError

# Load environment variables from .env file
load_dotenv()


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class CookieInfo(BaseModel):
    """Model representing cookie information."""
    cookies: Dict[str, str] = Field(description="Dictionary of cookie key-value pairs")


class UserProfile(BaseModel):
    """Model representing user profile information."""
    username: str = Field(description="User's username")
    email: Optional[str] = Field(description="User's email address")
    preferences: Optional[Dict[str, str]] = Field(description="User preferences")


async def basic_cookies_example():
    """Example 1: Basic cookies example using httpbin.org/cookies"""
    
    print("=" * 60)
    print("EXAMPLE 1: Basic Cookies Example")
    print("=" * 60)
    
    # Initialize client from environment variable
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        print("Please either:")
        print("  1. Set environment variable: export SGAI_API_KEY='your-api-key-here'")
        print("  2. Create a .env file with: SGAI_API_KEY=your-api-key-here")
        return
    
    try:
        client = AsyncClient(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return
    
    # Configuration
    website_url = "https://httpbin.org/cookies"
    user_prompt = "Extract all cookies info"
    
    # Example cookies - these will be sent to httpbin.org/cookies
    cookies = {"cookies_key": "cookies_value", "test_cookie": "test_value"}
    
    # Convert cookies dict to Cookie header string
    cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    headers = {"Cookie": cookie_header}
    
    print(f"🌐 Website URL: {website_url}")
    print(f"📝 User Prompt: {user_prompt}")
    print(f"🍪 Cookies: {cookies}")
    print("-" * 50)
    
    try:
        # Start timing
        start_time = time.time()
        
        # Perform the scraping with cookies
        result = await client.smartscraper(
            website_url=website_url,
            user_prompt=user_prompt,
            headers=headers,
            output_schema=CookieInfo,
        )
        
        # Calculate duration
        duration = time.time() - start_time
        
        print(f"✅ Request completed in {duration:.2f} seconds")
        print("\nExtracted Cookie Information:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except APIError as e:
        print(f"❌ API Error: {e}")
        print("This could be due to:")
        print("  - Invalid API key")
        print("  - Rate limiting")
        print("  - Server issues")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("This could be due to:")
        print("  - Network connectivity issues")
        print("  - Invalid website URL")
        print("  - Cookie format issues")


async def cookies_with_scrolling_example():
    """Example 2: Cookies with infinite scrolling"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Cookies with Infinite Scrolling")
    print("=" * 60)
    
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        return
    
    try:
        client = AsyncClient(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return
    
    # Configuration
    website_url = "https://httpbin.org/cookies"
    user_prompt = "Extract all cookies and scroll information"
    
    # Example session cookies
    cookies = {"session_id": "abc123", "user_token": "xyz789"}
    
    # Convert cookies dict to Cookie header string
    cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    headers = {"Cookie": cookie_header}
    
    print(f"🌐 Website URL: {website_url}")
    print(f"📝 User Prompt: {user_prompt}")
    print(f"🍪 Cookies: {cookies}")
    print(f"🔄 Number of scrolls: 3")
    print("-" * 50)
    
    try:
        # Start timing
        start_time = time.time()
        
        # Perform the scraping with cookies and infinite scrolling
        result = await client.smartscraper(
            website_url=website_url,
            user_prompt=user_prompt,
            headers=headers,
            number_of_scrolls=3,
            output_schema=CookieInfo,
        )
        
        # Calculate duration
        duration = time.time() - start_time
        
        print(f"✅ Request completed in {duration:.2f} seconds")
        print("\nExtracted Cookie Information with Scrolling:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except APIError as e:
        print(f"❌ API Error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def cookies_with_pagination_example():
    """Example 3: Cookies with pagination"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Cookies with Pagination")
    print("=" * 60)
    
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        return
    
    try:
        client = AsyncClient(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return
    
    # Configuration
    website_url = "https://httpbin.org/cookies"
    user_prompt = "Extract all cookies from multiple pages"
    
    # Example authentication cookies
    cookies = {"auth_token": "secret123", "preferences": "dark_mode"}
    
    # Convert cookies dict to Cookie header string
    cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    headers = {"Cookie": cookie_header}
    
    print(f"🌐 Website URL: {website_url}")
    print(f"📝 User Prompt: {user_prompt}")
    print(f"🍪 Cookies: {cookies}")
    print(f"📄 Total Pages: 3")
    print("-" * 50)
    
    try:
        # Start timing
        start_time = time.time()
        
        # Perform the scraping with cookies and pagination
        result = await client.smartscraper(
            website_url=website_url,
            user_prompt=user_prompt,
            headers=headers,
            total_pages=3,
            output_schema=CookieInfo,
        )
        
        # Calculate duration
        duration = time.time() - start_time
        
        print(f"✅ Request completed in {duration:.2f} seconds")
        print("\nExtracted Cookie Information with Pagination:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except APIError as e:
        print(f"❌ API Error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def ecommerce_cookies_example():
    """Example 4: E-commerce site scraping with authentication cookies"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 4: E-commerce Site Scraping with Authentication")
    print("=" * 60)
    
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        return
    
    try:
        client = AsyncClient(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return
    
    # Example cookies for an e-commerce site
    cookies = {
        "session_id": "abc123def456",
        "user_id": "user789",
        "cart_id": "cart101112",
        "preferences": "dark_mode,usd",
        "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    
    # Convert cookies dict to Cookie header string
    cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    headers = {"Cookie": cookie_header}
    
    # Note: Using a test URL since we can't access real e-commerce sites
    website_url = "https://httpbin.org/cookies"
    user_prompt = "Extract product information including name, price, availability, and rating"
    
    print(f"🌐 Website URL: {website_url}")
    print(f"📝 User Prompt: {user_prompt}")
    print(f"🍪 E-commerce Cookies: {cookies}")
    print(f"🔄 Number of scrolls: 5")
    print("-" * 50)
    
    try:
        # Start timing
        start_time = time.time()
        
        # Perform the scraping with e-commerce cookies
        result = await client.smartscraper(
            website_url=website_url,
            user_prompt=user_prompt,
            headers=headers,
            number_of_scrolls=5,  # Scroll to load more products
            output_schema=CookieInfo,
        )
        
        # Calculate duration
        duration = time.time() - start_time
        
        print(f"✅ Request completed in {duration:.2f} seconds")
        print("\nE-commerce Scraping Results:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except APIError as e:
        print(f"❌ API Error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


async def concurrent_cookies_example():
    """Example 5: Concurrent requests with different cookies"""
    
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Concurrent Requests with Different Cookies")
    print("=" * 60)
    
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        return
    
    try:
        client = AsyncClient(api_key=api_key)
    except Exception as e:
        print(f"❌ Error initializing client: {e}")
        return
    
    # Different cookie sets for different scenarios
    cookie_sets = [
        {
            "name": "Social Media Session",
            "cookies": {"session_token": "xyz789abc123", "user_session": "def456ghi789"}
        },
        {
            "name": "News Site Preferences", 
            "cookies": {"user_preferences": "technology,science,ai", "reading_level": "advanced"}
        },
        {
            "name": "Banking Secure Session",
            "cookies": {"secure_session": "pqr678stu901", "auth_token": "vwx234yz567"}
        }
    ]
    
    async def scrape_with_cookies(cookie_set):
        """Helper function to scrape with specific cookies"""
        cookies = cookie_set["cookies"]
        cookie_header = "; ".join([f"{k}={v}" for k, v in cookies.items()])
        headers = {"Cookie": cookie_header}
        
        try:
            result = await client.smartscraper(
                website_url="https://httpbin.org/cookies",
                user_prompt=f"Extract cookies for {cookie_set['name']}",
                headers=headers,
                output_schema=CookieInfo,
            )
            return {"success": True, "name": cookie_set["name"], "result": result}
        except Exception as e:
            return {"success": False, "name": cookie_set["name"], "error": str(e)}
    
    print("🚀 Starting concurrent requests with different cookies...")
    start_time = time.time()
    
    # Create tasks for concurrent execution
    tasks = [scrape_with_cookies(cookie_set) for cookie_set in cookie_sets]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    duration = time.time() - start_time
    print(f"✅ All concurrent requests completed in {duration:.2f} seconds")
    
    # Display results
    for result in results:
        if isinstance(result, dict):
            if result.get("success"):
                print(f"✅ {result['name']}: Success")
                print(f"   Cookies: {result['result']}")
            else:
                print(f"❌ {result['name']}: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Unexpected result type: {type(result)}")


async def main():
    """Main function to run all cookies examples"""
    
    print("ScrapeGraph SDK - SmartScraper Cookies Examples (Async)")
    print("=" * 70)
    print("This example demonstrates how to use cookies with SmartScraper API")
    print("Cookies are passed through the headers parameter as a Cookie header")
    print("=" * 70)
    
    # Run all examples
    await basic_cookies_example()
    await cookies_with_scrolling_example()
    await cookies_with_pagination_example()
    await ecommerce_cookies_example()
    await concurrent_cookies_example()
    
    print("\n" + "=" * 70)
    print("All cookies examples completed!")
    print("\nKey points:")
    print("1. Cookies are passed via the 'headers' parameter")
    print("2. Cookie format: 'key1=value1; key2=value2'")
    print("3. Cookies work with all SmartScraper features (scrolling, pagination)")
    print("4. Use concurrent requests for better performance")
    print("\nCommon use cases:")
    print("- Authentication for protected pages")
    print("- Session management for dynamic content")
    print("- User preferences and settings")
    print("- Shopping cart and user state")


if __name__ == "__main__":
    asyncio.run(main()) 