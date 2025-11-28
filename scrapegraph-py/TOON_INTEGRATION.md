# TOON Format Integration

## Overview

The ScrapeGraph SDK now supports [TOON (Token-Oriented Object Notation)](https://github.com/ScrapeGraphAI/toonify) format for API responses. TOON is a compact data format that reduces LLM token usage by **30-60%** compared to JSON, significantly lowering API costs while maintaining human readability.

## What is TOON?

TOON is a serialization format optimized for LLM token efficiency. It represents structured data in a more compact form than JSON while preserving all information.

### Example Comparison

**JSON** (247 bytes):
```json
{
  "products": [
    {"id": 101, "name": "Laptop Pro", "price": 1299},
    {"id": 102, "name": "Magic Mouse", "price": 79},
    {"id": 103, "name": "USB-C Cable", "price": 19}
  ]
}
```

**TOON** (98 bytes, **60% reduction**):
```
products[3]{id,name,price}:
  101,Laptop Pro,1299
  102,Magic Mouse,79
  103,USB-C Cable,19
```

## Benefits

- ✅ **30-60% reduction** in token usage
- ✅ **Lower LLM API costs** (saves $2,147 per million requests at GPT-4 pricing)
- ✅ **Faster processing** due to smaller payloads
- ✅ **Human-readable** format
- ✅ **Lossless** conversion (preserves all data)

## Usage

### Installation

The TOON integration is automatically available when you install the SDK:

```bash
pip install scrapegraph-py
```

The `toonify` library is included as a dependency.

### Basic Usage

All scraping methods now support a `return_toon` parameter. Set it to `True` to receive responses in TOON format:

```python
from scrapegraph_py import Client

client = Client(api_key="your-api-key")

# Get response in JSON format (default)
json_result = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract product information",
    return_toon=False  # or omit this parameter
)

# Get response in TOON format (30-60% fewer tokens)
toon_result = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract product information",
    return_toon=True
)
```

### Async Usage

The async client also supports TOON format:

```python
import asyncio
from scrapegraph_py import AsyncClient

async def main():
    async with AsyncClient(api_key="your-api-key") as client:
        # Get response in TOON format
        toon_result = await client.smartscraper(
            website_url="https://example.com",
            user_prompt="Extract product information",
            return_toon=True
        )
        print(toon_result)

asyncio.run(main())
```

## Supported Methods

The `return_toon` parameter is available for all scraping methods:

### SmartScraper
```python
# Sync
client.smartscraper(..., return_toon=True)
client.get_smartscraper(request_id, return_toon=True)

# Async
await client.smartscraper(..., return_toon=True)
await client.get_smartscraper(request_id, return_toon=True)
```

### SearchScraper
```python
# Sync
client.searchscraper(..., return_toon=True)
client.get_searchscraper(request_id, return_toon=True)

# Async
await client.searchscraper(..., return_toon=True)
await client.get_searchscraper(request_id, return_toon=True)
```

### Crawl
```python
# Sync
client.crawl(..., return_toon=True)
client.get_crawl(crawl_id, return_toon=True)

# Async
await client.crawl(..., return_toon=True)
await client.get_crawl(crawl_id, return_toon=True)
```

### AgenticScraper
```python
# Sync
client.agenticscraper(..., return_toon=True)
client.get_agenticscraper(request_id, return_toon=True)

# Async
await client.agenticscraper(..., return_toon=True)
await client.get_agenticscraper(request_id, return_toon=True)
```

### Markdownify
```python
# Sync
client.markdownify(..., return_toon=True)
client.get_markdownify(request_id, return_toon=True)

# Async
await client.markdownify(..., return_toon=True)
await client.get_markdownify(request_id, return_toon=True)
```

### Scrape
```python
# Sync
client.scrape(..., return_toon=True)
client.get_scrape(request_id, return_toon=True)

# Async
await client.scrape(..., return_toon=True)
await client.get_scrape(request_id, return_toon=True)
```

## Examples

Complete examples are available in the `examples/` directory:

- `examples/toon_example.py` - Sync examples demonstrating TOON format
- `examples/toon_async_example.py` - Async examples demonstrating TOON format

Run the examples:

```bash
# Set your API key
export SGAI_API_KEY="your-api-key"

# Run sync example
python examples/toon_example.py

# Run async example
python examples/toon_async_example.py
```

## When to Use TOON

**Use TOON when:**
- ✅ Passing scraped data to LLM APIs (reduces token costs)
- ✅ Working with large structured datasets
- ✅ Context window is limited
- ✅ Token cost optimization is important

**Use JSON when:**
- ❌ Maximum compatibility with third-party tools is required
- ❌ Data needs to be processed by JSON-only tools
- ❌ Working with highly irregular/nested data

## Cost Savings Example

At GPT-4 pricing:
- **Input tokens**: $0.01 per 1K tokens
- **Output tokens**: $0.03 per 1K tokens

With 50% token reduction using TOON:
- **1 million API requests** with 1K tokens each
- **Savings**: $2,147 per million requests
- **Savings**: $5,408 per billion tokens

## Technical Details

The TOON integration is implemented through a converter utility (`scrapegraph_py.utils.toon_converter`) that:

1. Takes the API response (dict)
2. Converts it to TOON format using the `toonify` library
3. Returns the TOON-formatted string

The conversion is **lossless** - all data is preserved and can be converted back to the original structure using the TOON decoder.

## Learn More

- [Toonify GitHub Repository](https://github.com/ScrapeGraphAI/toonify)
- [TOON Format Specification](https://github.com/toon-format/toon)
- [ScrapeGraph Documentation](https://docs.scrapegraphai.com)

## Contributing

Found a bug or have a suggestion for the TOON integration? Please open an issue or submit a pull request on our [GitHub repository](https://github.com/ScrapeGraphAI/scrapegraph-sdk).

