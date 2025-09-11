/**
 * Example demonstrating how to use the SmartScraper API with cookies.
 *
 * This example shows how to:
 * 1. Set up the API request with cookies for authentication
 * 2. Use cookies with infinite scrolling
 * 3. Define a Zod schema for structured output
 * 4. Make the API call and handle the response
 * 5. Process the extracted data
 *
 * Requirements:
 * - Node.js 16+
 * - scrapegraph-js
 * - A .env file with your SGAI_APIKEY
 *
 * Example .env file:
 * SGAI_APIKEY=your_api_key_here
 */

import { smartScraper } from 'scrapegraph-js';
import { z } from 'zod';
import 'dotenv/config';

// Define the data schema for structured output
const CookieInfoSchema = z.object({
  cookies: z.record(z.string()).describe('Dictionary of cookie key-value pairs')
});

async function main() {
  const apiKey = process.env.SGAI_APIKEY;

  // Check if API key is available
  if (!apiKey) {
    console.error('Error: SGAI_APIKEY not found in .env file');
    console.log('Please create a .env file with your API key:');
    console.log('SGAI_APIKEY=your_api_key_here');
    return;
  }

  // Example 1: Basic cookies example (httpbin.org/cookies)
  console.log('='.repeat(60));
  console.log('EXAMPLE 1: Basic Cookies Example');
  console.log('='.repeat(60));

  const websiteUrl = 'https://httpbin.org/cookies';
  const userPrompt = 'Extract all cookies info';
  const cookies = { cookies_key: 'cookies_value' };

  try {
    // Perform the scraping with cookies
    const response = await smartScraper(
      apiKey,
      websiteUrl,
      userPrompt,
      CookieInfoSchema,
      null, // numberOfScrolls
      null, // totalPages
      cookies
    );

    // Print the results
    console.log('\nExtracted Cookie Information:');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`Error occurred: ${error.message}`);
  }

  // Example 2: Cookies with infinite scrolling
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 2: Cookies with Infinite Scrolling');
  console.log('='.repeat(60));

  const cookiesWithScroll = { session_id: 'abc123', user_token: 'xyz789' };

  try {
    // Perform the scraping with cookies and infinite scrolling
    const response = await smartScraper(
      apiKey,
      websiteUrl,
      'Extract all cookies and scroll information',
      CookieInfoSchema,
      3, // numberOfScrolls
      null, // totalPages
      cookiesWithScroll
    );

    // Print the results
    console.log('\nExtracted Cookie Information with Scrolling:');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`Error occurred: ${error.message}`);
  }

  // Example 3: Cookies with pagination
  console.log('\n' + '='.repeat(60));
  console.log('EXAMPLE 3: Cookies with Pagination');
  console.log('='.repeat(60));

  const cookiesWithPagination = { auth_token: 'secret123', preferences: 'dark_mode' };

  try {
    // Perform the scraping with cookies and pagination
    const response = await smartScraper(
      apiKey,
      websiteUrl,
      'Extract all cookies from multiple pages',
      CookieInfoSchema,
      null, // numberOfScrolls
      3, // totalPages
      cookiesWithPagination
    );

    // Print the results
    console.log('\nExtracted Cookie Information with Pagination:');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`Error occurred: ${error.message}`);
  }
}

// Run the example
main().catch(console.error);
