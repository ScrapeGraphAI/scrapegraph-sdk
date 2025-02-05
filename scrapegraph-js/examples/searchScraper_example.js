import { searchScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const prompt = 'What is the latest version of Python and what are its main features?';

try {
  const response = await searchScraper(apiKey, prompt);
  console.log(response);
} catch (error) {
  console.error(error);
}
