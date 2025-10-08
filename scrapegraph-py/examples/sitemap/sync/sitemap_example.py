"""
Basic synchronous example demonstrating how to use the Sitemap API.

This example shows:
1. How to extract URLs from a website's sitemap
2. How to save sitemap URLs to a file
3. How to combine sitemap with other scraping operations

The Sitemap API automatically discovers the sitemap from:
- robots.txt file
- Common locations like /sitemap.xml
- Sitemap index files

Equivalent curl command:
curl -X POST https://api.scrapegraphai.com/v1/sitemap \
  -H "Content-Type: application/json" \
  -H "SGAI-APIKEY: your-api-key-here" \
  -d '{
    "website_url": "https://example.com"
  }'

Requirements:
- Python 3.10+
- scrapegraph-py
- python-dotenv
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

from pathlib import Path
from dotenv import load_dotenv

from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()


def basic_sitemap_example():
    """Demonstrate basic sitemap extraction."""
    print("🗺️  Basic Sitemap Example")
    print("=" * 40)

    # Initialize client
    client = Client.from_env()

    try:
        # Extract sitemap URLs
        print("Extracting sitemap from https://scrapegraphai.com...")
        response = client.sitemap(website_url="https://scrapegraphai.com")

        # Display results
        print(f"✅ Success! Found {len(response.urls)} URLs\n")

        # Show first 10 URLs
        print("First 10 URLs:")
        for i, url in enumerate(response.urls[:10], 1):
            print(f"   {i}. {url}")

        if len(response.urls) > 10:
            print(f"   ... and {len(response.urls) - 10} more URLs")

        return response

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    finally:
        client.close()


def save_urls_to_file(urls: list[str], filename: str):
    """Save sitemap URLs to a text file."""
    output_dir = Path("sitemap_output")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / f"{filename}.txt"
    with open(file_path, "w", encoding="utf-8") as f:
        for url in urls:
            f.write(url + "\n")

    print(f"💾 URLs saved to: {file_path}")
    return file_path


def filter_urls_example():
    """Demonstrate filtering sitemap URLs by pattern."""
    print("\n🔍 Filtering URLs Example")
    print("=" * 40)

    client = Client.from_env()

    try:
        # Extract sitemap
        print("Extracting sitemap...")
        response = client.sitemap(website_url="https://scrapegraphai.com")

        # Filter URLs containing specific patterns
        blog_urls = [url for url in response.urls if '/blog/' in url]
        doc_urls = [url for url in response.urls if '/docs/' in url or '/documentation/' in url]

        print(f"✅ Total URLs: {len(response.urls)}")
        print(f"📝 Blog URLs: {len(blog_urls)}")
        print(f"📚 Documentation URLs: {len(doc_urls)}")

        # Show sample blog URLs
        if blog_urls:
            print("\nSample blog URLs:")
            for url in blog_urls[:5]:
                print(f"   • {url}")

        return {
            'all_urls': response.urls,
            'blog_urls': blog_urls,
            'doc_urls': doc_urls
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    finally:
        client.close()


def combine_with_smartscraper():
    """Demonstrate combining sitemap with smartscraper."""
    print("\n🤖 Sitemap + SmartScraper Example")
    print("=" * 40)

    client = Client.from_env()

    try:
        # First, get sitemap URLs
        print("Step 1: Extracting sitemap...")
        sitemap_response = client.sitemap(website_url="https://scrapegraphai.com")

        # Filter for specific pages (e.g., blog posts)
        target_urls = [url for url in sitemap_response.urls if '/blog/' in url][:3]

        if not target_urls:
            # If no blog URLs, use first 3 URLs
            target_urls = sitemap_response.urls[:3]

        print(f"✅ Found {len(sitemap_response.urls)} URLs")
        print(f"🎯 Selected {len(target_urls)} URLs to scrape\n")

        # Scrape selected URLs
        print("Step 2: Scraping selected URLs...")
        results = []

        for i, url in enumerate(target_urls, 1):
            print(f"   Scraping ({i}/{len(target_urls)}): {url}")

            try:
                # Use smartscraper to extract data
                scrape_result = client.smartscraper(
                    website_url=url,
                    user_prompt="Extract the page title and main heading"
                )

                results.append({
                    'url': url,
                    'data': scrape_result.get('result'),
                    'status': 'success'
                })
                print(f"      ✅ Success")

            except Exception as e:
                results.append({
                    'url': url,
                    'error': str(e),
                    'status': 'failed'
                })
                print(f"      ❌ Failed: {str(e)}")

        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        print(f"\n📊 Summary:")
        print(f"   ✅ Successful: {successful}/{len(results)}")
        print(f"   ❌ Failed: {len(results) - successful}/{len(results)}")

        return results

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    finally:
        client.close()


def demonstrate_curl_equivalent():
    """Show the equivalent curl command."""
    print("\n🌐 Equivalent curl command:")
    print("=" * 40)

    print("curl -X POST https://api.scrapegraphai.com/v1/sitemap \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -H \"SGAI-APIKEY: your-api-key-here\" \\")
    print("  -d '{")
    print("    \"website_url\": \"https://scrapegraphai.com\"")
    print("  }'")


def main():
    """Main function demonstrating sitemap functionality."""
    print("🚀 Sitemap API Examples")
    print("=" * 40)

    # Show curl equivalent first
    demonstrate_curl_equivalent()

    try:
        # Run examples
        print("\n" + "=" * 40 + "\n")

        # Basic sitemap extraction
        response = basic_sitemap_example()

        if response and response.urls:
            # Save URLs to file
            save_urls_to_file(response.urls, "scrapegraphai_sitemap")

        # Filter URLs by pattern
        filtered = filter_urls_example()

        if filtered:
            # Save filtered URLs
            if filtered['blog_urls']:
                save_urls_to_file(filtered['blog_urls'], "blog_urls")
            if filtered['doc_urls']:
                save_urls_to_file(filtered['doc_urls'], "doc_urls")

        # Advanced: Combine with smartscraper
        combine_with_smartscraper()

        print("\n🎯 All examples completed!")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

    print("\n📚 Next steps:")
    print("• Try the curl command in your terminal")
    print("• Experiment with different websites")
    print("• Combine sitemap with other scraping operations")
    print("• Filter URLs based on your specific needs")


if __name__ == "__main__":
    main()
