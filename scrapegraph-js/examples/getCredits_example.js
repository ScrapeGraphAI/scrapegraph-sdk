import { getCredits } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

try {
  const myCredit = await getCredits(apiKey);
  console.log(myCredit);
} catch (error) {
  console.error(error);
}
