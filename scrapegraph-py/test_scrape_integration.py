#!/usr/bin/env python3
"""
Simple integration test for Scrape functionality.
This script tests the basic Scrape operations without requiring a real API key.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "scrapegraph_py"))

from models.scrape import ScrapeRequest, GetScrapeRequest


def test_scrape_models():
    """Test Scrape model validation"""
    print("🧪 Testing Scrape models...")
    
    # Test valid requests
    try:
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        print("✅ Basic Scrape request validation passed")
        
        request_with_headers = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=True,
            headers={"User-Agent": "Test Agent"}
        )
        print("✅ Scrape request with headers validation passed")
        
    except Exception as e:
        print(f"❌ Scrape request validation failed: {e}")
        return False
    
    # Test invalid requests
    try:
        ScrapeRequest(website_url="")
        print("❌ Empty URL should have failed validation")
        return False
    except ValueError:
        print("✅ Empty URL validation correctly failed")
    
    try:
        ScrapeRequest(website_url="invalid-url")
        print("❌ Invalid URL should have failed validation")
        return False
    except ValueError:
        print("✅ Invalid URL validation correctly failed")
    
    # Test GetScrapeRequest
    try:
        get_request = GetScrapeRequest(
            request_id="123e4567-e89b-12d3-a456-426614174000"
        )
        print("✅ Get Scrape request validation passed")
    except Exception as e:
        print(f"❌ Get Scrape request validation failed: {e}")
        return False
    
    try:
        GetScrapeRequest(request_id="invalid-uuid")
        print("❌ Invalid UUID should have failed validation")
        return False
    except ValueError:
        print("✅ Invalid UUID validation correctly failed")
    
    print("✅ All Scrape model tests passed!")
    return True


def test_scrape_model_serialization():
    """Test Scrape model serialization"""
    print("\n🧪 Testing Scrape model serialization...")
    
    try:
        # Test basic serialization
        request = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        data = request.model_dump()
        
        assert "website_url" in data
        assert "render_heavy_js" in data
        assert "headers" not in data  # Should be excluded as None
        print("✅ Basic serialization test passed")
        
        # Test serialization with headers
        request_with_headers = ScrapeRequest(
            website_url="https://example.com",
            render_heavy_js=True,
            headers={"User-Agent": "Test Agent"}
        )
        data_with_headers = request_with_headers.model_dump()
        
        assert data_with_headers["headers"] == {"User-Agent": "Test Agent"}
        print("✅ Serialization with headers test passed")
        
        print("✅ All serialization tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Serialization test failed: {e}")
        return False


def main():
    """Run all Scrape tests"""
    print("🚀 Scrape Integration Tests")
    print("=" * 40)
    
    tests = [
        test_scrape_models,
        test_scrape_model_serialization,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("📊 Test Results")
    print("=" * 20)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
