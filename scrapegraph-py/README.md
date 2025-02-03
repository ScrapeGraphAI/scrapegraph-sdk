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
