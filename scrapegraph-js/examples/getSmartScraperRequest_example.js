import { getSmartScraperRequest } from "scrapegraph-sdk";
import 'dotenv/config';

try {
  const apiKey = process.env.SGAI_APIKEY;
  const requestId = '3fa85f64-5717-4562-b3fc-2c963f66afa6'

  const requestInfo = await getSmartScraperRequest(apiKey, requestId);

  console.log(requestInfo);
} catch (error) {
  console.error(error);
}