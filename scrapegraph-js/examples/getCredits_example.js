import { getCredits } from 'scrapegraph-sdk';
import 'dotenv/config';

try {
    const apiKey = process.env.SGAI_APIKEY;

    const myCredit = await getCredits(apiKey);

    console.log(myCredit)
} catch (error) {
    console.error(error)
}