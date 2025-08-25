#!/usr/bin/env python3
"""
Simple integration test for HTMLfy functionality.
This script tests the basic HTMLfy operations without requiring a real API key.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "scrapegraph_py"))

from models.htmlfy import HtmlfyRequest, GetHtmlfyRequest


def test_htmlfy_models():
    """Test HTMLfy model validation"""
    print("🧪 Testing HTMLfy models...")
    
    # Test valid requests
    try:
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        print("✅ Basic HTMLfy request validation passed")
        
        request_with_headers = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=True,
            headers={"User-Agent": "Test Agent"}
        )
        print("✅ HTMLfy request with headers validation passed")
        
    except Exception as e:
        print(f"❌ HTMLfy request validation failed: {e}")
        return False
    
    # Test invalid requests
    try:
        HtmlfyRequest(website_url="")
        print("❌ Empty URL should have failed validation")
        return False
    except ValueError:
        print("✅ Empty URL validation correctly failed")
    
    try:
        HtmlfyRequest(website_url="invalid-url")
        print("❌ Invalid URL should have failed validation")
        return False
    except ValueError:
        print("✅ Invalid URL validation correctly failed")
    
    # Test GetHtmlfyRequest
    try:
        get_request = GetHtmlfyRequest(
            request_id="123e4567-e89b-12d3-a456-426614174000"
        )
        print("✅ Get HTMLfy request validation passed")
    except Exception as e:
        print(f"❌ Get HTMLfy request validation failed: {e}")
        return False
    
    try:
        GetHtmlfyRequest(request_id="invalid-uuid")
        print("❌ Invalid UUID should have failed validation")
        return False
    except ValueError:
        print("✅ Invalid UUID validation correctly failed")
    
    print("✅ All HTMLfy model tests passed!")
    return True


def test_htmlfy_model_serialization():
    """Test HTMLfy model serialization"""
    print("\n🧪 Testing HTMLfy model serialization...")
    
    try:
        # Test basic serialization
        request = HtmlfyRequest(
            website_url="https://example.com",
            render_heavy_js=False
        )
        data = request.model_dump()
        
        assert "website_url" in data
        assert "render_heavy_js" in data
        assert "headers" not in data  # Should be excluded as None
        print("✅ Basic serialization test passed")
        
        # Test serialization with headers
        request_with_headers = HtmlfyRequest(
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
    """Run all HTMLfy tests"""
    print("🚀 HTMLfy Integration Tests")
    print("=" * 40)
    
    tests = [
        test_htmlfy_models,
        test_htmlfy_model_serialization,
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
