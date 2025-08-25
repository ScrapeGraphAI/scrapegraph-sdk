"""
Comprehensive example demonstrating advanced usage of the HTMLfy API with the scrapegraph-py SDK.

This example shows how to:
1. Set up the client for HTMLfy with various configurations
2. Handle different types of websites and rendering modes
3. Implement error handling and retry logic
4. Process multiple websites concurrently
5. Save and analyze HTML content with detailed metadata
6. Use custom headers and cookies for authentication
7. Compare different rendering modes

Requirements:
- Python 3.7+
- scrapegraph-py
- python-dotenv
- A .env file with your SGAI_API_KEY

Example .env file:
SGAI_API_KEY=your_api_key_here
"""

import json
import os
import time
from pathlib import Path
from typing import Optional, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv

from scrapegraph_py import Client

# Load environment variables from .env file
load_dotenv()


class HtmlfyProcessor:
    """A comprehensive HTMLfy processor with advanced features"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the HTMLfy processor.
        
        Args:
            api_key: API key for authentication. If None, will try to load from environment
        """
        try:
            if api_key:
                self.client = Client(api_key=api_key)
            else:
                self.client = Client.from_env()
            print("✅ Client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize client: {str(e)}")
            raise
    
    def htmlfy_website(
        self,
        website_url: str,
        render_heavy_js: bool = False,
        headers: Optional[dict[str, str]] = None,
        max_retries: int = 3,
    ) -> dict:
        """
        Get HTML content from a website using the HTMLfy API with retry logic.
        
        Args:
            website_url: The URL of the website to get HTML from
            render_heavy_js: Whether to render heavy JavaScript
            headers: Optional headers to send with the request
            max_retries: Maximum number of retry attempts
            
        Returns:
            dict: A dictionary containing the HTML content and metadata
        """
        js_mode = "with heavy JS rendering" if render_heavy_js else "without JS rendering"
        print(f"🌐 Getting HTML content from: {website_url}")
        print(f"🔧 Mode: {js_mode}")
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                result = self.client.htmlfy(
                    website_url=website_url,
                    render_heavy_js=render_heavy_js,
                    headers=headers,
                )
                execution_time = time.time() - start_time
                
                print(f"✅ Success! Execution time: {execution_time:.2f} seconds")
                return {
                    **result,
                    "execution_time": execution_time,
                    "attempts": attempt + 1,
                }
                
            except Exception as e:
                print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⏳ Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"💥 All {max_retries} attempts failed for {website_url}")
                    raise
    
    def process_website_batch(
        self,
        websites: List[Dict],
        max_workers: int = 3,
        output_dir: str = "htmlfy_output"
    ) -> List[Dict]:
        """
        Process multiple websites concurrently.
        
        Args:
            websites: List of website configurations
            max_workers: Maximum number of concurrent workers
            output_dir: Directory to save output files
            
        Returns:
            List of results for each website
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_website = {
                executor.submit(
                    self._process_single_website, website, output_dir
                ): website
                for website in websites
            }
            
            # Process completed tasks
            for future in as_completed(future_to_website):
                website = future_to_website[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"✅ Completed: {website['url']}")
                except Exception as e:
                    print(f"❌ Failed: {website['url']} - {str(e)}")
                    results.append({
                        "website": website,
                        "error": str(e),
                        "status": "failed"
                    })
        
        return results
    
    def _process_single_website(
        self, website: Dict, output_dir: str
    ) -> Dict:
        """Process a single website and return results."""
        try:
            # Get HTML content
            result = self.htmlfy_website(
                website_url=website["url"],
                render_heavy_js=website.get("render_heavy_js", False),
                headers=website.get("headers"),
            )
            
            # Analyze HTML content
            html_content = result.get("html", "")
            if html_content:
                stats = self.analyze_html_content(html_content)
                result["analysis"] = stats
                
                # Save HTML content
                filename = self._generate_filename(website, result)
                saved_file = self.save_html_content(html_content, filename, output_dir)
                result["saved_file"] = str(saved_file)
                
                # Generate summary
                result["summary"] = self.generate_summary(stats, result)
            
            return {
                "website": website,
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "website": website,
                "error": str(e),
                "status": "failed"
            }
    
    def analyze_html_content(self, html_content: str) -> dict:
        """
        Analyze HTML content and provide comprehensive statistics.
        
        Args:
            html_content: The HTML content to analyze
            
        Returns:
            dict: Comprehensive statistics about the HTML content
        """
        stats = {
            "basic": {
                "total_length": len(html_content),
                "lines": len(html_content.splitlines()),
                "words": len(html_content.split()),
                "characters_no_spaces": len(html_content.replace(" ", "")),
            },
            "structure": {
                "has_doctype": html_content.strip().startswith("<!DOCTYPE"),
                "has_html_tag": "<html" in html_content.lower(),
                "has_head_tag": "<head" in html_content.lower(),
                "has_body_tag": "<body" in html_content.lower(),
                "has_title_tag": "<title" in html_content.lower(),
                "has_meta_tags": html_content.lower().count("<meta"),
            },
            "elements": {
                "script_tags": html_content.lower().count("<script"),
                "style_tags": html_content.lower().count("<style"),
                "div_tags": html_content.lower().count("<div"),
                "p_tags": html_content.lower().count("<p"),
                "img_tags": html_content.lower().count("<img"),
                "link_tags": html_content.lower().count("<link"),
                "a_tags": html_content.lower().count("<a"),
                "span_tags": html_content.lower().count("<span"),
                "table_tags": html_content.lower().count("<table"),
                "form_tags": html_content.lower().count("<form"),
            },
            "content": {
                "has_javascript": "<script" in html_content.lower(),
                "has_css": "<style" in html_content.lower(),
                "has_forms": "<form" in html_content.lower(),
                "has_tables": "<table" in html_content.lower(),
                "has_images": "<img" in html_content.lower(),
                "has_links": "<a" in html_content.lower(),
            }
        }
        
        return stats
    
    def generate_summary(self, stats: Dict, result: Dict) -> str:
        """Generate a human-readable summary of the HTML content."""
        basic = stats["basic"]
        elements = stats["elements"]
        
        summary = f"HTML document with {basic['total_length']:,} characters "
        summary += f"({basic['lines']:,} lines, {basic['words']:,} words). "
        
        if elements["div_tags"] > 0:
            summary += f"Contains {elements['div_tags']} div elements, "
        if elements["p_tags"] > 0:
            summary += f"{elements['p_tags']} paragraphs, "
        if elements["img_tags"] > 0:
            summary += f"{elements['img_tags']} images, "
        if elements["script_tags"] > 0:
            summary += f"{elements['script_tags']} script tags, "
        if elements["style_tags"] > 0:
            summary += f"{elements['style_tags']} style tags. "
        
        execution_time = result.get("execution_time", 0)
        summary += f"Processed in {execution_time:.2f} seconds."
        
        return summary
    
    def _generate_filename(self, website: Dict, result: Dict) -> str:
        """Generate a filename for the saved HTML content."""
        name = website.get("name", "website")
        js_mode = "js" if website.get("render_heavy_js", False) else "nojs"
        timestamp = int(time.time())
        return f"{name}_{js_mode}_{timestamp}"
    
    def save_html_content(
        self, html_content: str, filename: str, output_dir: str = "htmlfy_output"
    ) -> Path:
        """
        Save HTML content to a file with metadata.
        
        Args:
            html_content: The HTML content to save
            filename: The name of the file (without extension)
            output_dir: The directory to save the file in
            
        Returns:
            Path to the saved file
        """
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save HTML file
        html_file = output_path / f"{filename}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Save metadata file
        metadata_file = output_path / f"{filename}_metadata.json"
        metadata = {
            "filename": filename,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_size": len(html_content),
            "encoding": "utf-8"
        }
        
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 HTML content saved to: {html_file}")
        print(f"📊 Metadata saved to: {metadata_file}")
        return html_file
    
    def close(self):
        """Close the client to free up resources."""
        self.client.close()
        print("🔒 Client closed successfully")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Main function demonstrating comprehensive HTMLfy usage."""
    
    # Example websites with different configurations
    test_websites = [
        {
            "url": "https://example.com",
            "name": "example",
            "render_heavy_js": False,
            "description": "Simple static website",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        },
        {
            "url": "https://httpbin.org/html",
            "name": "httpbin_html",
            "render_heavy_js": False,
            "description": "HTTP testing service",
        },
        {
            "url": "https://httpbin.org/json",
            "name": "httpbin_json",
            "render_heavy_js": False,
            "description": "JSON endpoint",
        },
        {
            "url": "https://httpbin.org/headers",
            "name": "httpbin_headers",
            "render_heavy_js": False,
            "description": "Headers endpoint",
            "headers": {
                "User-Agent": "ScrapeGraph-HTMLfy-Example/1.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            }
        }
    ]
    
    print("🚀 Comprehensive HTMLfy API Example with scrapegraph-py SDK")
    print("=" * 70)
    
    try:
        with HtmlfyProcessor() as processor:
            print("\n📋 Processing websites...")
            
            # Process websites concurrently
            results = processor.process_website_batch(
                websites=test_websites,
                max_workers=2,  # Limit concurrent requests
                output_dir="htmlfy_comprehensive_output"
            )
            
            # Display summary
            print("\n📊 Processing Summary")
            print("=" * 50)
            
            successful = [r for r in results if r["status"] == "success"]
            failed = [r for r in results if r["status"] == "failed"]
            
            print(f"✅ Successful: {len(successful)}")
            print(f"❌ Failed: {len(failed)}")
            
            if successful:
                print(f"\n🎯 Successful Results:")
                for result in successful:
                    website = result["website"]
                    data = result["result"]
                    summary = data.get("summary", "No summary available")
                    print(f"  🌐 {website['url']}: {summary}")
            
            if failed:
                print(f"\n💥 Failed Results:")
                for result in failed:
                    website = result["website"]
                    error = result["error"]
                    print(f"  🌐 {website['url']}: {error}")
            
            print(f"\n📁 Output saved to: htmlfy_comprehensive_output/")
            
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        print("Make sure you have SGAI_API_KEY in your .env file")


if __name__ == "__main__":
    main()
