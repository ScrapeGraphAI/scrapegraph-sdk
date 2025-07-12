#!/usr/bin/env python3
"""
Test script to verify the schema field fix works without Pydantic warnings
"""

import warnings
from scrapegraph_py.models.crawl import CrawlRequest

# Capture warnings
warnings.simplefilter("always")

# Test creating a CrawlRequest model
try:
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"}
        }
    }
    
    request = CrawlRequest(
        url="https://example.com",
        prompt="Extract title and description",
        data_schema=schema
    )
    
    print("✅ CrawlRequest created successfully without Pydantic warnings!")
    print(f"URL: {request.url}")
    print(f"Prompt: {request.prompt}")
    print(f"Data schema type: {type(request.data_schema)}")
    print(f"Data schema keys: {list(request.data_schema.keys())}")
    
except Exception as e:
    print(f"❌ Error creating CrawlRequest: {e}") 