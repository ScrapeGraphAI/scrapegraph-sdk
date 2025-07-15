"""
Example demonstrating how to use the Smart Scraper API with interactive steps.
This example shows how to:
1. Set up interactive steps for website navigation
2. Use the Smart Scraper API with custom steps
3. Handle the response and display results with timing
4. Demonstrate the power of interactive movements

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

import json
import os
import time
from dotenv import load_dotenv
from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()


def smart_scraper_with_steps():
    """
    Enhanced Smart Scraper function with interactive steps and comprehensive timing.
    This demonstrates how to use interactive movements to navigate websites.
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

    print("🚀 Starting Smart Scraper with Interactive Steps...")
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
    print("🔄 Processing request with interactive steps...")

    try:
        # Initialize client
        with Client.from_env() as client:
            # Make request with interactive steps
            response = client.smartscraper(
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


def smart_scraper_multiple_scenarios():
    """
    Demonstrate different interactive step scenarios.
    """
    print("\n🎯 MULTIPLE SCENARIOS DEMONSTRATION")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Basic Search",
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
            "name": "Form Interaction",
            "url": "https://scrapegraphai.com/",
            "prompt": "Extract contact information",
            "steps": [
                "scroll down to contact form",
                "wait for 500ms",
                "click on email field",
                "wait for 200ms",
                "fill email with test@example.com"
            ]
        },
        {
            "name": "Navigation Flow",
            "url": "https://github.com/",
            "prompt": "Extract user profile",
            "steps": [
                "click on profile menu",
                "wait for 1 second",
                "click on settings",
                "wait for 2 seconds",
                "scroll to profile section"
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"🌐 URL: {scenario['url']}")
        print(f"🎯 Prompt: {scenario['prompt']}")
        print(f"📝 Steps: {len(scenario['steps'])}")
        for j, step in enumerate(scenario['steps'], 1):
            print(f"    {j}. {step}")
        print("-" * 40)


def main():
    """
    Main function to run the Smart Scraper steps example.
    """
    try:
        print("🎯 SMART SCRAPER INTERACTIVE STEPS EXAMPLE")
        print("=" * 60)
        print("This example demonstrates how to use interactive steps with Smart Scraper.")
        print("Interactive steps allow you to navigate websites like a human user.")
        print()
        
        smart_scraper_with_steps()
        smart_scraper_multiple_scenarios()
        
    except Exception as e:
        print(f"💥 Error occurred: {str(e)}")
        print("\n🛠️  Troubleshooting:")
        print("1. Make sure your .env file contains SGAI_API_KEY")
        print("2. Check your internet connection")
        print("3. Verify the target website is accessible")
        print("4. Ensure you have sufficient credits in your account")


if __name__ == "__main__":
    main() 