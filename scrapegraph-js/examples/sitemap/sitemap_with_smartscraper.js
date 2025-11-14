import { sitemap, smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

/**
 * Advanced Example: Extract sitemap and scrape selected URLs
 *
 * This example demonstrates how to combine the sitemap endpoint
 * with smartScraper to extract structured data from multiple pages.
 */

const apiKey = process.env.SGAI_APIKEY;

// Configuration
const websiteUrl = 'https://scrapegraphai.com/';
const maxPagesToScrape = 3; // Limit number of pages to scrape
const userPrompt = 'Extract the page title and main heading';

console.log('🗺️  Step 1: Extracting sitemap from:', websiteUrl);
console.log('⏳ Please wait...\n');

try {
  // Step 1: Get all URLs from sitemap
  const sitemapResponse = await sitemap(apiKey, websiteUrl);

  console.log('✅ Sitemap extracted successfully!');
  console.log(`📊 Total URLs found: ${sitemapResponse.urls.length}\n`);

  // Step 2: Filter URLs (example: only blog posts)
  const filteredUrls = sitemapResponse.urls
    .filter(url => url.includes('/blog/') || url.includes('/post/'))
    .slice(0, maxPagesToScrape);

  if (filteredUrls.length === 0) {
    console.log('ℹ️  No blog URLs found, using first 3 URLs instead');
    filteredUrls.push(...sitemapResponse.urls.slice(0, maxPagesToScrape));
  }

  console.log(`🎯 Selected ${filteredUrls.length} URLs to scrape:`);
  filteredUrls.forEach((url, index) => {
    console.log(`   ${index + 1}. ${url}`);
  });

  // Step 3: Scrape each selected URL
  console.log('\n🤖 Step 2: Scraping selected URLs...\n');

  const results = [];

  for (let i = 0; i < filteredUrls.length; i++) {
    const url = filteredUrls[i];
    console.log(`📄 Scraping (${i + 1}/${filteredUrls.length}): ${url}`);

    try {
      const scrapeResponse = await smartScraper(
        apiKey,
        url,
        userPrompt
      );

      results.push({
        url: url,
        data: scrapeResponse.result,
        status: 'success'
      });

      console.log('   ✅ Success');

      // Add a small delay between requests to avoid rate limiting
      if (i < filteredUrls.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

    } catch (error) {
      console.log(`   ❌ Failed: ${error.message}`);
      results.push({
        url: url,
        error: error.message,
        status: 'failed'
      });
    }
  }

  // Step 4: Display results
  console.log('\n📊 Scraping Results:\n');
  results.forEach((result, index) => {
    console.log(`${index + 1}. ${result.url}`);
    if (result.status === 'success') {
      console.log('   Status: ✅ Success');
      console.log('   Data:', JSON.stringify(result.data, null, 2));
    } else {
      console.log('   Status: ❌ Failed');
      console.log('   Error:', result.error);
    }
    console.log('');
  });

  // Summary
  const successCount = results.filter(r => r.status === 'success').length;
  console.log('📈 Summary:');
  console.log(`   ✅ Successful: ${successCount}`);
  console.log(`   ❌ Failed: ${results.length - successCount}`);
  console.log(`   📊 Total: ${results.length}`);

} catch (error) {
  console.error('❌ Error:', error.message);
  process.exit(1);
}
