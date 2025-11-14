import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
// Example URL that requires scrolling (e.g., a social media feed or infinite scroll page)
const url = 'https://example.com/infinite-scroll-page';
const prompt = 'Extract all the posts from the feed';
const numberOfScrolls = 10; // Will scroll 10 times to load more content

try {
  const response = await smartScraper(apiKey, url, prompt, null, numberOfScrolls);
  console.log('Extracted data from scrolled page:', response);
} catch (error) {
  console.error('Error:', error);
}
