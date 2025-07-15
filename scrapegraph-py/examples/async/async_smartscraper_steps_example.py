"""
Async example demonstrating how to use the Smart Scraper API with interactive steps.
This example shows how to:
1. Set up interactive steps for website navigation asynchronously
2. Use the AsyncClient with custom steps
3. Handle concurrent requests with different step configurations
4. Display comprehensive results with timing

Interactive steps allow you to:
- Click on elements
- Fill input fields
- Wait for page loads
- Navigate through multiple pages
- Perform complex user interactions

Requirements:
- Python 3.7+
- scrapegraph-py
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

import asyncio
import json
import os
import time
from dotenv import load_dotenv
from scrapegraph_py import AsyncClient

# Load environment variables from .env file
load_dotenv()


async def async_smartscraper_with_steps():
    """
    Enhanced async Smart Scraper function with interactive steps.
    This demonstrates how to use interactive movements to navigate websites asynchronously.
    """
    
    # Get API key from environment
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key must be provided or set in .env file as SGAI_API_KEY. "
            "Create a .env file with: SGAI_API_KEY=your_api_key_here"
        )

    # Interactive steps for website navigation
    steps = [
        "click on search bar",
        "wait for 500ms",
        "fill email input box with mdehsan873@gmail.com",
        "wait a sec",
        "click on the first result of search",
        "wait for 2 seconds to load the result of search",
    ]

    # Target website configuration
    website_url = "https://github.com/"
    user_prompt = "Extract user profile information"

    print("🚀 Starting Async Smart Scraper with Interactive Steps...")
    print(f"🌐 Website URL: {website_url}")
    print(f"🎯 User Prompt: {user_prompt}")
    print(f"📋 Interactive Steps: {len(steps)} steps configured")
    print("\n" + "=" * 60)

    # Display interactive steps
    print("🎯 Interactive Steps to Execute:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print("\n" + "=" * 60)

    # Start timer
    start_time = time.time()
    print(f"⏱️  Timer started at: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    print("🔄 Processing async request with interactive steps...")

    try:
        # Initialize async client
        async with AsyncClient.from_env() as client:
            # Make request with interactive steps
            response = await client.smartscraper(
                user_prompt=user_prompt,
                website_url=website_url,
                steps=steps
            )

            # Calculate execution time
            end_time = time.time()
            execution_time = end_time - start_time
            execution_minutes = execution_time / 60

            print(f"⏱️  Timer stopped at: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
            print(f"⚡ Total execution time: {execution_time:.2f} seconds ({execution_minutes:.2f} minutes)")
            print(f"📊 Performance: {execution_time:.1f}s ({execution_minutes:.1f}m) for {len(steps)} interactive steps")

            # Display results
            print("✅ Request completed successfully!")
            print(f"📊 Request ID: {response.get('request_id', 'N/A')}")
            print(f"🔄 Status: {response.get('status', 'N/A')}")

            if response.get("error"):
                print(f"❌ Error: {response['error']}")
            else:
                print("\n📋 EXTRACTED DATA:")
                print("=" * 60)
                
                # Pretty print the result
                if "result" in response:
                    result_data = response["result"]
                    print(json.dumps(result_data, indent=2, ensure_ascii=False))
                    
                    # Display extraction statistics
                    print("\n📊 EXTRACTION STATISTICS:")
                    print("-" * 50)
                    result_str = json.dumps(result_data)
                    print(f"📝 Data size: {len(result_str)} characters")
                    print(f"🔗 JSON keys: {len(result_data) if isinstance(result_data, dict) else 'N/A'}")
                    print(f"⚡ Processing speed: {len(result_str)/execution_time:.0f} chars/second")
                    print(f"🎯 Steps efficiency: {execution_time/len(steps):.2f}s per step")
                else:
                    print("No result data found")

    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        execution_minutes = execution_time / 60
        
        print(f"⏱️  Timer stopped at: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"⚡ Execution time before error: {execution_time:.2f} seconds ({execution_minutes:.2f} minutes)")
        print(f"💥 Error occurred: {str(e)}")


async def async_smartscraper_concurrent_steps():
    """
    Demonstrate concurrent Smart Scraper requests with different step configurations.
    """
    print("\n🎯 CONCURRENT REQUESTS WITH DIFFERENT STEPS")
    print("=" * 60)
    
    # Configuration for concurrent requests
    configs = [
        {
            "name": "GitHub Search",
            "url": "https://github.com/",
            "prompt": "Extract repository information",
            "steps": [
                "click on search bar",
                "wait for 300ms",
                "fill search with 'python'",
                "wait for 1 second",
                "click first result"
            ]
        },
        {
            "name": "Profile Navigation",
            "url": "https://github.com/",
            "prompt": "Extract user profile details",
            "steps": [
                "click on profile menu",
                "wait for 1 second",
                "click on settings",
                "wait for 2 seconds",
                "scroll to profile section"
            ]
        },
        {
            "name": "Repository Details",
            "url": "https://github.com/",
            "prompt": "Extract repository details",
            "steps": [
                "click on repositories tab",
                "wait for 500ms",
                "click on first repository",
                "wait for 1 second",
                "scroll to readme section"
            ]
        }
    ]
    
    print(f"🔄 Executing {len(configs)} concurrent requests...")
    start_time = time.time()
    
    try:
        async with AsyncClient.from_env() as client:
            # Create tasks for concurrent execution
            tasks = []
            for config in configs:
                task = client.smartscraper(
                    user_prompt=config["prompt"],
                    website_url=config["url"],
                    steps=config["steps"]
                )
                tasks.append(task)
            
            # Execute tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Calculate total execution time
            end_time = time.time()
            execution_time = end_time - start_time
            
            print(f"⚡ Total concurrent execution time: {execution_time:.2f} seconds")
            print(f"📊 Average per request: {execution_time/len(configs):.2f} seconds")
            
            # Display results
            print("\n📋 CONCURRENT RESULTS:")
            print("=" * 60)
            
            for i, (config, result) in enumerate(zip(configs, results), 1):
                print(f"\n{i}. {config['name']}:")
                print(f"   🎯 Prompt: {config['prompt']}")
                print(f"   📝 Steps: {len(config['steps'])}")
                
                if isinstance(result, Exception):
                    print(f"   ❌ Error: {str(result)}")
                else:
                    print(f"   ✅ Status: {result.get('status', 'N/A')}")
                    print(f"   📊 Request ID: {result.get('request_id', 'N/A')}")
                    if "result" in result:
                        data_size = len(json.dumps(result["result"]))
                        print(f"   📝 Data size: {data_size} characters")
                print("-" * 40)
                
    except Exception as e:
        print(f"💥 Error in concurrent execution: {str(e)}")


async def async_smartscraper_step_patterns():
    """
    Demonstrate different step patterns for various use cases.
    """
    print("\n🎯 DIFFERENT STEP PATTERNS DEMONSTRATION")
    print("=" * 60)
    
    patterns = [
        {
            "name": "Authentication Flow",
            "description": "Steps for logging into a website",
            "steps": [
                "click on login button",
                "wait for 1 second",
                "fill username field with user@example.com",
                "wait for 200ms",
                "fill password field with password123",
                "wait for 300ms",
                "click submit button",
                "wait for 3 seconds"
            ]
        },
        {
            "name": "Form Submission",
            "description": "Steps for filling and submitting a form",
            "steps": [
                "scroll to contact form",
                "wait for 500ms",
                "fill name field with John Doe",
                "wait for 200ms",
                "fill email field with john@example.com",
                "wait for 200ms",
                "fill message field with Hello World",
                "wait for 300ms",
                "click submit button"
            ]
        },
        {
            "name": "Dynamic Content Loading",
            "description": "Steps for loading more content dynamically",
            "steps": [
                "scroll to bottom of page",
                "wait for 1 second",
                "click load more button",
                "wait for 2 seconds",
                "scroll down again",
                "wait for 1 second",
                "click show details button"
            ]
        }
    ]
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\n📋 Pattern {i}: {pattern['name']}")
        print(f"📝 Description: {pattern['description']}")
        print(f"🎯 Steps ({len(pattern['steps'])}):")
        for j, step in enumerate(pattern['steps'], 1):
            step_type = "Navigation" if "click" in step else "Wait" if "wait" in step else "Input" if "fill" in step else "Action" if "scroll" in step else "Other"
            print(f"   {j}. {step} [{step_type}]")
        print("-" * 40)


async def main():
    """
    Main function to run the async Smart Scraper steps example.
    """
    try:
        print("🎯 ASYNC SMART SCRAPER INTERACTIVE STEPS EXAMPLE")
        print("=" * 60)
        print("This example demonstrates how to use interactive steps with Async Smart Scraper.")
        print("Interactive steps allow you to navigate websites like a human user asynchronously.")
        print("This enables faster processing through concurrent requests.")
        print()
        
        await async_smartscraper_with_steps()
        await async_smartscraper_concurrent_steps()
        await async_smartscraper_step_patterns()
        
    except Exception as e:
        print(f"💥 Error occurred: {str(e)}")
        print("\n🛠️  Troubleshooting:")
        print("1. Make sure your .env file contains SGAI_API_KEY")
        print("2. Check your internet connection")
        print("3. Verify the target website is accessible")
        print("4. Ensure you have sufficient credits in your account")


if __name__ == "__main__":
    asyncio.run(main()) 