"""
SmartScraper with Local HTML File Example

This example demonstrates how to use SmartScraper with a local HTML file
instead of fetching content from a URL. Perfect for:
- Testing with static HTML files
- Processing saved web pages
- Working offline
- Debugging and development

Requirements:
- SGAI_API_KEY environment variable must be set
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

# Load environment variables from .env file
load_dotenv()

sgai_logger.set_logging(level="INFO")


def read_html_file(file_path: str) -> str:
    """
    Read HTML content from a local file.

    Args:
        file_path: Path to the HTML file

    Returns:
        HTML content as string
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        raise
    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        raise


def main():
    """Extract data from a local HTML file using SmartScraper."""

    # Initialize the client with API key from environment variable
    api_key = os.getenv("SGAI_API_KEY")
    if not api_key:
        print("❌ Error: SGAI_API_KEY environment variable not set")
        print("Please either:")
        print("  1. Set environment variable: export SGAI_API_KEY='your-api-key-here'")
        print("  2. Create a .env file with: SGAI_API_KEY=your-api-key-here")
        return

    # Path to the sample HTML file in the same directory
    script_dir = Path(__file__).parent
    html_file_path = script_dir / "sample_product.html"

    # Check if the HTML file exists
    if not html_file_path.exists():
        print(f"❌ HTML file not found at: {html_file_path}")
        print("   Make sure sample_product.html exists in the sync/ directory")
        return

    # Read the HTML file
    print(f"📂 Reading HTML file: {html_file_path.name}")
    html_content = read_html_file(str(html_file_path))

    # Check file size (max 2MB)
    html_size_mb = len(html_content.encode("utf-8")) / (1024 * 1024)
    print(f"📊 HTML file size: {html_size_mb:.4f} MB")

    if html_size_mb > 2:
        print("❌ HTML file exceeds 2MB limit")
        return

    # Define what to extract
    user_prompt = "Extract the product name, price, description, all features, and contact information"

    # Create client and scrape using local HTML
    sgai_client = Client(api_key=api_key)

    print(f"🎯 Prompt: {user_prompt}")
    print()

    # Pass website_html instead of website_url
    # Note: website_url should be empty string when using website_html
    response = sgai_client.smartscraper(
        website_url="",  # Empty when using website_html
        user_prompt=user_prompt,
        website_html=html_content,  # Pass the HTML content here
    )

    # Print the response
    print("✅ Success! Extracted data from local HTML:")
    print()
    print(f"Request ID: {response['request_id']}")
    print(f"Result: {response['result']}")
    print()

    sgai_client.close()


if __name__ == "__main__":
    print("SmartScraper with Local HTML File Example")
    print("=" * 45)
    print()
    main()
