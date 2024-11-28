# 🌐 ScrapeGraph Python SDK

[![PyPI version](https://badge.fury.io/py/scrapegraph-py.svg)](https://badge.fury.io/py/scrapegraph-py)
[![Python Support](https://img.shields.io/pypi/pyversions/scrapegraph-py.svg)](https://pypi.org/project/scrapegraph-py/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/scrapegraph-py/badge/?version=latest)](https://scrapegraph-py.readthedocs.io/en/latest/?badge=latest)

Official Python SDK for the ScrapeGraph AI API - Smart web scraping powered by AI.

## 🚀 Features

- ✨ Smart web scraping with AI
- 🔄 Both sync and async clients
- 📊 Structured output with Pydantic schemas
- 🔍 Detailed logging with emojis
- ⚡ Automatic retries and error handling
- 🔐 Secure API authentication

## 📦 Installation

### Using pip

```
pip install scrapegraph-py
```

### Using Poetry (Recommended)

```
# Install poetry if you haven't already
pip install poetry

# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

## 🔧 Quick Start

> [!NOTE]
> If you prefer, you can use the environment variables to configure the API key and load them using `load_dotenv()`

```python
from scrapegraph_py import SyncClient
from scrapegraph_py.logger import get_logger

# Enable debug logging
logger = get_logger(level="DEBUG")

# Initialize client
client = SyncClient(api_key="sgai-your-api-key")

# Make a request
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the main heading and description"
)

print(response)
```

## 🎯 Examples

### Async Usage

```python
import asyncio
from scrapegraph_py import AsyncClient

async def main():
    async with AsyncClient(api_key="sgai-your-api-key") as client:
        response = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract the main heading"
        )
        print(response)

asyncio.run(main())
```

<details>
<summary><b>With Output Schema</b></summary>

```python
from pydantic import BaseModel, Field
from scrapegraph_py import SyncClient

class WebsiteData(BaseModel):
    title: str = Field(description="The page title")
    description: str = Field(description="The meta description")

client = SyncClient(api_key="sgai-your-api-key")
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the title and description",
    output_schema=WebsiteData
)
```
</details>

## 📚 Documentation

For detailed documentation, visit [docs.scrapegraphai.com](https://docs.scrapegraphai.com)

## 🛠️ Development

### Setup

1. Clone the repository:
```
git clone https://github.com/ScrapeGraphAI/scrapegraph-sdk.git
cd scrapegraph-sdk
```

2. Install dependencies:
```
poetry install
```

3. Install pre-commit hooks:
```
poetry run pre-commit install
```

### Running Tests

```
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=scrapegraph_py

# Run specific test file
poetry run pytest tests/test_client.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🔗 Links

- [Website](https://scrapegraphai.com)
- [Documentation](https://docs.scrapegraphai.com)
- [API Reference](https://docs.scrapegraphai.com/api)
- [GitHub](https://github.com/ScrapeGraphAI/scrapegraph-sdk)

## 💬 Support

- 📧 Email: support@scrapegraphai.com
- 💻 GitHub Issues: [Create an issue](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues)
- 🌟 Feature Requests: [Request a feature](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/new)

---

Made with ❤️ by [ScrapeGraph AI](https://scrapegraphai.com)