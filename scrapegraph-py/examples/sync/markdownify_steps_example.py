"""
Example demonstrating how to use the Markdownify API with interactive steps.
This example shows how to:
1. Set up interactive steps for website navigation before markdown conversion
2. Use the Markdownify API with custom steps
3. Handle the response and save the markdown content
4. Display comprehensive results with statistics and timing

Note: While Markdownify primarily converts websites to clean markdown format,
interactive steps can be used to navigate to specific content before conversion.

Interactive steps allow you to:
- Navigate to specific sections
- Click on elements to expand content
- Fill forms to access gated content
- Wait for dynamic content to load
- Perform authentication flows

Requirements:
- Python 3.7+
- scrapegraph-py
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

import os
import time
from dotenv import load_dotenv
from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()


def markdownify_with_steps():
    """
    Enhanced markdownify function with interactive steps and comprehensive timing.
    This demonstrates how to use interactive movements before markdown conversion.
    """
    
    # Get API key from environment
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        raise ValueError(
            "API key must be provided or set in .env file as SGAI_API_KEY. "
            "Create a .env file with: SGAI_API_KEY=your_api_key_here"
        )

    # Interactive steps for website navigation before markdown conversion
    steps = [
        "click on search bar",
        "wait for 500ms",
        "fill email input box with mdehsan873@gmail.com",
        "wait a sec",
        "click on the first result of search",
        "wait for 2 seconds to load the result of search",
    ]

    # Target website configuration
    website_url = "https://scrapegraphai.com/"
    
    # Enhanced headers for better scraping
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    print("🚀 Starting Markdownify with Interactive Steps...")
    print(f"🌐 Website URL: {website_url}")
    print(f"📋 Custom Headers: {len(custom_headers)} headers configured")
    print(f"🎯 Interactive Steps: {len(steps)} steps configured")
    print(f"📝 Goal: Convert website to clean markdown format after navigation")
    print("\n" + "=" * 60)

    # Display interactive steps
    print("🎯 Interactive Steps to Execute:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step}")
    print("\n" + "=" * 60)

    # Start timer
    start_time = time.time()
    print(f"⏱️  Timer started at: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    print("🔄 Processing markdown conversion with interactive steps...")

    try:
        # Initialize client
        with Client.from_env() as client:
            # Make request with interactive steps
            response = client.markdownify(
                website_url=website_url,
                headers=custom_headers,
                steps=steps
            )

            # Calculate execution time
            end_time = time.time()
            execution_time = end_time - start_time
            execution_minutes = execution_time / 60

            print(f"⏱️  Timer stopped at: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
            print(f"⚡ Total execution time: {execution_time:.2f} seconds ({execution_minutes:.2f} minutes)")
            print(f"📊 Performance: {execution_time:.1f}s ({execution_minutes:.1f}m) for markdown conversion with {len(steps)} steps")

            # Display results
            markdown_content = response.get("result", "")
            print("✅ Request completed successfully!")
            print(f"📊 Request ID: {response.get('request_id', 'N/A')}")
            print(f"🔄 Status: {response.get('status', 'N/A')}")
            print(f"📝 Content Length: {len(markdown_content)} characters")

            if response.get("error"):
                print(f"❌ Error: {response['error']}")
            else:
                print("\n📋 MARKDOWN CONVERSION RESULTS:")
                print("=" * 60)
                
                # Display markdown statistics
                lines = markdown_content.split("\n")
                words = len(markdown_content.split())
                print(f"📊 Statistics:")
                print(f"   - Total Lines: {len(lines)}")
                print(f"   - Total Words: {words}")
                print(f"   - Total Characters: {len(markdown_content)}")
                print(f"   - Processing Speed: {len(markdown_content)/execution_time:.0f} chars/second")
                print(f"   - Steps Efficiency: {execution_time/len(steps):.2f}s per step")

                # Display first 500 characters
                print(f"\n🔍 First 500 characters:")
                print("-" * 50)
                print(markdown_content[:500])
                if len(markdown_content) > 500:
                    print("...")
                print("-" * 50)

                # Save to file
                filename = f"markdownify_steps_output_{int(time.time())}.md"
                save_markdown_to_file(markdown_content, filename)

                # Display content analysis
                analyze_markdown_content(markdown_content, steps)

    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        execution_minutes = execution_time / 60
        
        print(f"⏱️  Timer stopped at: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"⚡ Execution time before error: {execution_time:.2f} seconds ({execution_minutes:.2f} minutes)")
        print(f"💥 Error occurred: {str(e)}")


def save_markdown_to_file(markdown_content: str, filename: str):
    """
    Save markdown content to a file with enhanced error handling.
    
    Args:
        markdown_content: The markdown content to save
        filename: The name of the file to save to
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"💾 Markdown saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")


def analyze_markdown_content(markdown_content: str, steps: list):
    """
    Analyze the markdown content and provide insights.
    
    Args:
        markdown_content: The markdown content to analyze
        steps: The interactive steps that were executed
    """
    print(f"\n🔍 CONTENT ANALYSIS:")
    print("-" * 50)
    
    # Count different markdown elements
    lines = markdown_content.split("\n")
    headers = [line for line in lines if line.strip().startswith("#")]
    links = [line for line in lines if "[" in line and "](" in line]
    code_blocks = markdown_content.count("```")
    
    print(f"📑 Headers found: {len(headers)}")
    print(f"🔗 Links found: {len(links)}")
    print(f"💻 Code blocks: {code_blocks // 2}")  # Divide by 2 since each block has opening and closing
    print(f"🎯 Interactive steps executed: {len(steps)}")
    
    # Show first few headers if they exist
    if headers:
        print(f"\n📋 First few headers:")
        for i, header in enumerate(headers[:3]):
            print(f"   {i+1}. {header.strip()}")
        if len(headers) > 3:
            print(f"   ... and {len(headers) - 3} more")
    
    # Show which steps might have contributed to content
    print(f"\n🔧 Steps Analysis:")
    for i, step in enumerate(steps, 1):
        step_type = "Navigation" if "click" in step else "Wait" if "wait" in step else "Input" if "fill" in step else "Other"
        print(f"   {i}. {step} [{step_type}]")


def markdownify_multiple_scenarios():
    """
    Demonstrate different interactive step scenarios for markdownify.
    """
    print("\n🎯 MULTIPLE SCENARIOS DEMONSTRATION")
    print("=" * 60)
    
    scenarios = [
        {
            "name": "Documentation Navigation",
            "url": "https://docs.scrapegraphai.com/",
            "steps": [
                "click on getting started menu",
                "wait for 1 second",
                "scroll down to examples section",
                "wait for 500ms",
                "click on first example"
            ]
        },
        {
            "name": "Blog Content Access",
            "url": "https://scrapegraphai.com/blog/",
            "steps": [
                "click on latest blog post",
                "wait for 2 seconds",
                "scroll to full content",
                "wait for 1 second",
                "click read more if available"
            ]
        },
        {
            "name": "Product Information",
            "url": "https://scrapegraphai.com/",
            "steps": [
                "click on features menu",
                "wait for 500ms",
                "scroll to pricing section",
                "wait for 1 second",
                "click on enterprise plan"
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 Scenario {i}: {scenario['name']}")
        print(f"🌐 URL: {scenario['url']}")
        print(f"📝 Steps: {len(scenario['steps'])}")
        for j, step in enumerate(scenario['steps'], 1):
            print(f"    {j}. {step}")
        print("-" * 40)


def main():
    """
    Main function to run the markdownify steps example.
    """
    try:
        print("🎯 MARKDOWNIFY INTERACTIVE STEPS EXAMPLE")
        print("=" * 60)
        print("This example demonstrates how to use interactive steps with Markdownify.")
        print("Interactive steps allow you to navigate to specific content before conversion.")
        print("This is useful for accessing gated content, expanding sections, or navigating SPAs.")
        print()
        
        markdownify_with_steps()
        markdownify_multiple_scenarios()
        
    except Exception as e:
        print(f"💥 Error occurred: {str(e)}")
        print("\n🛠️  Troubleshooting:")
        print("1. Make sure your .env file contains SGAI_API_KEY")
        print("2. Check your internet connection")
        print("3. Verify the target website is accessible")
        print("4. Ensure you have sufficient credits in your account")


if __name__ == "__main__":
    main() 