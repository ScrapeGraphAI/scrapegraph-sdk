# ScrapeGraph JS SDK

A JavaScript SDK for interacting with the ScrapeGraph AI API. This SDK provides easy-to-use functions for web scraping, managing credits, and submitting feedback.

## Installation

Install the package using npm:

```bash
npm install scrapegraph-js
```

## Usage

> [!WARNING]  
> Remember not to write API keys directly in the code; instead, store them securely in `.env` files.

First, import the required functions:

```javascript
import { smartScraper, getSmartScraperRequest, getCredits, sendFeedback } from 'scrapegraph-sdk';
```

### Scraping Websites

#### Basic scraping

```javascript
import { smartScraper } from 'scrapegraph-sdk';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com';
const prompt = 'What does the company do?';

try {
  const response = await smartScraper(apiKey, url, prompt);
  console.log(response);
} catch (error) {
  console.error(error);
}
```

#### Scraping with custom output schema

```javascript
import { smartScraper } from 'scrapegraph-sdk';

const apiKey = 'your_api_key';
const url = 'https://scrapegraphai.com';
const prompt = 'What does the company do?';
const schema = //TODO

try {
  const response = await smartScraper(apiKey, url, prompt, schema);
  console.log(response);
} catch (error) {
  console.error(error);
}
```

### Checking Credits

```javascript
import { getCredist } from 'scrapegraph-sdk';

const apiKey = 'your_api_key';

try {
	const myCredit = await getCredits(apiKey);
	console.log(myCredit)
} catch (error) {
	console.error(error)
}
```

### Submitting Feedback

```javascript
import { sendFeedback } from 'scrapegraph-sdk';

const apiKey = 'your_api_key';
const requestId = '16a63a80-c87f-4cde-b005-e6c3ecda278b';
const rating = 5;
const feedbackMessage = 'This is a test feedback message.';

try {
  const feedback_response = await sendFeedback(apiKey, requestId, rating, feedbackMessage);
  console.log(feedback_response);
} catch (error) {
  console.error(error)
}
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
- `feedbackText` (string) (optional): Feedback message

## Error Handling

All functions return javascript `Error` object with imformation. In case of errors, the response will include error details:

// TODO error list

```javascript
{
  "statusCode": 400,
  "title": "HTTP error occurred"
  "details": "Error details",
  
}
```

## License

MIT

## Support

For support, please visit [ScrapeGraph AI Documentation](https://sgai-api.onrender.com/docs).




