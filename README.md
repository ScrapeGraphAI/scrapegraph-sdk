# 🌐 ScrapeGraph AI SDKs

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python SDK](https://img.shields.io/badge/Python_SDK-Latest-blue)](https://github.com/ScrapeGraphAI/scrapegraph-sdk/tree/main/scrapegraph-py)
[![JavaScript SDK](https://img.shields.io/badge/JavaScript_SDK-Latest-yellow)](https://github.com/ScrapeGraphAI/scrapegraph-sdk/tree/main/scrapegraph-js)
[![Documentation](https://img.shields.io/badge/Documentation-Latest-green)](https://docs.scrapegraphai.com)

Official SDKs for the ScrapeGraph AI API - Intelligent web scraping and search powered by AI. Extract structured data from any webpage or perform AI-powered web searches with natural language prompts.

Get your [API key](https://scrapegraphai.com)!
[![API Banner](https://raw.githubusercontent.com/ScrapeGraphAI/Scrapegraph-ai/main/docs/assets/api_banner.png)](https://scrapegraphai.com/?utm_source=github&utm_medium=readme&utm_campaign=api_banner&utm_content=api_banner_image)

## Features

- 🤖 **SmartScraper**: Extract structured data from webpages using natural language prompts
- 🔍 **SearchScraper**: AI-powered web search with structured results and reference URLs
- 📝 **Markdownify**: Convert any webpage into clean, formatted markdown
- 🕷️ **SmartCrawler**: Intelligently crawl and extract data from multiple pages
- 🤖 **AgenticScraper**: Perform automated browser actions with AI-powered session management
- 📄 **Scrape**: Convert webpages to HTML with JavaScript rendering and custom headers
- ⏰ **Scheduled Jobs**: Create and manage automated scraping workflows with cron scheduling
- 💳 **Credits Management**: Monitor API usage and credit balance
- 💬 **Feedback System**: Provide ratings and feedback to improve service quality

## 🚀 Quick Links
ScrapeGraphAI offers seamless integration with popular frameworks and tools to enhance your scraping capabilities. Whether you're building with Python or Node.js, using LLM frameworks, or working with no-code platforms, we've got you covered with our comprehensive integration options..

You can find more informations at the following [link](https://scrapegraphai.com)

**Integrations**:

- **API**: [Documentation](https://docs.scrapegraphai.com/introduction)
- **SDKs**: [Python](https://docs.scrapegraphai.com/sdks/python), [Node](https://docs.scrapegraphai.com/sdks/javascript)
- **LLM Frameworks**: [Langchain](https://docs.scrapegraphai.com/integrations/langchain), [Llama Index](https://docs.scrapegraphai.com/integrations/llamaindex), [Crew.ai](https://docs.scrapegraphai.com/integrations/crewai), [CamelAI](https://github.com/camel-ai/camel)
- **Low-code Frameworks**: [Pipedream](https://pipedream.com/apps/scrapegraphai), [Bubble](https://bubble.io/plugin/scrapegraphai-1745408893195x213542371433906180), [Zapier](https://zapier.com/apps/scrapegraphai/integrations), [n8n](http://localhost:5001/dashboard), [LangFlow](https://www.langflow.org)
- **MCP server**:  [Link](https://smithery.ai/server/@ScrapeGraphAI/scrapegraph-mcp)

## 📦 Installation

### Python
```bash
pip install scrapegraph-py
```

### JavaScript
```bash
npm install scrapegraph-js
```

## 🎯 Core Features

- 🤖 **AI-Powered Extraction & Search**: Use natural language to extract data or search the web
- 📊 **Structured Output**: Get clean, structured data with optional schema validation
- 🔄 **Multiple Formats**: Extract data as JSON, Markdown, or custom schemas
- ⚡ **High Performance**: Concurrent processing and automatic retries
- 🔒 **Enterprise Ready**: Production-grade security and rate limiting

## 🛠️ Available Endpoints

### 🤖 SmartScraper
Using AI to extract structured data from any webpage or HTML content with natural language prompts.

**Example Usage:**

**Python:**
```python
from scrapegraph_py import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Client(api_key=os.getenv("SGAI_API_KEY"))

# Extract data from a webpage
response = client.smartscraper(
    website_url="https://example.com",
    user_prompt="Extract the main heading, description, and summary of the webpage",
)

print(f"Request ID: {response['request_id']}")
print(f"Result: {response['result']}")

client.close()
```

**JavaScript:**
```javascript
import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com';
const prompt = 'Extract the main heading, description, and summary of the webpage';

try {
  const response = await smartScraper(apiKey, url, prompt);
  console.log(response);
} catch (error) {
  console.error(error);
}
```

### 🔍 SearchScraper
Perform AI-powered web searches with structured results and reference URLs.

**Example Usage:**

**Python:**
```python
from scrapegraph_py import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Client(api_key=os.getenv("SGAI_API_KEY"))

# Perform AI-powered web search
response = client.searchscraper(
    user_prompt="What is the latest version of Python and what are its main features?",
    num_results=3,  # Number of websites to search (default: 3)
)

print(f"Result: {response['result']}")
print("\nReference URLs:")
for url in response["reference_urls"]:
    print(f"- {url}")

client.close()
```

**JavaScript:**
```javascript
import { searchScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const prompt = 'What is the latest version of Python and what are its main features?';

try {
  const response = await searchScraper(apiKey, prompt, 3); // 3 websites
  console.log('Result:', response.result);
  console.log('\nReference URLs:');
  response.reference_urls?.forEach(url => console.log(`- ${url}`));
} catch (error) {
  console.error(error);
}
```

### 📝 Markdownify
Convert any webpage into clean, formatted markdown.

**Example Usage:**

**Python:**
```python
from scrapegraph_py import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Client(api_key=os.getenv("SGAI_API_KEY"))

# Convert webpage to markdown
response = client.markdownify(
    website_url="https://example.com",
)

print(f"Request ID: {response['request_id']}")
print(f"Markdown: {response['result']}")

client.close()
```

**JavaScript:**
```javascript
import { markdownify } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com';

try {
  const response = await markdownify(apiKey, url);
  console.log(response);
} catch (error) {
  console.error(error);
}
```

### 🕷️ SmartCrawler
Intelligently crawl and extract data from multiple pages with configurable depth and batch processing.

**Example Usage:**

**Python:**
```python
from scrapegraph_py import Client
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Client(api_key=os.getenv("SGAI_API_KEY"))

# Start crawl job
crawl_response = client.crawl(
    url="https://example.com",
    prompt="Extract page titles and main headings",
    data_schema={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "headings": {"type": "array", "items": {"type": "string"}}
        }
    },
    depth=2,
    max_pages=5,
    same_domain_only=True,
)

crawl_id = crawl_response.get("id") or crawl_response.get("task_id")

# Poll for results
if crawl_id:
    for _ in range(10):
        time.sleep(5)
        result = client.get_crawl(crawl_id)
        if result.get("status") == "success":
            print("Crawl completed:", result["result"]["llm_result"])
            break

client.close()
```

**JavaScript:**
```javascript
import { crawl, getCrawlRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com';
const prompt = 'Extract page titles and main headings';
const schema = {
  type: "object",
  properties: {
    title: { type: "string" },
    headings: { type: "array", items: { type: "string" } }
  }
};

try {
  const crawlResponse = await crawl(apiKey, url, prompt, schema, {
    depth: 2,
    maxPages: 5,
    sameDomainOnly: true,
  });

  const crawlId = crawlResponse.id || crawlResponse.task_id;
  
  // Poll for results
  if (crawlId) {
    for (let i = 0; i < 10; i++) {
      await new Promise(resolve => setTimeout(resolve, 5000));
      const result = await getCrawlRequest(apiKey, crawlId);
      if (result.status === 'success') {
        console.log('Crawl completed:', result.result.llm_result);
        break;
      }
    }
  }
} catch (error) {
  console.error(error);
}
```

### 🤖 AgenticScraper
Perform automated browser actions on webpages using AI-powered agentic scraping with session management.

**Example Usage:**

**Python:**
```python
from scrapegraph_py import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Client(api_key=os.getenv("SGAI_API_KEY"))

# Perform automated browser actions
response = client.agenticscraper(
    url="https://example.com",
    use_session=True,
    steps=[
        "Type email@gmail.com in email input box",
        "Type password123 in password inputbox",
        "click on login"
    ],
    ai_extraction=False  # Set to True for AI extraction
)

print(f"Request ID: {response['request_id']}")
print(f"Status: {response.get('status')}")

# Get results
result = client.get_agenticscraper(response['request_id'])
print(f"Result: {result.get('result')}")

client.close()
```

**JavaScript:**
```javascript
import { agenticScraper, getAgenticScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com';
const steps = [
  'Type email@gmail.com in email input box',
  'Type password123 in password inputbox',
  'click on login'
];

try {
  const response = await agenticScraper(apiKey, url, steps, true);
  console.log('Request ID:', response.request_id);
  
  // Get results
  const result = await getAgenticScraperRequest(apiKey, response.request_id);
  console.log('Status:', result.status);
  console.log('Result:', result.result);
} catch (error) {
  console.error(error);
}
```

### 📄 Scrape
Convert webpages into HTML format with optional JavaScript rendering and custom headers.

**Example Usage:**

**Python:**
```python
from scrapegraph_py import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the client
client = Client(api_key=os.getenv("SGAI_API_KEY"))

# Get HTML content from webpage
response = client.scrape(
    website_url="https://example.com",
    render_heavy_js=False,  # Set to True for JavaScript-heavy sites
)

print(f"Request ID: {response['request_id']}")
print(f"HTML length: {len(response.get('html', ''))} characters")

client.close()
```

**JavaScript:**
```javascript
import { scrape } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com';

try {
  const response = await scrape(apiKey, url, {
    renderHeavyJs: false,  // Set to true for JavaScript-heavy sites
    headers: { 'User-Agent': 'Custom Agent' }
  });
  console.log('HTML length:', response.html?.length, 'characters');
} catch (error) {
  console.error(error);
}
```

### ⏰ Scheduled Jobs
Create, manage, and monitor scheduled scraping jobs with cron expressions and execution history.

### 💳 Credits
Check your API credit balance and usage.

### 💬 Feedback
Send feedback and ratings for scraping requests to help improve the service.

## 🌟 Key Benefits

- 📝 **Natural Language Queries**: No complex selectors or XPath needed
- 🎯 **Precise Extraction**: AI understands context and structure
- 🔄 **Adaptive Processing**: Works with both web content and direct HTML
- 📊 **Schema Validation**: Ensure data consistency with Pydantic/TypeScript
- ⚡ **Async Support**: Handle multiple requests efficiently
- 🔍 **Source Attribution**: Get reference URLs for search results

## 💡 Use Cases

- 🏢 **Business Intelligence**: Extract company information and contacts
- 📊 **Market Research**: Gather product data and pricing
- 📰 **Content Aggregation**: Convert articles to structured formats
- 🔍 **Data Mining**: Extract specific information from multiple sources
- 📱 **App Integration**: Feed clean data into your applications
- 🌐 **Web Research**: Perform AI-powered searches with structured results

## 📖 Documentation

For detailed documentation and examples, visit:
- [Python SDK Guide](scrapegraph-py/README.md)
- [JavaScript SDK Guide](scrapegraph-js/README.md)
- [API Documentation](https://docs.scrapegraphai.com)

## 💬 Support & Feedback

- 📧 Email: support@scrapegraphai.com
- 💻 GitHub Issues: [Create an issue](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues)
- 🌟 Feature Requests: [Request a feature](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/new)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by [ScrapeGraph AI](https://scrapegraphai.com)
