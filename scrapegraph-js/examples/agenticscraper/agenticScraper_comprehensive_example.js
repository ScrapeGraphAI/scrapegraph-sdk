#!/usr/bin/env node

/**
 * Comprehensive Agentic Scraper Example
 *
 * This example demonstrates how to use the agentic scraper API endpoint
 * to perform automated browser actions and scrape content with both
 * AI extraction and non-AI extraction modes.
 *
 * The agentic scraper can:
 * 1. Navigate to a website
 * 2. Perform a series of automated actions (like filling forms, clicking buttons)
 * 3. Extract the resulting HTML content as markdown
 * 4. Optionally use AI to extract structured data
 *
 * Usage:
 *     node examples/agenticScraper_comprehensive_example.js
 */

import { agenticScraper, getAgenticScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';
import fs from 'fs/promises';

const apiKey = process.env.SGAI_APIKEY;

/**
 * Helper function to poll for request completion
 * @param {string} requestId - The request ID to poll
 * @param {number} maxAttempts - Maximum number of polling attempts
 * @param {number} delayMs - Delay between polling attempts in milliseconds
 * @returns {Promise<Object>} The final result
 */
async function pollForCompletion(requestId, maxAttempts = 12, delayMs = 10000) {
  let attempts = 0;
  
  while (attempts < maxAttempts) {
    attempts++;
    console.log(`🔄 Polling attempt ${attempts}/${maxAttempts}...`);
    
    try {
      const result = await getAgenticScraperRequest(apiKey, requestId);
      
      if (result.status === 'completed') {
        console.log('✅ Request completed!');
        return result;
      } else if (result.status === 'failed') {
        console.log('❌ Request failed:', result.error || 'Unknown error');
        return result;
      } else {
        console.log(`⏳ Status: ${result.status}, waiting ${delayMs/1000} seconds...`);
        await new Promise(resolve => setTimeout(resolve, delayMs));
      }
    } catch (error) {
      console.log(`⚠️ Polling error: ${error.message}`);
      if (attempts === maxAttempts) throw error;
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }
  }
  
  throw new Error('Request timed out - maximum polling attempts reached');
}

/**
 * Example: Basic agentic scraping without AI extraction
 */
async function exampleBasicScrapingNoAI() {
  console.log('🚀 Starting basic agentic scraping (no AI extraction)...');
  
  const url = 'https://dashboard.scrapegraphai.com/';
  const steps = [
    'Type email@gmail.com in email input box',
    'Type test-password@123 in password inputbox',
    'click on login',
  ];

  try {
    console.log(`URL: ${url}`);
    console.log(`Steps: ${JSON.stringify(steps, null, 2)}`);

    // Perform the scraping without AI extraction
    const submitResponse = await agenticScraper(
      apiKey,
      url,
      steps,
      true,     // useSession
      null,     // userPrompt (not needed)
      null,     // outputSchema (not needed)
      false     // aiExtraction = false
    );

    console.log('✅ Basic scraping request submitted!');
    console.log(`Request ID: ${submitResponse.request_id}`);

    // Poll for completion
    const result = await pollForCompletion(submitResponse.request_id);

    if (result.status === 'completed') {
      // Save the markdown content to a file
      if (result.markdown) {
        await fs.writeFile('basic_scraped_content.md', result.markdown, 'utf-8');
        console.log('📄 Markdown content saved to "basic_scraped_content.md"');
      }

      // Print a preview of the content
      if (result.markdown) {
        const preview = result.markdown.length > 500 
          ? result.markdown.substring(0, 500) + '...'
          : result.markdown;
        console.log(`\n📝 Content Preview:\n${preview}`);
      }

      if (result.error) {
        console.log(`⚠️ Warning: ${result.error}`);
      }
    }

    return result;

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return null;
  }
}

/**
 * Example: Use AI extraction to get structured data from dashboard
 */
async function exampleAIExtraction() {
  console.log('🤖 Starting agentic scraping with AI extraction...');

  const url = 'https://dashboard.scrapegraphai.com/';
  const steps = [
    'Type email@gmail.com in email input box',
    'Type test-password@123 in password inputbox',
    'click on login',
    'wait for dashboard to load completely',
  ];

  // Define extraction schema for user dashboard information
  const outputSchema = {
    user_info: {
      type: "object",
      properties: {
        username: { type: "string" },
        email: { type: "string" },
        dashboard_sections: {
          type: "array",
          items: { type: "string" }
        },
        account_status: { type: "string" },
        credits_remaining: { type: "number" }
      },
      required: ["username", "dashboard_sections"]
    }
  };

  const userPrompt = "Extract user information, available dashboard sections, account status, and remaining credits from the dashboard";

  try {
    console.log(`URL: ${url}`);
    console.log(`Steps: ${JSON.stringify(steps, null, 2)}`);
    console.log(`User Prompt: ${userPrompt}`);

    const submitResponse = await agenticScraper(
      apiKey,
      url,
      steps,
      true,         // useSession
      userPrompt,   // userPrompt for AI extraction
      outputSchema, // outputSchema for structured data
      true          // aiExtraction = true
    );

    console.log('✅ AI extraction request submitted!');
    console.log(`Request ID: ${submitResponse.request_id}`);

    // Poll for completion
    const result = await pollForCompletion(submitResponse.request_id);

    if (result.status === 'completed') {
      if (result.result) {
        console.log('🎯 Extracted Structured Data:');
        console.log(JSON.stringify(result.result, null, 2));
        
        // Save extracted data to JSON file
        await fs.writeFile('extracted_dashboard_data.json', JSON.stringify(result.result, null, 2), 'utf-8');
        console.log('💾 Structured data saved to "extracted_dashboard_data.json"');
      }

      // Also save the raw markdown if available
      if (result.markdown) {
        await fs.writeFile('ai_scraped_content.md', result.markdown, 'utf-8');
        console.log('📄 Raw markdown also saved to "ai_scraped_content.md"');
      }
    }

    return result;

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return null;
  }
}

/**
 * Example: Scraping an e-commerce site for product information
 */
async function exampleEcommerceProductScraping() {
  console.log('🛒 Scraping e-commerce products with AI extraction...');

  const url = 'https://example-ecommerce.com';
  const steps = [
    'click on search box',
    'type "laptop" in search box',
    'press enter',
    'wait for search results to load',
    'scroll down 3 times to load more products',
  ];

  const outputSchema = {
    products: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string" },
          price: { type: "string" },
          rating: { type: "number" },
          availability: { type: "string" },
          description: { type: "string" },
          image_url: { type: "string" }
        },
        required: ["name", "price"]
      }
    },
    search_info: {
      type: "object",
      properties: {
        total_results: { type: "number" },
        search_term: { type: "string" },
        page: { type: "number" }
      }
    }
  };

  const userPrompt = "Extract all visible product information including names, prices, ratings, availability status, descriptions, and image URLs. Also extract search metadata like total results and current page.";

  try {
    console.log(`URL: ${url}`);
    console.log(`Steps: ${JSON.stringify(steps, null, 2)}`);

    const submitResponse = await agenticScraper(
      apiKey,
      url,
      steps,
      true,
      userPrompt,
      outputSchema,
      true
    );

    console.log('✅ E-commerce scraping request submitted!');
    console.log(`Request ID: ${submitResponse.request_id}`);

    // Poll for completion
    const result = await pollForCompletion(submitResponse.request_id);

    if (result.status === 'completed' && result.result) {
      const products = result.result.products || [];
      const searchInfo = result.result.search_info || {};
      
      console.log(`🔍 Search Results for "${searchInfo.search_term || 'laptop'}":`);
      console.log(`📊 Total Results: ${searchInfo.total_results || 'Unknown'}`);
      console.log(`📄 Current Page: ${searchInfo.page || 'Unknown'}`);
      console.log(`🛍️ Products Found: ${products.length}`);
      
      console.log('\n📦 Product Details:');
      products.slice(0, 5).forEach((product, index) => {
        console.log(`\n${index + 1}. ${product.name || 'N/A'}`);
        console.log(`   💰 Price: ${product.price || 'N/A'}`);
        console.log(`   ⭐ Rating: ${product.rating || 'N/A'}`);
        console.log(`   📦 Availability: ${product.availability || 'N/A'}`);
        if (product.description) {
          const desc = product.description.length > 100 
            ? product.description.substring(0, 100) + '...'
            : product.description;
          console.log(`   📝 Description: ${desc}`);
        }
      });
      
      // Save extracted data
      await fs.writeFile('ecommerce_products.json', JSON.stringify(result.result, null, 2), 'utf-8');
      console.log('\n💾 Product data saved to "ecommerce_products.json"');
    }

    return result;

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return null;
  }
}

/**
 * Example: Fill out a contact form and extract confirmation details
 */
async function exampleFormFillingAndDataExtraction() {
  console.log('📝 Filling contact form and extracting confirmation...');

  const url = 'https://example-company.com/contact';
  const steps = [
    'find and click on contact form',
    'type "John Doe" in name field',
    'type "john.doe@example.com" in email field',
    'type "Product Inquiry" in subject field',
    'type "I am interested in your premium plan. Could you provide more details about pricing and features?" in message field',
    'click submit button',
    'wait for confirmation message to appear',
  ];

  const outputSchema = {
    form_submission: {
      type: "object",
      properties: {
        status: { type: "string" },
        confirmation_message: { type: "string" },
        reference_number: { type: "string" },
        estimated_response_time: { type: "string" },
        submitted_data: {
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            subject: { type: "string" }
          }
        }
      },
      required: ["status", "confirmation_message"]
    }
  };

  const userPrompt = "Extract the form submission status, confirmation message, any reference numbers, estimated response time, and echo back the submitted form data";

  try {
    console.log(`URL: ${url}`);
    console.log(`Steps: ${JSON.stringify(steps, null, 2)}`);

    const submitResponse = await agenticScraper(
      apiKey,
      url,
      steps,
      true,
      userPrompt,
      outputSchema,
      true
    );

    console.log('✅ Form submission request submitted!');
    console.log(`Request ID: ${submitResponse.request_id}`);

    // Poll for completion
    const result = await pollForCompletion(submitResponse.request_id);

    if (result.status === 'completed' && result.result) {
      const formData = result.result.form_submission || {};
      
      console.log('📋 Form Submission Results:');
      console.log(`   ✅ Status: ${formData.status || 'Unknown'}`);
      console.log(`   💬 Message: ${formData.confirmation_message || 'No message'}`);
      
      if (formData.reference_number) {
        console.log(`   🔢 Reference: ${formData.reference_number}`);
      }
      
      if (formData.estimated_response_time) {
        console.log(`   ⏰ Response Time: ${formData.estimated_response_time}`);
      }
      
      const submittedData = formData.submitted_data || {};
      if (Object.keys(submittedData).length > 0) {
        console.log('\n📤 Submitted Data:');
        Object.entries(submittedData).forEach(([key, value]) => {
          console.log(`   ${key.charAt(0).toUpperCase() + key.slice(1)}: ${value}`);
        });
      }
      
      // Save form results
      await fs.writeFile('form_submission_results.json', JSON.stringify(result.result, null, 2), 'utf-8');
      console.log('\n💾 Form results saved to "form_submission_results.json"');
    }

    return result;

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
    return null;
  }
}

/**
 * Main function to run all examples
 */
async function main() {
  console.log('🔧 Comprehensive Agentic Scraper Examples');
  console.log('='.repeat(60));

  // Check if API key is set
  if (!apiKey) {
    console.error('❌ Error: SGAI_APIKEY environment variable not set');
    console.log('Please either:');
    console.log('  1. Set environment variable: export SGAI_APIKEY=your-api-key-here');
    console.log('  2. Create a .env file with: SGAI_APIKEY=your-api-key-here');
    process.exit(1);
  }

  try {
    console.log('\n1. Basic Scraping (No AI Extraction)');
    console.log('-'.repeat(40));
    await exampleBasicScrapingNoAI();

    console.log('\n\n2. AI Extraction Example - Dashboard Data');
    console.log('-'.repeat(40));
    await exampleAIExtraction();

    console.log('\n\n3. E-commerce Product Scraping with AI');
    console.log('-'.repeat(40));
    // Uncomment to run e-commerce example
    // await exampleEcommerceProductScraping();

    console.log('\n\n4. Form Filling and Confirmation Extraction');
    console.log('-'.repeat(40));
    // Uncomment to run form filling example
    // await exampleFormFillingAndDataExtraction();

    console.log('\n✨ Examples completed!');
    console.log('\nℹ️ Note: Some examples are commented out by default.');
    console.log('   Uncomment them in the main function to run additional examples.');

  } catch (error) {
    console.error(`❌ Fatal error: ${error.message}`);
    process.exit(1);
  }
}

// Run the main function if this script is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
