# SmartScraper Pagination

This document describes the pagination functionality added to the ScrapeGraph JavaScript SDK.

## Overview

The `smartScraper` function now supports pagination, allowing you to scrape multiple pages of content in a single request. This is particularly useful for e-commerce sites, search results, news feeds, and other paginated content.

## Usage

### Basic Pagination

```javascript
import { smartScraper } from 'scrapegraph-js';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com/products';
const prompt = 'Extract all product information';
const totalPages = 5; // Scrape 5 pages

const result = await smartScraper(apiKey, url, prompt, null, null, totalPages);
```

### Pagination with Schema

```javascript
import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';

const ProductSchema = z.object({
  products: z.array(z.object({
    name: z.string(),
    price: z.string(),
    rating: z.string().optional(),
  })),
});

const result = await smartScraper(
  apiKey,
  url,
  prompt,
  ProductSchema,
  null,
  3 // 3 pages
);
```

### Pagination with Scrolling

```javascript
const result = await smartScraper(
  apiKey,
  url,
  prompt,
  null,
  10, // 10 scrolls per page
  2   // 2 pages
);
```

### All Features Combined

```javascript
const result = await smartScraper(
  apiKey,
  url,
  prompt,
  ProductSchema,
  5, // numberOfScrolls
  3  // totalPages
);
```

## Function Signature

```javascript
smartScraper(apiKey, url, prompt, schema, numberOfScrolls, totalPages)
```

### Parameters

- `apiKey` (string): Your ScrapeGraph AI API key
- `url` (string): The URL of the webpage to scrape
- `prompt` (string): Natural language prompt describing what data to extract
- `schema` (Object, optional): Zod schema object defining the output structure
- `numberOfScrolls` (number, optional): Number of times to scroll the page (0-100)
- `totalPages` (number, optional): Number of pages to scrape (1-10)

### Parameter Validation

- `totalPages` must be an integer between 1 and 10
- `numberOfScrolls` must be an integer between 0 and 100
- Both parameters are optional and default to `null`

## Examples

### E-commerce Product Scraping

```javascript
import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';

const ProductSchema = z.object({
  products: z.array(z.object({
    name: z.string(),
    price: z.string(),
    rating: z.string().optional(),
    image_url: z.string().optional(),
  })),
});

const result = await smartScraper(
  process.env.SGAI_APIKEY,
  'https://www.amazon.com/s?k=laptops',
  'Extract all laptop products with name, price, rating, and image',
  ProductSchema,
  null,
  5 // Scrape 5 pages of results
);
```

### News Articles Scraping

```javascript
const NewsSchema = z.object({
  articles: z.array(z.object({
    title: z.string(),
    summary: z.string(),
    author: z.string().optional(),
    date: z.string().optional(),
  })),
});

const result = await smartScraper(
  process.env.SGAI_APIKEY,
  'https://news.example.com',
  'Extract all news articles with title, summary, author, and date',
  NewsSchema,
  3, // Scroll 3 times per page
  4  // Scrape 4 pages
);
```

## Error Handling

The function will throw an error if:
- `totalPages` is not an integer between 1 and 10
- `numberOfScrolls` is not an integer between 0 and 100
- API key is invalid
- Network request fails

```javascript
try {
  const result = await smartScraper(apiKey, url, prompt, null, null, totalPages);
  console.log('Success:', result);
} catch (error) {
  if (error.message.includes('totalPages')) {
    console.error('Pagination error:', error.message);
  } else {
    console.error('Other error:', error.message);
  }
}
```

## Backward Compatibility

The pagination feature is fully backward compatible. All existing function calls will continue to work:

```javascript
// These all work as before
await smartScraper(apiKey, url, prompt);
await smartScraper(apiKey, url, prompt, schema);
await smartScraper(apiKey, url, prompt, schema, numberOfScrolls);
```

## Performance Considerations

- Pagination requests may take significantly longer than single-page requests
- Consider using smaller `totalPages` values for testing
- Some websites may not support pagination
- Rate limiting may apply for large pagination requests

## Testing

Run the pagination tests:

```bash
npm test
```

Or run specific examples:

```bash
node examples/smartScraper_pagination_example.js
node examples/smartScraper_pagination_enhanced_example.js
node examples/smartScraper_pagination_with_scroll_example.js
```

## Best Practices

1. **Start Small**: Begin with 1-2 pages for testing
2. **Use Schemas**: Define clear schemas for structured data extraction
3. **Error Handling**: Always wrap calls in try-catch blocks
4. **Rate Limiting**: Be mindful of API rate limits with large pagination requests
5. **Website Compatibility**: Not all websites support pagination - test thoroughly
6. **Performance**: Monitor request times and adjust parameters accordingly

## Troubleshooting

### Common Issues

1. **Validation Error**: Ensure `totalPages` is between 1-10
2. **Timeout**: Try reducing `totalPages` or `numberOfScrolls`
3. **No Results**: Some websites may not support pagination
4. **Rate Limiting**: Reduce request frequency or pagination size

### Debug Tips

```javascript
console.log('Starting pagination request...');
console.log('URL:', url);
console.log('Total Pages:', totalPages);
console.log('Number of Scrolls:', numberOfScrolls);

const startTime = Date.now();
const result = await smartScraper(apiKey, url, prompt, schema, numberOfScrolls, totalPages);
const duration = Date.now() - startTime;

console.log('Request completed in:', duration, 'ms');
console.log('Result type:', typeof result);
```

## Support

For issues or questions about pagination functionality:

1. Check the examples in the `examples/` directory
2. Run the test suite with `npm test`
3. Review the error messages for specific guidance
4. Check the main SDK documentation

---

*This pagination feature is designed to work with the existing ScrapeGraph AI API and maintains full backward compatibility with existing code.*
