import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com/';
const prompt = 'What does the company do? and ';

const schema = z.object({
  title: z.string().describe('The title of the webpage'),
  description: z.string().describe('The description of the webpage'),
  summary: z.string().describe('A brief summary of the webpage'),
});

try {
  const response = await smartScraper(apiKey, url, prompt, schema);
  console.log(response.result);
} catch (error) {
  console.error(error);
}
