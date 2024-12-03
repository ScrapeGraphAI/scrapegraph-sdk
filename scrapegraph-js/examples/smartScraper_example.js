import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com';
const prompt = 'What does the company do?';

try {
  const response = await smartScraper(apiKey, url, prompt);
  console.log(response);
} catch (error) {
  console.error(error);
}
