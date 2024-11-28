import { smartScraper } from 'scrapegraph-sdk';
import 'dotenv/config';

try {
  const apiKey = process.env.SGAI_APIKEY;
  const url = 'https://scrapegraphai.com';
  const prompt = 'What does the company do?';

  const response = await smartScraper(apiKey, url, prompt);

  console.log(response);
} catch (error) {
  console.error(error);
}
