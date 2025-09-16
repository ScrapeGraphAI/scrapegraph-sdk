#!/usr/bin/env python3
"""
Test script to verify render_heavy_js parameter implementation in Python SDK
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapegraph-py'))

from scrapegraph_py.models.smartscraper import SmartScraperRequest
from scrapegraph_py.models.scrape import ScrapeRequest
from scrapegraph_py.models.agenticscraper import AgenticScraperRequest
from scrapegraph_py.models.crawl import CrawlRequest
from scrapegraph_py.models.searchscraper import SearchScraperRequest

def test_smartscraper_render_heavy_js():
    """Test SmartScraperRequest with render_heavy_js parameter"""
    print("Testing SmartScraperRequest with render_heavy_js...")
    
    # Test with render_heavy_js=True
    request = SmartScraperRequest(
        user_prompt="Extract company info",
        website_url="https://example.com",
        render_heavy_js=True
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == True, "render_heavy_js should be True"
    print("✅ SmartScraperRequest with render_heavy_js=True works")
    
    # Test with render_heavy_js=False (default)
    request = SmartScraperRequest(
        user_prompt="Extract company info",
        website_url="https://example.com"
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == False, "render_heavy_js should default to False"
    print("✅ SmartScraperRequest with render_heavy_js=False (default) works")

def test_scrape_render_heavy_js():
    """Test ScrapeRequest with render_heavy_js parameter"""
    print("Testing ScrapeRequest with render_heavy_js...")
    
    # Test with render_heavy_js=True
    request = ScrapeRequest(
        website_url="https://example.com",
        render_heavy_js=True
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == True, "render_heavy_js should be True"
    print("✅ ScrapeRequest with render_heavy_js=True works")
    
    # Test with render_heavy_js=False (default)
    request = ScrapeRequest(
        website_url="https://example.com"
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == False, "render_heavy_js should default to False"
    print("✅ ScrapeRequest with render_heavy_js=False (default) works")

def test_agenticscraper_render_heavy_js():
    """Test AgenticScraperRequest with render_heavy_js parameter"""
    print("Testing AgenticScraperRequest with render_heavy_js...")
    
    # Test with render_heavy_js=True
    request = AgenticScraperRequest(
        url="https://example.com",
        steps=["Click button", "Fill form"],
        render_heavy_js=True
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == True, "render_heavy_js should be True"
    print("✅ AgenticScraperRequest with render_heavy_js=True works")
    
    # Test with render_heavy_js=False (default)
    request = AgenticScraperRequest(
        url="https://example.com",
        steps=["Click button", "Fill form"]
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == False, "render_heavy_js should default to False"
    print("✅ AgenticScraperRequest with render_heavy_js=False (default) works")

def test_crawl_render_heavy_js():
    """Test CrawlRequest with render_heavy_js parameter"""
    print("Testing CrawlRequest with render_heavy_js...")
    
    # Test with render_heavy_js=True
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"},
        render_heavy_js=True
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == True, "render_heavy_js should be True"
    print("✅ CrawlRequest with render_heavy_js=True works")
    
    # Test with render_heavy_js=False (default)
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract data",
        data_schema={"type": "object"}
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == False, "render_heavy_js should default to False"
    print("✅ CrawlRequest with render_heavy_js=False (default) works")

def test_searchscraper_render_heavy_js():
    """Test SearchScraperRequest with render_heavy_js parameter"""
    print("Testing SearchScraperRequest with render_heavy_js...")
    
    # Test with render_heavy_js=True
    request = SearchScraperRequest(
        user_prompt="What is Python?",
        render_heavy_js=True
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == True, "render_heavy_js should be True"
    print("✅ SearchScraperRequest with render_heavy_js=True works")
    
    # Test with render_heavy_js=False (default)
    request = SearchScraperRequest(
        user_prompt="What is Python?"
    )
    
    data = request.model_dump()
    assert data['render_heavy_js'] == False, "render_heavy_js should default to False"
    print("✅ SearchScraperRequest with render_heavy_js=False (default) works")

if __name__ == "__main__":
    print("🧪 Testing render_heavy_js parameter implementation in Python SDK\n")
    
    try:
        test_smartscraper_render_heavy_js()
        test_scrape_render_heavy_js()
        test_agenticscraper_render_heavy_js()
        test_crawl_render_heavy_js()
        test_searchscraper_render_heavy_js()
        
        print("\n🎉 All Python SDK tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

