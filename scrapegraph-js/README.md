# 🌐 ScrapeGraph JavaScript SDK

[![npm version](https://badge.fury.io/js/scrapegraph-js.svg)](https://badge.fury.io/js/scrapegraph-js) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) [![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.scrapegraphai.com)

<p align="left">
  <img src="https://raw.githubusercontent.com/VinciGit00/Scrapegraph-ai/main/docs/assets/api-banner.png" alt="ScrapeGraph API Banner" style="width: 70%;">
</p>

Official JavaScript/TypeScript SDK for the ScrapeGraph AI API - Smart web scraping powered by AI.

## 🚀 Features

- ✨ Smart web scraping with AI
- 🔄 Fully asynchronous design
- 🔍 Detailed error handling
- ⚡ Automatic retries and logging
- 🔐 Secure API authentication
- 🔧 AI-powered schema generation

## 📦 Installation

Install the package using npm or yarn:

```bash
# Using npm
npm i scrapegraph-js

# Using yarn
yarn add scrapegraph-js
```

## 🔧 Quick Start

> **Note**: Store your API keys securely in environment variables. Use `.env` files and libraries like `dotenv` to load them into your app.

### Basic Example

```javascript
import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

// Initialize variables
const apiKey = process.env.SGAI_APIKEY; // Set your API key as an environment variable
const websiteUrl = 'https://example.com';
const prompt = 'What does the company do?';

(async () => {
  try {
    const response = await smartScraper(apiKey, websiteUrl, prompt);
    console.log(response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

## 🎯 Examples

### Scraping Websites

#### Basic Scraping

```javascript
import { smartScraper } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const url = 'https://example.com';
const prompt = 'Extract the main heading and description.';

(async () => {
  try {
    const response = await smartScraper(apiKey, url, prompt);
    console.log(response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

#### Scraping with Custom Output Schema

> [!NOTE]
> To use this feature, it is necessary to employ the [Zod](https://www.npmjs.com/package/zod) package for schema creation.

Here is a real-world example:

```javascript
import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';

const apiKey = 'your-api-key';
const url = 'https://scrapegraphai.com/';
const prompt = 'What does the company do? and ';

const schema = z.object({
  title: z.string().describe('The title of the webpage'),
  description: z.string().describe('The description of the webpage'),
  summary: z.string().describe('A brief summary of the webpage'),
});

(async () => {
  try {
    const response = await smartScraper(apiKey, url, prompt, schema);
    console.log(response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

#### Scraping with Infinite Scrolling

For websites that load content dynamically through infinite scrolling (like social media feeds), you can use the `numberOfScrolls` parameter:

```javascript
import { smartScraper } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const url = 'https://example.com/infinite-scroll-page';
const prompt = 'Extract all the posts from the feed';
const numberOfScrolls = 10; // Will scroll 10 times to load more content

(async () => {
  try {
    const response = await smartScraper(apiKey, url, prompt, null, numberOfScrolls);
    console.log('Extracted data from scrolled page:', response);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

The `numberOfScrolls` parameter accepts values between 0 and 100, allowing you to control how many times the page should be scrolled before extraction.

#### Scraping with Cookies

Use cookies for authentication and session management when scraping websites that require login or have user-specific content:

```javascript
import { smartScraper } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const url = 'https://example.com/dashboard';
const prompt = 'Extract user profile information';

// Define cookies for authentication
const cookies = {
  session_id: 'abc123def456',
  auth_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
  user_preferences: 'dark_mode,usd'
};

(async () => {
  try {
    const response = await smartScraper(apiKey, url, prompt, null, null, null, cookies);
    console.log(response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

**Common Use Cases:**
- **E-commerce sites**: User authentication, shopping cart persistence
- **Social media**: Session management, user preferences
- **Banking/Financial**: Secure authentication, transaction history
- **News sites**: User preferences, subscription content
- **API endpoints**: Authentication tokens, API keys

#### Advanced Scraping with Cookies, Scrolling, and Pagination

Combine cookies with infinite scrolling and pagination for comprehensive data extraction:

```javascript
import { smartScraper } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const url = 'https://example.com/feed';
const prompt = 'Extract all posts from the feed';
const cookies = { session_token: 'xyz789abc123' };
const numberOfScrolls = 10; // Scroll 10 times
const totalPages = 5; // Scrape 5 pages

(async () => {
  try {
    const response = await smartScraper(apiKey, url, prompt, null, numberOfScrolls, totalPages, cookies);
    console.log('Extracted data:', response);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

### Search Scraping

Search and extract information from multiple web sources using AI.

```javascript
import { searchScraper } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const prompt = 'What is the latest version of Python and what are its main features?';

(async () => {
  try {
    const response = await searchScraper(apiKey, prompt);
    console.log(response.result);
  } catch (error) {
    console.error('Error:', error);
  }
})();
```

### Crawl API

Start a crawl job to extract structured data from a website and its linked pages, using a custom schema.

```javascript
import { crawl, getCrawlRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com/';
const prompt = 'What does the company do? and I need text content from there privacy and terms';

const schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ScrapeGraphAI Website Content",
  "type": "object",
  "properties": {
    "company": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "description": { "type": "string" },
        "features": { "type": "array", "items": { "type": "string" } },
        "contact_email": { "type": "string", "format": "email" },
        "social_links": {
          "type": "object",
          "properties": {
            "github": { "type": "string", "format": "uri" },
            "linkedin": { "type": "string", "format": "uri" },
            "twitter": { "type": "string", "format": "uri" }
          },
          "additionalProperties": false
        }
      },
      "required": ["name", "description"]
    },
    "services": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "service_name": { "type": "string" },
          "description": { "type": "string" },
          "features": { "type": "array", "items": { "type": "string" } }
        },
        "required": ["service_name", "description"]
      }
    },
    "legal": {
      "type": "object",
      "properties": {
        "privacy_policy": { "type": "string" },
        "terms_of_service": { "type": "string" }
      },
      "required": ["privacy_policy", "terms_of_service"]
    }
  },
  "required": ["company", "services", "legal"]
};

(async () => {
  try {
    // Start the crawl job
    const crawlResponse = await crawl(apiKey, url, prompt, schema, {
      cacheWebsite: true,
      depth: 2,
      maxPages: 2,
      sameDomainOnly: true,
      batchSize: 1,
    });
    console.log('Crawl job started. Response:', crawlResponse);

    // If the crawl is asynchronous and returns an ID, fetch the result
    const crawlId = crawlResponse.id || crawlResponse.task_id;
    if (crawlId) {
      for (let i = 0; i < 10; i++) {
        await new Promise((resolve) => setTimeout(resolve, 5000));
        const result = await getCrawlRequest(apiKey, crawlId);
        if (result.status === 'success' && result.result) {
          console.log('Crawl completed. Result:', result.result.llm_result);
          break;
        } else if (result.status === 'failed') {
          console.log('Crawl failed. Result:', result);
          break;
        } else {
          console.log(`Status: ${result.status}, waiting...`);
        }
      }
    } else {
      console.log('No crawl ID found in response. Synchronous result:', crawlResponse);
    }
  } catch (error) {
    console.error('Error occurred:', error);
  }
})();
```

You can use a plain JSON schema or a [Zod](https://www.npmjs.com/package/zod) schema for the `schema` parameter. The crawl API supports options for crawl depth, max pages, domain restriction, and batch size.

### Scraping local HTML

Extract structured data from local HTML content

```javascript
import { localScraper } from 'scrapegraph-js';

const apiKey = 'your_api_key';
const prompt = 'What does the company do?';

const websiteHtml = `<html>
                      <body>
                        <h1>Company Name</h1>
                        <p>We are a technology company focused on AI solutions.</p>
                        <div class="contact">
                          <p>Email: contact@example.com</p>
                        </div>
                      </body>
                    </html>`;
(async () => {
  try {
    const response = await localScraper(apiKey, websiteHtml, prompt);
    console.log(response);
  } catch (error) {
    console.error(error);
  }
})();
```

### Markdownify

Converts a webpage into clean, well-structured markdown format.

```javascript
import { smartScraper } from 'scrapegraph-js';

const apiKey = 'your_api_key';
const url = 'https://scrapegraphai.com/';

(async () => {
  try {
    const response = await markdownify(apiKey, url);
    console.log(response);
  } catch (error) {
    console.error(error);
  }
})();
```

### Checking API Credits

```javascript
import { getCredits } from 'scrapegraph-js';

const apiKey = 'your-api-key';

(async () => {
  try {
    const credits = await getCredits(apiKey);
    console.log('Available credits:', credits);
  } catch (error) {
    console.error('Error fetching credits:', error);
  }
})();
```

### Submitting Feedback

```javascript
import { sendFeedback } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const requestId = '16a63a80-c87f-4cde-b005-e6c3ecda278b';
const rating = 5;
const feedbackText = 'This is a test feedback message.';

(async () => {
  try {
    const response = await sendFeedback(apiKey, requestId, rating, feedbackText);
    console.log('Feedback response:', response);
  } catch (error) {
    console.error('Error sending feedback:', error);
  }
})();
```

### AI-Powered Schema Generation

Generate JSON schemas from natural language prompts using AI. This feature helps you create structured data schemas for web scraping and data extraction.

#### Basic Schema Generation

```javascript
import { generateSchema } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const prompt = 'Find laptops with specifications like brand, processor, RAM, storage, and price';

(async () => {
  try {
    const response = await generateSchema(prompt, null, { apiKey });
    console.log('Generated schema:', response.generated_schema);
    console.log('Request ID:', response.request_id);
  } catch (error) {
    console.error('Error generating schema:', error);
  }
})();
```

#### Modifying Existing Schemas

```javascript
import { generateSchema } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const existingSchema = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    price: { type: 'number' }
  },
  required: ['name', 'price']
};

const modificationPrompt = 'Add brand and rating fields to the existing schema';

(async () => {
  try {
    const response = await generateSchema(modificationPrompt, existingSchema, { apiKey });
    console.log('Modified schema:', response.generated_schema);
  } catch (error) {
    console.error('Error modifying schema:', error);
  }
})();
```

#### Checking Schema Generation Status

```javascript
import { getSchemaStatus } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const requestId = '123e4567-e89b-12d3-a456-426614174000';

(async () => {
  try {
    const response = await getSchemaStatus(requestId, { apiKey });
    console.log('Status:', response.status);
    if (response.status === 'completed') {
      console.log('Generated schema:', response.generated_schema);
    }
  } catch (error) {
    console.error('Error checking status:', error);
  }
})();
```

#### Polling for Completion with Progress Tracking

```javascript
import { pollSchemaGeneration } from 'scrapegraph-js';

const apiKey = 'your-api-key';
const requestId = '123e4567-e89b-12d3-a456-426614174000';

(async () => {
  try {
    const finalResult = await pollSchemaGeneration(requestId, {
      apiKey,
      maxAttempts: 15,
      delay: 3000,
      onProgress: ({ attempt, maxAttempts, status, response }) => {
        if (status === 'checking') {
          console.log(`Checking status... (${attempt}/${maxAttempts})`);
        } else {
          console.log(`Status: ${status} (${attempt}/${maxAttempts})`);
        }
      }
    });
    
    console.log('Schema generation completed!');
    console.log('Final schema:', finalResult.generated_schema);
  } catch (error) {
    console.error('Error during polling:', error);
  }
})();
```

## 📚 Documentation

For detailed documentation, visit [docs.scrapegraphai.com](https://docs.scrapegraphai.com)

## 🛠️ Development

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ScrapeGraphAI/scrapegraph-sdk.git
   cd scrapegraph-sdk/scrapegraph-js
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Run linting and testing:
   ```bash
   npm run lint
   npm test
   ```

### Running Tests

```bash
# Run all tests
npm test

# Run tests with coverage
npm run test:coverage
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
- [GitHub](https://github.com/ScrapeGraphAI/scrapegraph-sdk)

## 💬 Support

- 📧 Email: support@scrapegraphai.com
- 💻 GitHub Issues: [Create an issue](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues)
- 🌟 Feature Requests: [Request a feature](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/new)

---

Made with ❤️ by [ScrapeGraph AI](https://scrapegraphai.com)
