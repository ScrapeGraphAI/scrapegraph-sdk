import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com/';
const prompt = 'What does the company do? and ';

const schema = 2;

try {
  const response = await smartScraper(apiKey, url, prompt, schema);
  console.log(response.result);
} catch (error) {
  console.error(error);
}