/**
 * Schema-based SearchScraper Example
 *
 * This example demonstrates both schema-based output and configurable website limits:
 * - Default: 3 websites (30 credits)
 * - Enhanced: 5 websites (50 credits) - provides more comprehensive data for schema
 * - Maximum: 20 websites (200 credits) - for highly detailed schema population
 */

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

// Configure number of websites for better schema population
const numResults = 5; // Enhanced search for better schema data (50 credits)

try {
  console.log(`🔍 Searching ${numResults} websites with custom schema`);
  console.log(`💳 Credits required: ${numResults <= 3 ? 30 : 30 + (numResults - 3) * 10}`);
  console.log('-'.repeat(60));

  const response = await searchScraper(apiKey, prompt, numResults, schema);

  console.log('✅ Schema-based search completed successfully!');
  console.log('\n📋 STRUCTURED RESULT:');
  console.log(JSON.stringify(response.result, null, 2));

  console.log('\n🔗 Reference URLs:');
  response.reference_urls?.forEach((url, index) => {
    console.log(`${index + 1}. ${url}`);
  });

} catch (error) {
  console.error('❌ Error:', error.message);
}
