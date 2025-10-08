"""
Asynchronous example demonstrating how to use the Sitemap API.

This example shows:
1. How to extract URLs from a website's sitemap asynchronously
2. How to process multiple sitemaps concurrently
3. How to combine sitemap with async smartscraper operations

The Sitemap API automatically discovers the sitemap from:
- robots.txt file
- Common locations like /sitemap.xml
- Sitemap index files

Requirements:
- Python 3.10+
- scrapegraph-py
- python-dotenv
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

import asyncio
from pathlib import Path
from dotenv import load_dotenv

from scrapegraph_py import AsyncClient

# Load environment variables from .env file
load_dotenv()


async def basic_sitemap_example():
    """Demonstrate basic async sitemap extraction."""
    print("🗺️  Basic Async Sitemap Example")
    print("=" * 40)

    async with AsyncClient.from_env() as client:
        try:
            # Extract sitemap URLs
            print("Extracting sitemap from https://scrapegraphai.com...")
            response = await client.sitemap(website_url="https://scrapegraphai.com")

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


async def save_urls_to_file(urls: list[str], filename: str):
    """Save sitemap URLs to a text file asynchronously."""
    output_dir = Path("sitemap_output")
    output_dir.mkdir(exist_ok=True)

    file_path = output_dir / f"{filename}.txt"

    # Use asyncio to write file asynchronously
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        lambda: file_path.write_text("\n".join(urls), encoding="utf-8")
    )

    print(f"💾 URLs saved to: {file_path}")
    return file_path


async def concurrent_sitemaps_example():
    """Demonstrate extracting multiple sitemaps concurrently."""
    print("\n⚡ Concurrent Sitemaps Example")
    print("=" * 40)

    websites = [
        "https://scrapegraphai.com",
        "https://example.com",
        "https://python.org"
    ]

    async with AsyncClient.from_env() as client:
        try:
            print(f"Extracting sitemaps from {len(websites)} websites concurrently...")

            # Create tasks for concurrent execution
            tasks = [
                client.sitemap(website_url=url)
                for url in websites
            ]

            # Execute all tasks concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            successful = 0
            for url, result in zip(websites, results):
                if isinstance(result, Exception):
                    print(f"❌ {url}: {str(result)}")
                else:
                    print(f"✅ {url}: {len(result.urls)} URLs")
                    successful += 1

            print(f"\n📊 Summary: {successful}/{len(websites)} successful")

            return [r for r in results if not isinstance(r, Exception)]

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None


async def filter_and_scrape_example():
    """Demonstrate filtering sitemap URLs and scraping them asynchronously."""
    print("\n🤖 Filter + Async Scrape Example")
    print("=" * 40)

    async with AsyncClient.from_env() as client:
        try:
            # Extract sitemap
            print("Step 1: Extracting sitemap...")
            response = await client.sitemap(website_url="https://scrapegraphai.com")

            # Filter for specific URLs
            target_urls = [url for url in response.urls if '/blog/' in url][:3]

            if not target_urls:
                target_urls = response.urls[:3]

            print(f"✅ Found {len(response.urls)} URLs")
            print(f"🎯 Selected {len(target_urls)} URLs to scrape\n")

            # Create scraping tasks
            print("Step 2: Scraping URLs concurrently...")

            async def scrape_url(url):
                """Scrape a single URL."""
                try:
                    result = await client.smartscraper(
                        website_url=url,
                        user_prompt="Extract the page title and main heading"
                    )
                    return {
                        'url': url,
                        'data': result.get('result'),
                        'status': 'success'
                    }
                except Exception as e:
                    return {
                        'url': url,
                        'error': str(e),
                        'status': 'failed'
                    }

            # Execute scraping tasks concurrently
            tasks = [scrape_url(url) for url in target_urls]
            results = await asyncio.gather(*tasks)

            # Display results
            successful = sum(1 for r in results if r['status'] == 'success')
            print(f"\n📊 Summary:")
            print(f"   ✅ Successful: {successful}/{len(results)}")
            print(f"   ❌ Failed: {len(results) - successful}/{len(results)}")

            # Show sample results
            print("\nSample results:")
            for i, result in enumerate(results[:3], 1):
                print(f"\n   {i}. {result['url']}")
                if result['status'] == 'success':
                    print(f"      Data: {result['data']}")
                else:
                    print(f"      Error: {result['error']}")

            return results

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None


async def batch_process_with_rate_limit():
    """Demonstrate batch processing with rate limiting."""
    print("\n⏱️  Batch Processing with Rate Limit")
    print("=" * 40)

    async with AsyncClient.from_env() as client:
        try:
            # Extract sitemap
            print("Extracting sitemap...")
            response = await client.sitemap(website_url="https://scrapegraphai.com")

            # Get URLs to process
            urls_to_process = response.urls[:10]
            print(f"Processing {len(urls_to_process)} URLs with rate limiting...")

            # Process in batches to avoid overwhelming the API
            batch_size = 3
            results = []

            for i in range(0, len(urls_to_process), batch_size):
                batch = urls_to_process[i:i + batch_size]
                print(f"\nProcessing batch {i // batch_size + 1}...")

                # Process batch
                batch_tasks = [
                    client.smartscraper(
                        website_url=url,
                        user_prompt="Extract title"
                    )
                    for url in batch
                ]

                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                results.extend(batch_results)

                # Rate limiting: wait between batches
                if i + batch_size < len(urls_to_process):
                    print("Waiting 2 seconds before next batch...")
                    await asyncio.sleep(2)

            successful = sum(1 for r in results if not isinstance(r, Exception))
            print(f"\n✅ Processed {successful}/{len(results)} URLs successfully")

            return results

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None


async def main():
    """Main function demonstrating async sitemap functionality."""
    print("🚀 Async Sitemap API Examples")
    print("=" * 40)

    try:
        # Basic sitemap extraction
        response = await basic_sitemap_example()

        if response and response.urls:
            # Save URLs to file
            await save_urls_to_file(response.urls, "async_scrapegraphai_sitemap")

        # Concurrent sitemaps
        await concurrent_sitemaps_example()

        # Filter and scrape
        await filter_and_scrape_example()

        # Batch processing with rate limit
        await batch_process_with_rate_limit()

        print("\n🎯 All examples completed!")

    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

    print("\n📚 Next steps:")
    print("• Experiment with different websites")
    print("• Adjust batch sizes for your use case")
    print("• Combine with other async operations")
    print("• Implement custom error handling and retry logic")


if __name__ == "__main__":
    asyncio.run(main())
