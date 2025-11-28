#!/usr/bin/env python3
"""
Async example demonstrating TOON format integration with ScrapeGraph SDK.

TOON (Token-Oriented Object Notation) reduces token usage by 30-60% compared to JSON,
which can significantly reduce costs when working with LLM APIs.

This example shows how to use the `return_toon` parameter with various async scraping methods.
"""
import asyncio
import os
from scrapegraph_py import AsyncClient


async def main():
    """Demonstrate TOON format with different async scraping methods."""
    
    # Set your API key as an environment variable
    # export SGAI_API_KEY="your-api-key-here"
    # or set it in your .env file
    
    # Initialize the async client
    async with AsyncClient.from_env() as client:
        print("🎨 Async TOON Format Integration Example\n")
        print("=" * 60)
        
        # Example 1: SmartScraper with TOON format
        print("\n📌 Example 1: Async SmartScraper with TOON Format")
        print("-" * 60)
        
        try:
            # Request with return_toon=False (default JSON response)
            json_response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract the page title and main heading",
                return_toon=False
            )
            
            print("\nJSON Response:")
            print(json_response)
            
            # Request with return_toon=True (TOON formatted response)
            toon_response = await client.smartscraper(
                website_url="https://example.com",
                user_prompt="Extract the page title and main heading",
                return_toon=True
            )
            
            print("\nTOON Response:")
            print(toon_response)
            
            # Compare token sizes (approximate)
            if isinstance(json_response, dict):
                import json
                json_str = json.dumps(json_response)
                json_tokens = len(json_str.split())
                toon_tokens = len(str(toon_response).split())
                
                savings = ((json_tokens - toon_tokens) / json_tokens) * 100 if json_tokens > 0 else 0
                
                print(f"\n📊 Token Comparison:")
                print(f"   JSON tokens (approx): {json_tokens}")
                print(f"   TOON tokens (approx): {toon_tokens}")
                print(f"   Savings: {savings:.1f}%")
            
        except Exception as e:
            print(f"Error in Example 1: {e}")
        
        # Example 2: SearchScraper with TOON format
        print("\n\n📌 Example 2: Async SearchScraper with TOON Format")
        print("-" * 60)
        
        try:
            # Request with TOON format
            toon_search_response = await client.searchscraper(
                user_prompt="Latest AI developments in 2024",
                num_results=3,
                return_toon=True
            )
            
            print("\nTOON Search Response:")
            print(toon_search_response)
            
        except Exception as e:
            print(f"Error in Example 2: {e}")
        
        # Example 3: Markdownify with TOON format
        print("\n\n📌 Example 3: Async Markdownify with TOON Format")
        print("-" * 60)
        
        try:
            # Request with TOON format
            toon_markdown_response = await client.markdownify(
                website_url="https://example.com",
                return_toon=True
            )
            
            print("\nTOON Markdown Response:")
            print(str(toon_markdown_response)[:500])  # Print first 500 chars
            print("...(truncated)")
            
        except Exception as e:
            print(f"Error in Example 3: {e}")
        
        print("\n\n✅ Async TOON Integration Examples Completed!")
        print("=" * 60)
        print("\n💡 Benefits of TOON Format:")
        print("   • 30-60% reduction in token usage")
        print("   • Lower LLM API costs")
        print("   • Faster processing")
        print("   • Human-readable format")
        print("\n🔗 Learn more: https://github.com/ScrapeGraphAI/toonify")


if __name__ == "__main__":
    asyncio.run(main())

