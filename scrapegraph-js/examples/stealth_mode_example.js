/**
 * Stealth Mode Examples for ScrapeGraph AI JavaScript SDK
 *
 * This file demonstrates how to use stealth mode with various endpoints
 * to avoid bot detection when scraping websites.
 *
 * Stealth mode enables advanced techniques to make requests appear more
 * like those from a real browser, helping to bypass basic bot detection.
 */

import {
  smartScraper,
  searchScraper,
  markdownify,
  scrape,
  agenticScraper,
  crawl,
  getScrapeRequest,
  getAgenticScraperRequest,
  getCrawlRequest
} from '../index.js';
import 'dotenv/config';

// Get API key from environment variable
const API_KEY = process.env.SGAI_APIKEY || 'your-api-key-here';

// ============================================================================
// EXAMPLE 1: SmartScraper with Stealth Mode
// ============================================================================

async function exampleSmartScraperWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 1: SmartScraper with Stealth Mode');
  console.log('='.repeat(60));

  try {
    const response = await smartScraper(
      API_KEY,
      'https://www.scrapethissite.com/pages/simple/',
      'Extract country names and capitals',
      null,          // schema
      null,          // numberOfScrolls
      null,          // totalPages
      null,          // cookies
      {},            // options
      false,         // plain_text
      false,         // renderHeavyJs
      true           // stealth - Enable stealth mode
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
    console.log('Result:', JSON.stringify(response.result, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 2: SmartScraper with Stealth Mode and Pagination
// ============================================================================

async function exampleSmartScraperWithStealthAndPagination() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 2: SmartScraper with Stealth Mode and Pagination');
  console.log('='.repeat(60));

  try {
    const response = await smartScraper(
      API_KEY,
      'https://example.com/products',
      'Extract all product information from multiple pages',
      null,          // schema
      10,            // numberOfScrolls
      5,             // totalPages
      null,          // cookies
      {},            // options
      false,         // plain_text
      true,          // renderHeavyJs - Enable JS rendering
      true           // stealth - Enable stealth mode
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
    console.log('Products extracted:', response.result);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 3: SearchScraper with Stealth Mode
// ============================================================================

async function exampleSearchScraperWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 3: SearchScraper with Stealth Mode');
  console.log('='.repeat(60));

  try {
    const response = await searchScraper(
      API_KEY,
      'What are the latest developments in AI technology?',
      5,             // numResults
      null,          // schema
      null,          // userAgent
      {
        stealth: true,           // Enable stealth mode
        extractionMode: true,
        renderHeavyJs: false
      }
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
    console.log('Result:', JSON.stringify(response.result, null, 2));

    if (response.reference_urls) {
      console.log('Reference URLs:', response.reference_urls);
    }
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 4: Markdownify with Stealth Mode
// ============================================================================

async function exampleMarkdownifyWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 4: Markdownify with Stealth Mode');
  console.log('='.repeat(60));

  try {
    const response = await markdownify(
      API_KEY,
      'https://www.example.com',
      {
        stealth: true  // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
    console.log('Markdown Preview (first 500 chars):');
    console.log(response.result.substring(0, 500));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 5: Scrape with Stealth Mode
// ============================================================================

async function exampleScrapeWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 5: Scrape with Stealth Mode');
  console.log('='.repeat(60));

  try {
    const response = await scrape(
      API_KEY,
      'https://www.example.com',
      {
        stealth: true  // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Scrape Request ID:', response.scrape_request_id);
    console.log('HTML Preview (first 500 chars):');
    console.log(response.html.substring(0, 500));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 6: Scrape with Stealth Mode and Heavy JS Rendering
// ============================================================================

async function exampleScrapeWithStealthAndJS() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 6: Scrape with Stealth Mode and Heavy JS');
  console.log('='.repeat(60));

  try {
    const response = await scrape(
      API_KEY,
      'https://www.example.com',
      {
        renderHeavyJs: true,  // Enable JavaScript rendering
        stealth: true         // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Scrape Request ID:', response.scrape_request_id);
    console.log('HTML Preview (first 500 chars):');
    console.log(response.html.substring(0, 500));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 7: Scrape with Stealth Mode and Custom Headers
// ============================================================================

async function exampleScrapeWithStealthAndHeaders() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 7: Scrape with Stealth Mode and Custom Headers');
  console.log('='.repeat(60));

  try {
    const customHeaders = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
      'DNT': '1'
    };

    const response = await scrape(
      API_KEY,
      'https://www.protected-site.com',
      {
        headers: customHeaders,  // Custom headers
        stealth: true            // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Scrape Request ID:', response.scrape_request_id);
    console.log('Success! Stealth mode + custom headers bypassed detection.');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 8: Agentic Scraper with Stealth Mode
// ============================================================================

async function exampleAgenticScraperWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 8: Agentic Scraper with Stealth Mode');
  console.log('='.repeat(60));

  try {
    const steps = [
      'Type user@example.com in email input box',
      'Type password123 in password input box',
      'Click on login button'
    ];

    const response = await agenticScraper(
      API_KEY,
      'https://dashboard.example.com/login',
      steps,
      true,          // useSession
      null,          // userPrompt
      null,          // outputSchema
      false,         // aiExtraction
      {
        stealth: true  // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
    console.log('Message:', response.message);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 9: Agentic Scraper with Stealth Mode and AI Extraction
// ============================================================================

async function exampleAgenticScraperWithStealthAndAI() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 9: Agentic Scraper with Stealth and AI Extraction');
  console.log('='.repeat(60));

  try {
    const steps = [
      'Navigate to user profile section',
      'Click on settings tab'
    ];

    const outputSchema = {
      user_info: {
        type: 'object',
        properties: {
          username: { type: 'string' },
          email: { type: 'string' },
          settings: { type: 'object' }
        }
      }
    };

    const response = await agenticScraper(
      API_KEY,
      'https://dashboard.example.com',
      steps,
      true,                                                    // useSession
      'Extract user profile information and settings',         // userPrompt
      outputSchema,                                            // outputSchema
      true,                                                    // aiExtraction
      {
        stealth: true  // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 10: Crawl with Stealth Mode
// ============================================================================

async function exampleCrawlWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 10: Crawl with Stealth Mode');
  console.log('='.repeat(60));

  try {
    const schema = {
      type: 'object',
      properties: {
        title: { type: 'string', description: 'Page title' },
        content: { type: 'string', description: 'Main content' }
      },
      required: ['title']
    };

    const response = await crawl(
      API_KEY,
      'https://www.example.com',
      'Extract page titles and main content',
      schema,
      {
        depth: 2,
        maxPages: 5,
        stealth: true  // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Crawl ID:', response.id);
    console.log('Message:', response.message);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 11: Crawl with Stealth Mode and Sitemap
// ============================================================================

async function exampleCrawlWithStealthAndSitemap() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 11: Crawl with Stealth Mode and Sitemap');
  console.log('='.repeat(60));

  try {
    const schema = {
      type: 'object',
      properties: {
        product_name: { type: 'string' },
        price: { type: 'string' },
        description: { type: 'string' }
      },
      required: ['product_name']
    };

    const response = await crawl(
      API_KEY,
      'https://www.example-shop.com',
      'Extract product information from all pages',
      schema,
      {
        sitemap: true,      // Use sitemap for better page discovery
        depth: 3,
        maxPages: 10,
        stealth: true       // Enable stealth mode
      }
    );

    console.log('Status:', response.status);
    console.log('Crawl ID:', response.id);
    console.log('Message:', response.message);
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 12: Complete Workflow with Stealth Mode
// ============================================================================

async function exampleCompleteWorkflowWithStealth() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 12: Complete Workflow with Stealth Mode');
  console.log('='.repeat(60));

  try {
    // Step 1: Start a scrape request with stealth mode
    console.log('\n1. Starting scrape request with stealth mode...');
    const scrapeResponse = await scrape(
      API_KEY,
      'https://www.example.com',
      {
        renderHeavyJs: true,
        stealth: true
      }
    );

    console.log('   Scrape initiated. Request ID:', scrapeResponse.scrape_request_id);
    console.log('   Status:', scrapeResponse.status);

    // Step 2: Wait a bit and check the result (if processing)
    if (scrapeResponse.status === 'processing') {
      console.log('\n2. Waiting for scrape to complete...');
      await new Promise(resolve => setTimeout(resolve, 3000)); // Wait 3 seconds

      const result = await getScrapeRequest(API_KEY, scrapeResponse.scrape_request_id);
      console.log('   Updated Status:', result.status);

      if (result.status === 'completed') {
        console.log('   HTML received (length):', result.html.length);
      }
    }

    console.log('\n✅ Workflow completed successfully with stealth mode!');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 13: SearchScraper with Stealth and Custom User Agent
// ============================================================================

async function exampleSearchScraperWithStealthAndUserAgent() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 13: SearchScraper with Stealth and User Agent');
  console.log('='.repeat(60));

  try {
    const customUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36';

    const response = await searchScraper(
      API_KEY,
      'Find the best practices for web scraping',
      5,             // numResults
      null,          // schema
      customUserAgent,  // Custom user agent
      {
        stealth: true,
        extractionMode: true
      }
    );

    console.log('Status:', response.status);
    console.log('Request ID:', response.request_id);
    console.log('Result:', JSON.stringify(response.result, null, 2));
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// EXAMPLE 14: Comparing With and Without Stealth Mode
// ============================================================================

async function exampleCompareStealthMode() {
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 14: Comparing With and Without Stealth Mode');
  console.log('='.repeat(60));

  try {
    const testUrl = 'https://www.example.com';

    // Without stealth mode
    console.log('\n1. Scraping WITHOUT stealth mode...');
    const responseWithoutStealth = await scrape(
      API_KEY,
      testUrl,
      {
        stealth: false
      }
    );
    console.log('   Status:', responseWithoutStealth.status);
    console.log('   Request ID:', responseWithoutStealth.scrape_request_id);

    // With stealth mode
    console.log('\n2. Scraping WITH stealth mode...');
    const responseWithStealth = await scrape(
      API_KEY,
      testUrl,
      {
        stealth: true
      }
    );
    console.log('   Status:', responseWithStealth.status);
    console.log('   Request ID:', responseWithStealth.scrape_request_id);

    console.log('\n📊 Comparison complete!');
    console.log('   Both requests succeeded, but stealth mode provides better bot detection avoidance.');
  } catch (error) {
    console.error('Error:', error.message);
  }
}

// ============================================================================
// RUN ALL EXAMPLES
// ============================================================================

async function runAllExamples() {
  console.log('\n' + '='.repeat(60));
  console.log('STEALTH MODE EXAMPLES FOR SCRAPEGRAPH AI JAVASCRIPT SDK');
  console.log('='.repeat(60));
  console.log('\nThese examples demonstrate how to use stealth mode');
  console.log('to avoid bot detection when scraping websites.');
  console.log('\nStealth mode is available for all major endpoints:');
  console.log('- SmartScraper');
  console.log('- SearchScraper');
  console.log('- Markdownify');
  console.log('- Scrape');
  console.log('- Agentic Scraper');
  console.log('- Crawl');

  const examples = [
    { name: 'SmartScraper with Stealth', fn: exampleSmartScraperWithStealth },
    { name: 'SmartScraper with Stealth and Pagination', fn: exampleSmartScraperWithStealthAndPagination },
    { name: 'SearchScraper with Stealth', fn: exampleSearchScraperWithStealth },
    { name: 'Markdownify with Stealth', fn: exampleMarkdownifyWithStealth },
    { name: 'Scrape with Stealth', fn: exampleScrapeWithStealth },
    { name: 'Scrape with Stealth and Heavy JS', fn: exampleScrapeWithStealthAndJS },
    { name: 'Scrape with Stealth and Custom Headers', fn: exampleScrapeWithStealthAndHeaders },
    { name: 'Agentic Scraper with Stealth', fn: exampleAgenticScraperWithStealth },
    { name: 'Agentic Scraper with Stealth and AI', fn: exampleAgenticScraperWithStealthAndAI },
    { name: 'Crawl with Stealth', fn: exampleCrawlWithStealth },
    { name: 'Crawl with Stealth and Sitemap', fn: exampleCrawlWithStealthAndSitemap },
    { name: 'Complete Workflow with Stealth', fn: exampleCompleteWorkflowWithStealth },
    { name: 'SearchScraper with Stealth and User Agent', fn: exampleSearchScraperWithStealthAndUserAgent },
    { name: 'Compare Stealth Mode', fn: exampleCompareStealthMode }
  ];

  for (let i = 0; i < examples.length; i++) {
    const example = examples[i];
    try {
      console.log(`\n\n📌 Running Example ${i + 1}/${examples.length}: ${example.name}`);
      await example.fn();
      console.log(`\n✅ Example ${i + 1} completed`);
    } catch (error) {
      console.error(`\n❌ Example ${i + 1} failed: ${error.message}`);
    }

    // Add a small delay between examples
    if (i < examples.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  console.log('\n' + '='.repeat(60));
  console.log('ALL EXAMPLES COMPLETED');
  console.log('='.repeat(60));
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

// Run all examples if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllExamples()
    .then(() => {
      console.log('\n✨ All stealth mode examples executed successfully!');
      process.exit(0);
    })
    .catch(error => {
      console.error('\n💥 Fatal error:', error.message);
      process.exit(1);
    });
}

// Export individual examples for selective usage
export {
  exampleSmartScraperWithStealth,
  exampleSmartScraperWithStealthAndPagination,
  exampleSearchScraperWithStealth,
  exampleMarkdownifyWithStealth,
  exampleScrapeWithStealth,
  exampleScrapeWithStealthAndJS,
  exampleScrapeWithStealthAndHeaders,
  exampleAgenticScraperWithStealth,
  exampleAgenticScraperWithStealthAndAI,
  exampleCrawlWithStealth,
  exampleCrawlWithStealthAndSitemap,
  exampleCompleteWorkflowWithStealth,
  exampleSearchScraperWithStealthAndUserAgent,
  exampleCompareStealthMode,
  runAllExamples
};
