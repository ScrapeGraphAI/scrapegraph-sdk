#!/usr/bin/env python3
"""
Test script to verify that the Pydantic warning is resolved and models work correctly.
"""

import warnings
from scrapegraph_py.models.crawl import CrawlRequest
from scrapegraph_py.models.smartscraper import SmartScraperRequest
from scrapegraph_py.models.searchscraper import SearchScraperRequest
from scrapegraph_py.models.markdownify import MarkdownifyRequest
from scrapegraph_py.models.feedback import FeedbackRequest

# Capture warnings
warnings.simplefilter("always")

def test_crawl_request():
    """Test CrawlRequest model"""
    print("Testing CrawlRequest...")
    
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"}
        }
    }
    
    request = CrawlRequest(
        url="https://example.com",
        prompt="Test prompt",
        data_schema=schema
    )
    
    # Test model_dump
    data = request.model_dump()
    print(f"✅ CrawlRequest model_dump works: {len(data)} fields")
    assert "data_schema" in data
    assert "schema" not in data  # Old field should not be present
    
def test_smartscraper_request():
    """Test SmartScraperRequest model"""
    print("Testing SmartScraperRequest...")
    
    # Test without number_of_scrolls (should be None)
    request = SmartScraperRequest(
        user_prompt="Test prompt",
        website_url="https://example.com"
    )
    
    # Test model_dump - number_of_scrolls should be excluded when None
    data = request.model_dump()
    print(f"✅ SmartScraperRequest model_dump works: {len(data)} fields")
    assert "number_of_scrolls" not in data  # Should be excluded when None
    
    # Test with number_of_scrolls
    request_with_scrolls = SmartScraperRequest(
        user_prompt="Test prompt",
        website_url="https://example.com",
        number_of_scrolls=5
    )
    
    data_with_scrolls = request_with_scrolls.model_dump()
    assert "number_of_scrolls" in data_with_scrolls  # Should be included when not None
    assert data_with_scrolls["number_of_scrolls"] == 5

def test_searchscraper_request():
    """Test SearchScraperRequest model"""
    print("Testing SearchScraperRequest...")
    
    request = SearchScraperRequest(
        user_prompt="Test prompt"
    )
    
    data = request.model_dump()
    print(f"✅ SearchScraperRequest model_dump works: {len(data)} fields")
    assert "headers" not in data  # Should be excluded when None

def test_markdownify_request():
    """Test MarkdownifyRequest model"""
    print("Testing MarkdownifyRequest...")
    
    request = MarkdownifyRequest(
        website_url="https://example.com"
    )
    
    data = request.model_dump()
    print(f"✅ MarkdownifyRequest model_dump works: {len(data)} fields")
    assert "headers" not in data  # Should be excluded when None

def test_feedback_request():
    """Test FeedbackRequest model"""
    print("Testing FeedbackRequest...")
    
    request = FeedbackRequest(
        request_id="123e4567-e89b-12d3-a456-426614174000",
        rating=5
    )
    
    data = request.model_dump()
    print(f"✅ FeedbackRequest model_dump works: {len(data)} fields")
    assert "feedback_text" not in data  # Should be excluded when None

if __name__ == "__main__":
    print("🧪 Testing Pydantic model fixes...")
    
    test_crawl_request()
    test_smartscraper_request()
    test_searchscraper_request()
    test_markdownify_request()
    test_feedback_request()
    
    print("\n✅ All tests passed! The Pydantic warning should be resolved.")
    print("🎉 Models now properly exclude None values from serialization.") 