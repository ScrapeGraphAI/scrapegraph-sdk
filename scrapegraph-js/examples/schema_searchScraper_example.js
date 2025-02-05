import { searchScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const prompt = 'What is the latest version of Python and what are its main features?';

const schema = z.object({
  version: z.string().describe('The latest version'),
  release_date: z.string().describe('The release date of latest version'),
  major_features: z.array(z.string()),
});

try {
  const response = await searchScraper(apiKey, prompt, schema);
  console.log(response.result);
} catch (error) {
  console.error(error);
}
