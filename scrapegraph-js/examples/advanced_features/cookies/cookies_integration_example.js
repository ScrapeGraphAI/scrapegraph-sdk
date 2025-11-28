/**
 * Comprehensive example demonstrating cookies integration for web scraping.
 *
 * This example shows various real-world scenarios where cookies are essential:
 * 1. E-commerce site scraping with authentication
 * 2. Social media scraping with session cookies
 * 3. Banking/financial site scraping with secure cookies
 * 4. News site scraping with user preferences
 * 5. API endpoint scraping with authentication tokens
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

// Define data schemas for different scenarios
const ProductInfoSchema = z.object({
  name: z.string().describe('Product name'),
  price: z.string().describe('Product price'),
  availability: z.string().describe('Product availability status'),
  rating: z.string().optional().describe('Product rating')
});

const SocialMediaPostSchema = z.object({
  author: z.string().describe('Post author'),
  content: z.string().describe('Post content'),
  likes: z.string().optional().describe('Number of likes'),
  comments: z.string().optional().describe('Number of comments'),
  timestamp: z.string().optional().describe('Post timestamp')
});

const NewsArticleSchema = z.object({
  title: z.string().describe('Article title'),
  summary: z.string().describe('Article summary'),
  author: z.string().optional().describe('Article author'),
  publish_date: z.string().optional().describe('Publish date')
});

const BankTransactionSchema = z.object({
  date: z.string().describe('Transaction date'),
  description: z.string().describe('Transaction description'),
  amount: z.string().describe('Transaction amount'),
  type: z.string().describe('Transaction type (credit/debit)')
});

async function scrapeEcommerceWithAuth() {
  console.log('='.repeat(60));
  console.log('E-COMMERCE SITE SCRAPING WITH AUTHENTICATION');
  console.log('='.repeat(60));

  // Example cookies for an e-commerce site
  const cookies = {
    session_id: '<SESSION_ID>',
    user_id: '<USER_ID>',
    cart_id: '<CART_ID>',
    preferences: '<PREFERENCES>',
    auth_token: '<JWT_TOKEN>'
  };

  const websiteUrl = 'https://example-ecommerce.com/products';
  const userPrompt = 'Extract product information including name, price, availability, and rating';

  try {
    const response = await smartScraper(
      process.env.SGAI_APIKEY,
      websiteUrl,
      userPrompt,
      ProductInfoSchema,
      5, // numberOfScrolls - Scroll to load more products
      null, // totalPages
      cookies
    );

    console.log('✅ E-commerce scraping completed successfully');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`❌ Error in e-commerce scraping: ${error.message}`);
  }
}

async function scrapeSocialMediaWithSession() {
  console.log('\n' + '='.repeat(60));
  console.log('SOCIAL MEDIA SCRAPING WITH SESSION COOKIES');
  console.log('='.repeat(60));

  // Example cookies for a social media site
  const cookies = {
    session_token: '<SESSION_TOKEN>',
    user_session: '<USER_SESSION>',
    csrf_token: '<CSRF_TOKEN>',
    remember_me: '<REMEMBER_ME>',
    language: '<LANGUAGE>'
  };

  const websiteUrl = 'https://example-social.com/feed';
  const userPrompt = 'Extract posts from the feed including author, content, likes, and comments';

  try {
    const response = await smartScraper(
      process.env.SGAI_APIKEY,
      websiteUrl,
      userPrompt,
      SocialMediaPostSchema,
      10, // numberOfScrolls - Scroll to load more posts
      null, // totalPages
      cookies
    );

    console.log('✅ Social media scraping completed successfully');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`❌ Error in social media scraping: ${error.message}`);
  }
}

async function scrapeNewsWithPreferences() {
  console.log('\n' + '='.repeat(60));
  console.log('NEWS SITE SCRAPING WITH USER PREFERENCES');
  console.log('='.repeat(60));

  // Example cookies for a news site
  const cookies = {
    user_preferences: 'technology,science,ai',
    reading_level: 'advanced',
    region: 'US',
    subscription_tier: 'premium',
    theme: 'dark'
  };

  const websiteUrl = 'https://example-news.com/technology';
  const userPrompt = 'Extract news articles including title, summary, author, and publish date';

  try {
    const response = await smartScraper(
      process.env.SGAI_APIKEY,
      websiteUrl,
      userPrompt,
      NewsArticleSchema,
      null, // numberOfScrolls
      3, // totalPages - Scrape multiple pages
      cookies
    );

    console.log('✅ News scraping completed successfully');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`❌ Error in news scraping: ${error.message}`);
  }
}

async function scrapeBankingWithSecureCookies() {
  console.log('\n' + '='.repeat(60));
  console.log('BANKING SITE SCRAPING WITH SECURE COOKIES');
  console.log('='.repeat(60));

  // Example secure cookies for a banking site
  const cookies = {
    secure_session: '<SECURE_SESSION>',
    auth_token: '<AUTH_TOKEN>',
    mfa_verified: '<MFA_VERIFIED>',
    device_id: '<DEVICE_ID>',
    last_activity: '<LAST_ACTIVITY_ISO8601>'
  };

  const websiteUrl = 'https://example-bank.com/transactions';
  const userPrompt = 'Extract recent transactions including date, description, amount, and type';

  try {
    const response = await smartScraper(
      process.env.SGAI_APIKEY,
      websiteUrl,
      userPrompt,
      BankTransactionSchema,
      null, // numberOfScrolls
      5, // totalPages - Scrape multiple pages of transactions
      cookies
    );

    console.log('✅ Banking scraping completed successfully');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`❌ Error in banking scraping: ${error.message}`);
  }
}

async function scrapeApiWithAuthTokens() {
  console.log('\n' + '='.repeat(60));
  console.log('API ENDPOINT SCRAPING WITH AUTH TOKENS');
  console.log('='.repeat(60));

  // Example API authentication cookies
  const cookies = {
    api_token: '<API_TOKEN>',
    client_id: '<CLIENT_ID>',
    access_token: '<ACCESS_TOKEN>',
    refresh_token: '<REFRESH_TOKEN>',
    scope: '<SCOPE>'
  };

  const websiteUrl = 'https://api.example.com/data';
  const userPrompt = 'Extract data from the API response';

  try {
    const response = await smartScraper(
      process.env.SGAI_APIKEY,
      websiteUrl,
      userPrompt,
      null, // No schema for generic API response
      null, // numberOfScrolls
      null, // totalPages
      cookies
    );

    console.log('✅ API scraping completed successfully');
    console.log(JSON.stringify(response, null, 2));

  } catch (error) {
    console.error(`❌ Error in API scraping: ${error.message}`);
  }
}

async function main() {
  const apiKey = process.env.SGAI_APIKEY;

  // Check if API key is available
  if (!apiKey) {
    console.error('Error: SGAI_APIKEY not found in .env file');
    console.log('Please create a .env file with your API key:');
    console.log('SGAI_APIKEY=your_api_key_here');
    return;
  }

  console.log('🍪 COOKIES INTEGRATION EXAMPLES');
  console.log('This demonstrates various real-world scenarios where cookies are essential for web scraping.');

  // Run all examples
  await scrapeEcommerceWithAuth();
  await scrapeSocialMediaWithSession();
  await scrapeNewsWithPreferences();
  await scrapeBankingWithSecureCookies();
  await scrapeApiWithAuthTokens();

  console.log('\n' + '='.repeat(60));
  console.log('✅ All examples completed!');
  console.log('='.repeat(60));
}

// Run the example
main().catch(console.error);
