import { getAgenticScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
// Replace this with an actual request ID from a previous agenticScraper call
const requestId = 'your-request-id-here';

try {
  const response = await getAgenticScraperRequest(apiKey, requestId);
  
  console.log('🔍 Agentic Scraper Request Status');
  console.log('Request ID:', requestId);
  console.log('Status:', response.status);
  console.log('Created At:', response.created_at);
  
  if (response.status === 'completed') {
    console.log('✅ Automation Completed!');
    console.log('Completed At:', response.completed_at);
    console.log('Result:', JSON.stringify(response.result, null, 2));
  } else if (response.status === 'pending') {
    console.log('⏳ Automation is still in progress...');
    console.log('Please check again in a few moments.');
  } else if (response.status === 'failed') {
    console.log('❌ Automation Failed');
    console.log('Error:', response.error);
  }
  
  console.log('\nFull Response:', JSON.stringify(response, null, 2));
} catch (error) {
  console.error('❌ Error:', error.message);
}
