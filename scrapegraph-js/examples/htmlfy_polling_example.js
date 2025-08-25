/**
 * Example demonstrating how to use HTMLfy with polling for results.
 *
 * This example shows how to:
 * 1. Make an HTMLfy request
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
 * node htmlfy_polling_example.js
 */

import { htmlfy, getHtmlfyRequest } from '../index.js';
import fs from 'fs/promises';
import path from 'path';

// Configuration
const API_KEY = process.env.SGAI_API_KEY || 'your-api-key-here';
const OUTPUT_DIR = 'htmlfy_polling_output';
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
 * Poll for HTMLfy results until completion or timeout.
 *
 * @param {string} apiKey - Your API key
 * @param {string} requestId - The request ID to poll for
 * @param {Object} options - Polling options
 * @returns {Object} The final result
 */
async function pollHtmlfyResult(apiKey, requestId, options = {}) {
  const {
    interval = POLLING_INTERVAL,
    maxTime = MAX_POLLING_TIME,
    maxRetries = MAX_RETRIES
  } = options;

  console.log(`🔍 Polling for HTMLfy result: ${requestId}`);
  console.log(`⏱️  Polling interval: ${interval}ms`);
  console.log(`⏰ Max polling time: ${maxTime / 1000}s`);

  const startTime = Date.now();
  let attempt = 0;

  while (true) {
    try {
      attempt++;
      console.log(`\n📡 Polling attempt ${attempt}...`);

      const result = await getHtmlfyRequest(apiKey, requestId);
      
      console.log(`📊 Status: ${result.status}`);
      
      if (result.status === 'completed') {
        console.log('✅ HTMLfy request completed successfully!');
        return result;
      } else if (result.status === 'failed') {
        console.error(`❌ HTMLfy request failed: ${result.error || 'Unknown error'}`);
        throw new Error(`HTMLfy request failed: ${result.error || 'Unknown error'}`);
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
      console.error(`❌ Polling error on attempt ${attempt}: ${error.message}`);
      
      if (attempt >= maxRetries) {
        throw new Error(`Max retries (${maxRetries}) exceeded: ${error.message}`);
      }
      
      // Wait before retry
      const retryDelay = interval * attempt;
      console.log(`⏳ Waiting ${retryDelay / 1000}s before retry...`);
      await wait(retryDelay);
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
  // Create output directory if it doesn't exist
  try {
    await fs.mkdir(outputDir, { recursive: true });
  } catch (error) {
    if (error.code !== 'EEXIST') {
      throw error;
    }
  }

  // Save HTML file
  const htmlFile = path.join(outputDir, `${filename}.html`);
  await fs.writeFile(htmlFile, htmlContent, 'utf8');

  console.log(`💾 HTML content saved to: ${htmlFile}`);
  return htmlFile;
}

/**
 * Main function demonstrating HTMLfy polling usage.
 */
async function main() {
  console.log('🚀 HTMLfy Polling Example with scrapegraph-js SDK');
  console.log('='.repeat(60));

  // Check API key
  if (!API_KEY || API_KEY === 'your-api-key-here') {
    console.error('❌ Please set your SGAI_API_KEY environment variable');
    console.error('Example: export SGAI_API_KEY=your_api_key_here');
    process.exit(1);
  }

  console.log('✅ API key configured');

  const testUrl = 'https://example.com';
  const testName = 'example_polling';

  try {
    console.log(`\n🌐 Starting HTMLfy request for: ${testUrl}`);
    
    // Step 1: Make the initial HTMLfy request
    const startTime = Date.now();
    const initialResult = await htmlfy(API_KEY, testUrl, {
      renderHeavyJs: false
    });
    
    const requestTime = (Date.now() - startTime) / 1000;
    console.log(`✅ Initial request completed in ${requestTime.toFixed(2)}s`);
    
    if (initialResult.status === 'completed') {
      // Request completed immediately
      console.log('🎉 Request completed immediately!');
      
      if (initialResult.html) {
        const filename = `${testName}_immediate`;
        await saveHtmlContent(initialResult.html, filename);
        console.log(`📁 HTML saved to: ${OUTPUT_DIR}/${filename}.html`);
      }
      
    } else if (initialResult.htmlfy_request_id) {
      // Request is processing, need to poll
      console.log(`🔄 Request is processing, request ID: ${initialResult.htmlfy_request_id}`);
      
      // Step 2: Poll for results
      const finalResult = await pollHtmlfyResult(API_KEY, initialResult.htmlfy_request_id, {
        interval: POLLING_INTERVAL,
        maxTime: MAX_POLLING_TIME,
        maxRetries: MAX_RETRIES
      });
      
      // Step 3: Save the final result
      if (finalResult.html) {
        const filename = `${testName}_polled`;
        await saveHtmlContent(finalResult.html, filename);
        console.log(`📁 HTML saved to: ${OUTPUT_DIR}/${filename}.html`);
        
        // Display some basic info about the HTML
        console.log(`\n📊 HTML Content Summary:`);
        console.log(`  Total length: ${finalResult.html.length.toLocaleString()} characters`);
        console.log(`  Lines: ${finalResult.html.split('\n').length.toLocaleString()}`);
        console.log(`  Has DOCTYPE: ${finalResult.html.trim().startsWith('<!DOCTYPE')}`);
        console.log(`  Has HTML tag: ${finalResult.html.toLowerCase().includes('<html')}`);
        console.log(`  Has Head tag: ${finalResult.html.toLowerCase().includes('<head')}`);
        console.log(`  Has Body tag: ${finalResult.html.toLowerCase().includes('<body')}`);
      }
      
    } else {
      console.error('❌ No request ID received from initial request');
      console.log('Initial result:', initialResult);
    }
    
    const totalTime = (Date.now() - startTime) / 1000;
    console.log(`\n⏱️  Total processing time: ${totalTime.toFixed(2)}s`);
    console.log(`📁 Output saved to: ${OUTPUT_DIR}/`);
    console.log('✅ HTMLfy polling example completed successfully');
    
  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

// Run the example
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(error => {
    console.error('❌ Fatal error:', error.message);
    process.exit(1);
  });
}
