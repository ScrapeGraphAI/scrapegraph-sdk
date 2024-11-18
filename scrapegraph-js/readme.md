# ScrapeGraph JS SDK

A JavaScript SDK for interacting with the ScrapeGraph AI API. This SDK provides easy-to-use functions for web scraping, managing credits, and submitting feedback.

## Installation

Install the package using npm:

```bash
npm install scrapegraph-js
```

## Usage

First, import the required functions:

```javascript
import { scrape, credits, feedback } from 'scrapegraph-js';
```

### Scraping Websites

```javascript
const apiKey = 'your_api_key';
const url = 'https://example.com';

// Basic scraping
const result = await scrape(apiKey, url);
console.log(JSON.parse(result));

// Scraping with custom options
const options = {
  elements: ['h1', '.product-price'],
  wait_for: '.specific-element',
  javascript: true
};

const customResult = await scrape(apiKey, url, options);
console.log(JSON.parse(customResult));
```

### Checking Credits

```javascript
const apiKey = 'your_api_key';

const creditsInfo = await credits(apiKey);
console.log(JSON.parse(creditsInfo));
```

### Submitting Feedback

```javascript
const apiKey = 'your_api_key';
const requestId = 'request_id_from_scrape_response';
const rating = 5;
const feedbackText = 'Great results!';

const feedbackResponse = await feedback(apiKey, requestId, rating, feedbackText);
console.log(JSON.parse(feedbackResponse));
```

## API Reference

### scrape(apiKey, url[, options])

Scrapes a website and returns the extracted data.

Parameters:
- `apiKey` (string): Your ScrapeGraph AI API key
- `url` (string): The URL to scrape
- `options` (object, optional):
  - `elements` (array): Specific elements to extract
  - `wait_for` (string): CSS selector to wait for before scraping
  - `javascript` (boolean): Enable JavaScript rendering

### credits(apiKey)

Retrieves your current credit balance.

Parameters:
- `apiKey` (string): Your ScrapeGraph AI API key

### feedback(apiKey, requestId, rating, feedbackText)

Submits feedback for a scraping request.

Parameters:
- `apiKey` (string): Your ScrapeGraph AI API key
- `requestId` (string): The request ID from the scrape response
- `rating` (number): Rating score
- `feedbackText` (string): Feedback message

## Error Handling

All functions return JSON strings that you should parse. In case of errors, the response will include error details:

```javascript
{
  "error": "HTTP error occurred",
  "message": "Error details",
  "status_code": 400
}
```

## License

MIT

## Support

For support, please visit [ScrapeGraph AI Documentation](https://sgai-api.onrender.com/docs).




