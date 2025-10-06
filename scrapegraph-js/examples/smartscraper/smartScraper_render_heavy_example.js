import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://example.com';
const prompt = 'Find the CEO of company X and their contact details';

try {
  const response = await smartScraper(
    apiKey,
    url,
    prompt,
    null, // schema
    null, // numberOfScrolls
    null, // totalPages
    null, // cookies
    {}, // options
    false, // plain_text
    true // renderHeavyJs - Enable heavy JavaScript rendering
  );
  console.log(response);
} catch (error) {
  console.error(error);
}