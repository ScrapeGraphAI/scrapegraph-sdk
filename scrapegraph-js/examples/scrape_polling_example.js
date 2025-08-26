/**
 * Example demonstrating how to use Scrape with polling for results.
 *
 * This example shows how to:
 * 1. Make a scrape request
 * 2. Poll for results until completion
 * 3. Handle different status responses
 * 4. Implement timeout and retry logic
 *
 * Requirements:
 * - Node.js 16+
 * - scrapegraph-js
 * - A valid API key
 *
 * Usage:
 * node scrape_polling_example.js
 */

import { scrape, getScrapeRequest } from '../index.js';
import fs from 'fs/promises';
import path from 'path';

// Configuration
const API_KEY = process.env.SGAI_API_KEY || 'your-api-key-here';
const OUTPUT_DIR = 'scrape_polling_output';
const POLLING_INTERVAL = 2000; // 2 seconds
const MAX_POLLING_TIME = 300000; // 5 minutes
const MAX_RETRIES = 3;

/**
 * Wait for a specified amount of time.
 *
 * @param {number} ms - Milliseconds to wait
 * @returns {Promise} Promise that resolves after the specified time
 */
function wait(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Poll for scrape results until completion or timeout.
 *
 * @param {string} apiKey - Your API key
 * @param {string} requestId - The request ID to poll for
 * @param {Object} options - Polling options
 * @returns {Object} The final result
 */
async function pollScrapeResult(apiKey, requestId, options = {}) {
  const {
    interval = POLLING_INTERVAL,
    maxTime = MAX_POLLING_TIME,
    maxRetries = MAX_RETRIES
  } = options;

  console.log(`🔍 Polling for scrape result: ${requestId}`);
  console.log(`⏱️  Polling interval: ${interval}ms`);
  console.log(`⏰ Max polling time: ${maxTime / 1000}s`);

  const startTime = Date.now();
  let attempt = 0;

  while (true) {
    try {
      attempt++;
      console.log(`\n📡 Polling attempt ${attempt}...`);

      const result = await getScrapeRequest(apiKey, requestId);
      
      console.log(`📊 Status: ${result.status}`);
      
      if (result.status === 'completed') {
        console.log('✅ Scrape request completed successfully!');
        return result;
      } else if (result.status === 'failed') {
        console.error(`❌ Scrape request failed: ${result.error || 'Unknown error'}`);
        throw new Error(`Scrape request failed: ${result.error || 'Unknown error'}`);
      } else if (result.status === 'processing') {
        console.log('⏳ Request is still processing...');
        
        // Check if we've exceeded the maximum polling time
        if (Date.now() - startTime > maxTime) {
          throw new Error(`Polling timeout after ${maxTime / 1000}s`);
        }
        
        // Wait before the next poll
        console.log(`⏳ Waiting ${interval / 1000}s before next poll...`);
        await wait(interval);
        
      } else {
        console.log(`ℹ️  Unknown status: ${result.status}`);
        
        // Check if we've exceeded the maximum polling time
        if (Date.now() - startTime > maxTime) {
          throw new Error(`Polling timeout after ${maxTime / 1000}s`);
        }
        
        // Wait before the next poll
        await wait(interval);
      }
      
    } catch (error) {
      console.error(`❌ Polling error: ${error.message}`);
      
      // Check if we've exceeded the maximum polling time
      if (Date.now() - startTime > maxTime) {
        throw new Error(`Polling timeout after ${maxTime / 1000}s`);
      }
      
      // Check if we've exceeded the maximum retries
      if (attempt >= maxRetries) {
        throw new Error(`Max retries (${maxRetries}) exceeded`);
      }
      
      // Wait before retry
      console.log(`⏳ Waiting ${interval / 1000}s before retry...`);
      await wait(interval);
    }
  }
}

/**
 * Save HTML content to a file.
 *
 * @param {string} htmlContent - The HTML content to save
 * @param {string} filename - The name of the file (without extension)
 * @param {string} outputDir - The directory to save the file in
 * @returns {string} Path to the saved file
 */
async function saveHtmlContent(htmlContent, filename, outputDir = OUTPUT_DIR) {
  try {
    await fs.mkdir(outputDir, { recursive: true });
  } catch (error) {
    if (error.code !== 'EEXIST') {
      throw error;
    }
  }

  const htmlFile = path.join(outputDir, `${filename}.html`);
  await fs.writeFile(htmlFile, htmlContent, 'utf8');

  console.log(`💾 HTML content saved to: ${htmlFile}`);
  return htmlFile;
}

/**
 * Analyze HTML content and provide basic statistics.
 *
 * @param {string} htmlContent - The HTML content to analyze
 * @returns {Object} Basic statistics about the HTML content
 */
function analyzeHtmlContent(htmlContent) {
  if (!htmlContent) {
    return {
      totalLength: 0,
      lines: 0,
      hasDoctype: false,
      hasHtmlTag: false,
      hasHeadTag: false,
      hasBodyTag: false,
      scriptTags: 0,
      styleTags: 0,
      divTags: 0,
      pTags: 0,
      imgTags: 0,
      linkTags: 0
    };
  }

  const stats = {
    totalLength: htmlContent.length,
    lines: htmlContent.split('\n').length,
    hasDoctype: htmlContent.trim().startsWith('<!DOCTYPE'),
    hasHtmlTag: htmlContent.toLowerCase().includes('<html'),
    hasHeadTag: htmlContent.toLowerCase().includes('<head'),
    hasBodyTag: htmlContent.toLowerCase().includes('<body'),
    scriptTags: (htmlContent.match(/<script/gi) || []).length,
    styleTags: (htmlContent.match(/<style/gi) || []).length,
    divTags: (htmlContent.match(/<div/gi) || []).length,
    pTags: (htmlContent.match(/<p/gi) || []).length,
    imgTags: (htmlContent.match(/<img/gi) || []).length,
    linkTags: (htmlContent.match(/<link/gi) || []).length
  };

  return stats;
}

/**
 * Main function demonstrating scrape polling usage.
 */
async function main() {
  // Example website to test
  const testWebsite = {
    url: 'https://example.com',
    name: 'example_website',
    renderHeavyJs: false,
    description: 'Simple static website with polling'
  };

  console.log('🚀 Scrape Polling Example with scrapegraph-js SDK');
  console.log('='.repeat(60));

  // Check API key
  if (!API_KEY || API_KEY === 'your-api-key-here') {
    console.error('❌ Please set your SGAI_API_KEY environment variable');
    console.error('Example: export SGAI_API_KEY=your_api_key_here');
    process.exit(1);
  }

  console.log('✅ API key configured');
  console.log(`🌐 Testing website: ${testWebsite.url}`);
  console.log(`🔧 Render Heavy JS: ${testWebsite.renderHeavyJs}\n`);

  try {
    // Step 1: Make the initial scrape request
    console.log('📤 Step 1: Making initial scrape request...');
    const initialResult = await scrape(API_KEY, testWebsite.url, {
      renderHeavyJs: testWebsite.renderHeavyJs
    });

    console.log(`✅ Initial request submitted successfully`);
    console.log(`🆔 Request ID: ${initialResult.scrape_request_id}`);
    console.log(`📊 Initial Status: ${initialResult.status}`);

    // Step 2: Poll for results
    console.log('\n📡 Step 2: Polling for results...');
    const finalResult = await pollScrapeResult(API_KEY, initialResult.scrape_request_id, {
      interval: POLLING_INTERVAL,
      maxTime: MAX_POLLING_TIME,
      maxRetries: MAX_RETRIES
    });

    // Step 3: Analyze and save the HTML content
    console.log('\n📊 Step 3: Analyzing and saving HTML content...');
    
    const htmlContent = finalResult.html || '';
    if (htmlContent) {
      const stats = analyzeHtmlContent(htmlContent);
      console.log('\nHTML Content Analysis:');
      console.log(`  Total length: ${stats.totalLength.toLocaleString()} characters`);
      console.log(`  Lines: ${stats.lines.toLocaleString()}`);
      console.log(`  Has DOCTYPE: ${stats.hasDoctype}`);
      console.log(`  Has HTML tag: ${stats.hasHtmlTag}`);
      console.log(`  Has Head tag: ${stats.hasHeadTag}`);
      console.log(`  Has Body tag: ${stats.hasBodyTag}`);
      console.log(`  Script tags: ${stats.scriptTags}`);
      console.log(`  Style tags: ${stats.styleTags}`);
      console.log(`  Div tags: ${stats.divTags}`);
      console.log(`  Paragraph tags: ${stats.pTags}`);
      console.log(`  Image tags: ${stats.imgTags}`);
      console.log(`  Link tags: ${stats.linkTags}`);

      // Save HTML content
      const filename = `${testWebsite.name}_${testWebsite.renderHeavyJs ? 'js' : 'nojs'}`;
      const savedFile = await saveHtmlContent(htmlContent, filename);

      // Show first 500 characters as preview
      const preview = htmlContent.substring(0, 500).replace(/\n/g, ' ').trim();
      console.log(`\nHTML Preview (first 500 chars):`);
      console.log(`  ${preview}...`);

      console.log(`\n📁 Output saved to: ${savedFile}`);
    } else {
      console.log('❌ No HTML content received');
    }

    // Summary
    console.log('\n🎯 Summary:');
    console.log(`✅ Successfully processed ${testWebsite.url} with polling`);
    console.log(`🆔 Final Request ID: ${finalResult.scrape_request_id}`);
    console.log(`📊 Final Status: ${finalResult.status}`);
    console.log(`⏱️  Total processing time: ${((Date.now() - Date.now()) / 1000).toFixed(2)}s`);

  } catch (error) {
    console.error(`\n💥 Error occurred: ${error.message}`);
    console.error('Check your API key and internet connection');
    process.exit(1);
  }

  console.log('\n✅ Scrape polling example completed successfully');
}

// Run the example
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(error => {
    console.error('❌ Fatal error:', error.message);
    process.exit(1);
  });
}
