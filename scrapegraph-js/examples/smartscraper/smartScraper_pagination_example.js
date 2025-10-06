import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;
const url = 'https://www.amazon.in/s?k=tv&crid=1TEF1ZFVLU8R8&sprefix=t%2Caps%2C390&ref=nb_sb_noss_2';
const prompt = 'Extract all product info including name, price, rating, and image_url';
const totalPages = 3; // Number of pages to scrape

try {
  console.log('🔍 Starting SmartScraper pagination request...');
  console.log(`🌐 URL: ${url}`);
  console.log(`📝 Prompt: ${prompt}`);
  console.log(`📄 Total Pages: ${totalPages}`);
  console.log('-'.repeat(50));

  const startTime = Date.now();

  const response = await smartScraper(apiKey, url, prompt, null, null, totalPages);

  const duration = Date.now() - startTime;

  console.log(`✅ Request completed in ${duration}ms`);
  console.log('📊 Response:', JSON.stringify(response, null, 2));

  // Check if pagination worked
  if (response && typeof response === 'object' && response.data) {
    console.log(`\n✨ Pagination successful! Data extracted from ${totalPages} pages`);
  } else if (Array.isArray(response)) {
    console.log(`\n✅ Pagination successful! Extracted ${response.length} items`);
  } else {
    console.log(`\n📋 Request successful! Response type: ${typeof response}`);
  }

} catch (error) {
  console.error('❌ Error:', error.message);
  console.error('This could be due to:');
  console.error('  - Invalid API key');
  console.error('  - Rate limiting');
  console.error('  - Server issues');
  console.error('  - Network connectivity issues');
}
