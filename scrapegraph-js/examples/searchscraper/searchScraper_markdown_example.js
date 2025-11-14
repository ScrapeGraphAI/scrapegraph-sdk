/**
 * Basic SearchScraper Markdown Example
 *
 * This example demonstrates the simplest way to use the SearchScraper API
 * in markdown mode to search and scrape web pages, returning raw markdown content
 * instead of AI-extracted data.
 *
 * Features demonstrated:
 * - Basic search and scrape with markdown output
 * - Simple error handling
 * - Minimal code approach
 * - Cost-effective: Only 2 credits per page (vs 10 credits for AI extraction)
 */

import { searchScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

async function basicSearchScraperMarkdownExample() {
  console.log('🔍 Basic SearchScraper Markdown Example');
  console.log('='.repeat(50));

  // Configuration
  const userPrompt = 'Latest developments in artificial intelligence';
  const numResults = 3;

  console.log(`📝 Query: ${userPrompt}`);
  console.log(`📊 Results: ${numResults} websites`);
  console.log('🔧 Mode: Markdown conversion');
  console.log('💰 Cost: 2 credits per page (vs 10 for AI extraction)');

  try {
    // Send a searchscraper request in markdown mode
    const response = await searchScraper(
      apiKey,
      userPrompt,
      numResults,
      null, // schema
      null, // userAgent
      {
        extractionMode: false, // false = markdown mode, true = AI extraction mode
      }
    );

    console.log('\n✅ SearchScraper markdown completed successfully!');
    console.log(`📄 Request ID: ${response.request_id || 'N/A'}`);

    // For async requests, you would need to poll for results
    if (response.request_id && !response.status) {
      console.log('📝 This is an async request. Use getSearchScraperRequest() to retrieve results.');
      console.log(`🔍 Use: getSearchScraperRequest('${response.request_id}')`);
    } else {
      // If it's a sync response, display the results
      if (response.markdown_content) {
        const markdownContent = response.markdown_content;
        console.log('\n📝 Markdown Content Preview:');
        console.log(markdownContent.length > 500 
          ? markdownContent.substring(0, 500) + '...' 
          : markdownContent
        );
      } else {
        console.log('⚠️  No markdown content returned');
      }

      if (response.reference_urls) {
        console.log(`\n🔗 References: ${response.reference_urls.length}`);
        console.log('\n🔗 Reference URLs:');
        response.reference_urls.forEach((url, index) => {
          console.log(`  ${index + 1}. ${url}`);
        });
      } else {
        console.log('⚠️  No reference URLs returned');
      }
    }

    return true;

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return false;
  }
}

// Run the example
try {
  const success = await basicSearchScraperMarkdownExample();
  process.exit(success ? 0 : 1);
} catch (error) {
  console.error('❌ Unexpected error:', error.message);
  process.exit(1);
}

