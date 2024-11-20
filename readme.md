# ScrapeGraph SDKs

Official SDKs for interacting with the ScrapeGraph AI API - a powerful web scraping and data extraction service.

## Available SDKs

- [Python SDK (scrapegraph-py)](#python-sdk)
- [JavaScript SDK (scrapegraph-js)](#javascript-sdk)

## Python SDK

### Installation
bash
pip install scrapegraph-py
### Features

- Web Scraping (basic and structured)
- Credits checking
- Feedback submission
- API status checking
- Local HTML scraping support
- Pydantic schema integration

### Basic Usage
python
from scrapegraph_py import ScrapeGraphClient, smart_scraper
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("SCRAPEGRAPH_API_KEY")
client = ScrapeGraphClient(api_key)
url = "https://example.com"
prompt = "What does the company do?"
result = smart_scraper(client, url, prompt)
print(result)
### Structured Data with Schema
python
from pydantic import BaseModel, Field
class CompanyInfoSchema(BaseModel):
company_name: str = Field(description="The name of the company")
description: str = Field(description="A description of the company")
main_products: list[str] = Field(description="The main products of the company")
result = smart_scraper(
client=client,
url="https://example.com",
prompt="Extract company information",
schema=CompanyInfoSchema
)
bash
npm install scrapegraph-js
### Features

- Smart web scraping
- Credits management
- Feedback submission
- Schema-based extraction
- Promise-based API

### Basic Usage
javascript
import { smartScraper, credits, feedback } from 'scrapegraph-js';
const apiKey = process.env.SCRAPEGRAPH_API_KEY;
const url = 'https://example.com';
// Basic scraping
const result = await smartScraper(apiKey, url, "What does the company do?");
console.log(JSON.parse(result));
// Check credits
const creditsInfo = await credits(apiKey);
console.log(JSON.parse(creditsInfo));
### Schema-based Extraction
avascript
const schema = {
title: "CompanyInfo",
properties: {
company_name: { type: "string", description: "The name of the company" },
description: { type: "string", description: "A description of the company" },
main_products: {
type: "array",
items: { type: "string" },
description: "The main products of the company"
}
},
required: ["company_name", "description"]
};
const result = await smartScraper(apiKey, url, "Extract company information", schema);
## Authentication

Both SDKs support authentication via API key. We recommend storing your API key in environment variables:
bash
For Python
export SCRAPEGRAPH_API_KEY="your-api-key-here"
For Node.js
export SCRAPEGRAPH_API_KEY="your-api-key-here"
Or using a `.env` file:
plaintext
SCRAPEGRAPH_API_KEY="your-api-key-here"

## Error Handling

Both SDKs provide consistent error handling
json
{
"error": "HTTP error occurred",
"message": "Error details",
"status_code": 400
}

## Development

### Python SDK Requirements
- Python 3.9+
- [Rye](https://rye-up.com/) for dependency management (optional)

### JavaScript SDK Requirements
- Node.js 14+
- npm or yarn

## Contributing

We welcome contributions to both SDKs! Please check our [Contributing Guidelines](CONTRIBUTING.md) for more information.

## License

Both SDKs are licensed under the MIT License.

## Support

For support:
- Visit [ScrapeGraph AI Documentation](https://sgai-api.onrender.com/docs)
- Check the examples in the respective SDK's examples directory
- Contact our support team

## Links

- [Python SDK Documentation](https://github.com/ScrapeGraphAI/scrapegraph-sdk/tree/main/scrapegraph-py)
- [JavaScript SDK Documentation](https://github.com/ScrapeGraphAI/scrapegraph-sdk/tree/main/scrapegraph-js)
This README combines information from both SDKs and provides a comprehensive overview of their features and usage. I referenced the following code blocks for accuracy:
