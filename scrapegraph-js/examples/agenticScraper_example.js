import { agenticScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://dashboard.scrapegraphai.com/';
const steps = [
  'Type email@gmail.com in email input box',
  'Type test-password@123 in password inputbox',
  'click on login'
];

try {
  const response = await agenticScraper(apiKey, url, steps, true);
  console.log('🤖 Agentic Scraper Request Submitted');
  console.log('Request ID:', response.request_id);
  console.log('Status:', response.status);
  console.log('Full Response:', JSON.stringify(response, null, 2));
} catch (error) {
  console.error('❌ Error:', error.message);
}
