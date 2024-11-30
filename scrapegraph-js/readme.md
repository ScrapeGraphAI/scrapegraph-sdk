# 🌐 ScrapeGraph JavaScript SDK

[![npm version](https://badge.fury.io/js/scrapegraph-js.svg)](https://badge.fury.io/js/scrapegraph-js)  
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)  
[![Build Status](https://github.com/ScrapeGraphAI/scrapegraph-sdk/actions/workflows/ci.yml/badge.svg)](https://github.com/ScrapeGraphAI/scrapegraph-sdk/actions)  
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.scrapegraphai.com)

Official JavaScript/TypeScript SDK for the ScrapeGraph AI API - Smart web scraping powered by AI.

## 🚀 Features

- ✨ Smart web scraping with AI  
- 🔄 Fully asynchronous design 
- 🔍 Detailed error handling  
- ⚡ Automatic retries and logging  
- 🔐 Secure API authentication  

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
import 'dotenv/config';

const apiKey = 'your-api-key';
const url = 'https://scrapegraphai.com/';
const prompt = 'What does the company do? and ';

const schema = z.object({
  title: z.string().describe('The title of the webpage'),
  description: z.string().describe('The description of the webpage'),
  summary: z.string().describe('A brief summary of the webpage')
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
- [Documentation](https://scrapegraphai.com/documentation)  
- [GitHub](https://github.com/ScrapeGraphAI/scrapegraph-sdk)  

## 💬 Support

- 📧 Email: support@scrapegraphai.com  
- 💻 GitHub Issues: [Create an issue](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues)  
- 🌟 Feature Requests: [Request a feature](https://github.com/ScrapeGraphAI/scrapegraph-sdk/issues/new)

---

Made with ❤️ by [ScrapeGraph AI](https://scrapegraphai.com)
