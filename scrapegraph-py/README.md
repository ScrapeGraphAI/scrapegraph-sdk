# 🌐 ScrapeGraph Python SDK

[![PyPI version](https://badge.fury.io/py/scrapegraph-py.svg)](https://badge.fury.io/py/scrapegraph-py)
[![Python Support](https://img.shields.io/pypi/pyversions/scrapegraph-py.svg)](https://pypi.org/project/scrapegraph-py/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/scrapegraph-py/badge/?version=latest)](https://docs.scrapegraphai.com)

<p align="left">
  <img src="https://raw.githubusercontent.com/VinciGit00/Scrapegraph-ai/main/docs/assets/api-banner.png" alt="ScrapeGraph API Banner" style="width: 70%;">
</p>

Official [Python SDK ](https://scrapegraphai.com) for the ScrapeGraph API - Smart web scraping powered by AI.

## 📦 Installation

```bash
pip install scrapegraph-py
```

## 🚀 Features

- 🤖 AI-powered web scraping and search
- 🕷️ Smart crawling with both AI extraction and markdown conversion modes
- 💰 Cost-effective markdown conversion (80% savings vs AI mode)
- 🔄 Both sync and async clients
- 📊 Structured output with Pydantic schemas
- 🔍 Detailed logging
- ⚡ Automatic retries
- 🔐 Secure authentication

## 🎯 Quick Start

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")
```

> [!NOTE]
> You can set the `SGAI_API_KEY` environment variable and initialize the client without parameters: `client = Client()`

## 📚 Available Endpoints

### 🤖 SmartScraper

Extract structured data from any webpage or HTML content using AI.

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

# Using a URL
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the main heading and description"
)

# Or using HTML content
html_content = """
<html>
    <body>
        <h1>Company Name</h1>
        <p>We are a technology company focused on AI solutions.</p>
    </body>
</html>
"""

response = client.smartscraper(
    website_html=html_content,
    user_prompt="Extract the company description"
)

print(response)
```

<details>
<summary>Output Schema (Optional)</summary>

```python
from pydantic import BaseModel, Field
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

class WebsiteData(BaseModel):
    title: str = Field(description="The page title")
    description: str = Field(description="The meta description")

response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the title and description",
    output_schema=WebsiteData
)
```

</details>

<details>
<summary>🍪 Cookies Support</summary>

Use cookies for authentication and session management:

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

# Define cookies for authentication
cookies = {
    "session_id": "abc123def456",
    "auth_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_preferences": "dark_mode,usd"
}

response = client.smartscraper(
    website_url="https://example.com/dashboard",
    user_prompt="Extract user profile information",
    cookies=cookies
)
```

**Common Use Cases:**
- **E-commerce sites**: User authentication, shopping cart persistence
- **Social media**: Session management, user preferences
- **Banking/Financial**: Secure authentication, transaction history
- **News sites**: User preferences, subscription content
- **API endpoints**: Authentication tokens, API keys

</details>

<details>
<summary>🔄 Advanced Features</summary>

**Infinite Scrolling:**
```python
response = client.smartscraper(
    website_url="https://example.com/feed",
    user_prompt="Extract all posts from the feed",
    cookies=cookies,
    number_of_scrolls=10  # Scroll 10 times to load more content
)
```

**Pagination:**
```python
response = client.smartscraper(
    website_url="https://example.com/products",
    user_prompt="Extract all product information",
    cookies=cookies,
    total_pages=5  # Scrape 5 pages
)
```

**Combined with Cookies:**
```python
response = client.smartscraper(
    website_url="https://example.com/dashboard",
    user_prompt="Extract user data from all pages",
    cookies=cookies,
    number_of_scrolls=5,
    total_pages=3
)
```

</details>

### 🔍 SearchScraper

Perform AI-powered web searches with structured results and reference URLs.

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

response = client.searchscraper(
    user_prompt="What is the latest version of Python and its main features?"
)

print(f"Answer: {response['result']}")
print(f"Sources: {response['reference_urls']}")
```

<details>
<summary>Output Schema (Optional)</summary>

```python
from pydantic import BaseModel, Field
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

class PythonVersionInfo(BaseModel):
    version: str = Field(description="The latest Python version number")
    release_date: str = Field(description="When this version was released")
    major_features: list[str] = Field(description="List of main features")

response = client.searchscraper(
    user_prompt="What is the latest version of Python and its main features?",
    output_schema=PythonVersionInfo
)
```

</details>

### 📝 Markdownify

Converts any webpage into clean, formatted markdown.

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

response = client.markdownify(
    website_url="https://example.com"
)

print(response)
```

### 🕷️ Crawler

Intelligently crawl and extract data from multiple pages with support for both AI extraction and markdown conversion modes.

#### AI Extraction Mode (Default)
Extract structured data from multiple pages using AI:

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

# Define the data schema for extraction
schema = {
    "type": "object",
    "properties": {
        "company_name": {"type": "string"},
        "founders": {
            "type": "array",
            "items": {"type": "string"}
        },
        "description": {"type": "string"}
    }
}

response = client.crawl(
    url="https://scrapegraphai.com",
    prompt="extract the company information and founders",
    data_schema=schema,
    depth=2,
    max_pages=5,
    same_domain_only=True
)

# Poll for results (crawl is asynchronous)
crawl_id = response.get("crawl_id")
result = client.get_crawl(crawl_id)
```

#### Markdown Conversion Mode (Cost-Effective)
Convert pages to clean markdown without AI processing (80% cheaper):

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key-here")

response = client.crawl(
    url="https://scrapegraphai.com",
    extraction_mode=False,  # Markdown conversion mode
    depth=2,
    max_pages=5,
    same_domain_only=True,
    sitemap=True  # Use sitemap for better page discovery
)

# Poll for results
crawl_id = response.get("crawl_id")
result = client.get_crawl(crawl_id)

# Access markdown content
for page in result["result"]["pages"]:
    print(f"URL: {page['url']}")
    print(f"Markdown: {page['markdown']}")
    print(f"Metadata: {page['metadata']}")
```

<details>
<summary>🔧 Crawl Parameters</summary>

- **url** (required): Starting URL for the crawl
- **extraction_mode** (default: True):
  - `True` = AI extraction mode (requires prompt and data_schema)
  - `False` = Markdown conversion mode (no AI, 80% cheaper)
- **prompt** (required for AI mode): AI prompt to guide data extraction
- **data_schema** (required for AI mode): JSON schema defining extracted data structure
- **depth** (default: 2): Maximum crawl depth (1-10)
- **max_pages** (default: 2): Maximum pages to crawl (1-100)
- **same_domain_only** (default: True): Only crawl pages from the same domain
- **sitemap** (default: False): Use sitemap.xml for better page discovery and more comprehensive crawling
- **cache_website** (default: True): Cache website content
- **batch_size** (optional): Batch size for processing pages (1-10)

**Cost Comparison:**
- AI Extraction Mode: ~10 credits per page
- Markdown Conversion Mode: ~2 credits per page (80% savings!)

**Sitemap Benefits:**
- Better page discovery using sitemap.xml
- More comprehensive website coverage
- Efficient crawling of structured websites
- Perfect for e-commerce, news sites, and content-heavy websites

</details>

## ⚡ Async Support

All endpoints support async operations:

```python
import asyncio
from scrapegraph_py import AsyncClient

async def main():
    async with AsyncClient() as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract the main content"
        )
        print(response)

asyncio.run(main())
```

## 📖 Documentation

For detailed documentation, visit [docs.scrapegraphai.com](https://docs.scrapegraphai.com)

## 🛠️ Development

For information about setting up the development environment and contributing to the project, see our [Contributing Guide](CONTRIBUTING.md).

## 💬 Support & Feedback

- 📧 Email: support@scrapegraphai.com
- 💻 GitHub Issues: [Create an issue](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues)
- 🌟 Feature Requests: [Request a feature](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/new)
- ⭐ API Feedback: You can also submit feedback programmatically using the feedback endpoint:
  ```python
  from scrapegraph_py import Client

  client = Client(api_key="your-api-key-here")

  client.submit_feedback(
      request_id="your-request-id",
      rating=5,
      feedback_text="Great results!"
  )
  ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Website](https://scrapegraphai.com)
- [Documentation](https://docs.scrapegraphai.com)
- [GitHub](https://github.com/ScrapeGraphAI/scrapegraph-sdk)

---

Made with ❤️ by [ScrapeGraph AI](https://scrapegraphai.com)
