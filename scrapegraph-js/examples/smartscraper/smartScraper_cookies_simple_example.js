/**
 * Simple example demonstrating cookies usage with SmartScraper.
 *
 * This example shows the basic pattern for using cookies with the API.
 */

import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

// Example cookies for authentication
const cookies = {
  session_id: '<SESSION_ID>',
  auth_token: '<JWT_TOKEN>',
  user_preferences: '<USER_PREFERENCES>'
};

async function scrapeWithCookies() {
  try {
    const response = await smartScraper(
      apiKey,
      'https://example.com/dashboard',
      'Extract user profile information',
      null, // schema
      null, // numberOfScrolls
      null, // totalPages
      cookies // cookies parameter
    );

    console.log('✅ Scraping with cookies completed successfully');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

// Run the example
scrapeWithCookies();
