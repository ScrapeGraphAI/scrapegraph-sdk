/**
 * Advanced SearchScraper Markdown Example with Async Polling
 *
 * This example demonstrates using the SearchScraper API in markdown mode
 * with async request handling and result polling.
 *
 * Features demonstrated:
 * - Async search and scrape with markdown output
 * - Polling for async results with timeout handling
 * - Error handling with async operations
 * - Cost-effective: Only 2 credits per page (vs 10 credits for AI extraction)
 */

import { searchScraper, getSearchScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

/**
 * Poll for completion of an async SearchScraper request.
 * 
 * @param {string} requestId - The request ID to poll for
 * @param {number} maxWaitTime - Maximum time to wait in seconds
 * @returns {Promise<Object|null>} The completed response or null if timeout
 */
async function waitForCompletion(requestId, maxWaitTime = 60) {
  const startTime = Date.now();
  
  while (Date.now() - startTime < maxWaitTime * 1000) {
    try {
      const result = await getSearchScraperRequest(apiKey, requestId);
      
      if (result.status === 'completed') {
        return result;
      } else if (result.status === 'failed') {
        console.error(`❌ Request failed: ${result.error || 'Unknown error'}`);
        return null;
      } else {
        console.log(`⏳ Status: ${result.status || 'processing'}... waiting 5 seconds`);
        await new Promise(resolve => setTimeout(resolve, 5000));
      }
      
    } catch (error) {
      console.warn(`⚠️ Error polling for results: ${error.message}`);
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }
  
  console.log('⏰ Timeout waiting for completion');
  return null;
}

async function advancedSearchScraperMarkdownExample() {
  console.log('🔍 Advanced SearchScraper Markdown Example with Async Polling');
  console.log('='.repeat(60));

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

    console.log('\n✅ SearchScraper request submitted successfully!');
    console.log(`📄 Request ID: ${response.request_id || 'N/A'}`);

    // Check if this is an async request that needs polling
    if (response.request_id && !response.status) {
      console.log('⏳ Waiting for async processing to complete...');
      
      // Poll for completion
      const finalResult = await waitForCompletion(response.request_id);
      
      if (finalResult) {
        // Update response with final results
        Object.assign(response, finalResult);
      } else {
        console.error('❌ Failed to get completed results');
        return false;
      }
    }

    // Display results
    if (response.status === 'completed') {
      console.log('\n🎉 SearchScraper markdown completed successfully!');
      
      // Display markdown content (first 500 chars)
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

      // Display reference URLs
      if (response.reference_urls && response.reference_urls.length > 0) {
        console.log(`\n🔗 References: ${response.reference_urls.length}`);
        console.log('\n🔗 Reference URLs:');
        response.reference_urls.forEach((url, index) => {
          console.log(`  ${index + 1}. ${url}`);
        });
      } else {
        console.log('⚠️  No reference URLs returned');
      }

      return true;
    } else {
      console.error(`❌ Request not completed. Status: ${response.status || 'unknown'}`);
      return false;
    }

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return false;
  }
}

// Run the example
try {
  const success = await advancedSearchScraperMarkdownExample();
  process.exit(success ? 0 : 1);
} catch (error) {
  console.error('❌ Unexpected error:', error.message);
  process.exit(1);
}

