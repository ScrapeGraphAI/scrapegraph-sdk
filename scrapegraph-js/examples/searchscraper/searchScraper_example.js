/**
 * Basic SearchScraper Example
 *
 * This example demonstrates the configurable website limits feature:
 * - Default: 3 websites (30 credits)
 * - Enhanced: 5 websites (50 credits) - uncomment to try
 * - Maximum: 20 websites (200 credits) - for comprehensive research
 */

import { searchScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const prompt = 'What is the latest version of Python and what are its main features?';

// Configure the number of websites to search
const numResults = 3; // Default: 3 websites (30 credits)
// const numResults = 5; // Enhanced: 5 websites (50 credits) - uncomment for more comprehensive results
// const numResults = 10; // Deep research: 10 websites (100 credits) - uncomment for extensive research

try {
  console.log(`🔍 Searching ${numResults} websites for: ${prompt}`);
  console.log(`💳 Credits required: ${numResults <= 3 ? 30 : 30 + (numResults - 3) * 10}`);
  console.log('-'.repeat(60));

  const response = await searchScraper(apiKey, prompt, numResults);

  console.log('✅ Search completed successfully!');
  console.log('\n📋 RESULTS:');
  console.log(`Result: ${response.result}`);
  console.log('\n🔗 Reference URLs:');
  response.reference_urls?.forEach((url, index) => {
    console.log(`${index + 1}. ${url}`);
  });

} catch (error) {
  console.error('❌ Error:', error.message);
}
