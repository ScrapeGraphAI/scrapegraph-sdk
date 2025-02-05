import { getSearchScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const requestId = '64801288-6e3b-41f3-9d94-07cff3829e15';

try {
  const requestInfo = await getSearchScraperRequest(apiKey, requestId);
  console.log(requestInfo);
} catch (error) {
  console.error(error);
}
