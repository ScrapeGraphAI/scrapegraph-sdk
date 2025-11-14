import { agenticScraper, getAgenticScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

/**
 * Complete example showing how to use agentic scraper for automated login
 * and then retrieve the results
 */
async function completeAgenticScrapingExample() {
  console.log('🤖 Starting Complete Agentic Scraping Example');
  console.log('='.repeat(50));
  
  // Configuration
  const url = 'https://dashboard.scrapegraphai.com/';
  const steps = [
    'Type email@gmail.com in email input box',
    'Type test-password@123 in password inputbox',
    'click on login'
  ];
  const useSession = true;
  
  try {
    // Step 1: Submit the agentic scraper request
    console.log('\n📤 Step 1: Submitting agentic scraper request...');
    console.log('URL:', url);
    console.log('Use Session:', useSession);
    console.log('Steps:', steps.length, 'automation steps');
    
    const submitResponse = await agenticScraper(apiKey, url, steps, useSession);
    
    console.log('✅ Request submitted successfully!');
    console.log('Request ID:', submitResponse.request_id);
    console.log('Initial Status:', submitResponse.status);
    
    const requestId = submitResponse.request_id;
    
    // Step 2: Poll for results
    console.log('\n🔄 Step 2: Polling for results...');
    let attempts = 0;
    const maxAttempts = 12; // 2 minutes max (10 seconds * 12)
    
    while (attempts < maxAttempts) {
      attempts++;
      console.log(`\n⏳ Attempt ${attempts}/${maxAttempts}: Checking status...`);
      
      const statusResponse = await getAgenticScraperRequest(apiKey, requestId);
      console.log('Status:', statusResponse.status);
      
      if (statusResponse.status === 'completed') {
        console.log('\n🎉 Automation completed successfully!');
        console.log('Completed At:', statusResponse.completed_at);
        console.log('Processing Time:', calculateProcessingTime(submitResponse.created_at, statusResponse.completed_at));
        console.log('\n📋 Results:');
        console.log(JSON.stringify(statusResponse.result, null, 2));
        
        return statusResponse;
      } else if (statusResponse.status === 'failed') {
        console.log('\n❌ Automation failed');
        console.log('Error:', statusResponse.error);
        throw new Error(`Automation failed: ${statusResponse.error}`);
      } else {
        console.log('Still processing... waiting 10 seconds');
        await sleep(10000); // Wait 10 seconds
      }
    }
    
    throw new Error('Timeout: Automation took too long to complete');
    
  } catch (error) {
    console.error('\n❌ Error in complete example:', error.message);
    throw error;
  }
}

/**
 * Example with different automation steps
 */
async function ecommerceAutomationExample() {
  console.log('\n🛒 E-commerce Automation Example');
  console.log('='.repeat(40));
  
  const url = 'https://example-shop.com';
  const steps = [
    'click on search input',
    'type "laptop" in search box',
    'click search button',
    'wait for 2 seconds',
    'click on first product',
    'scroll down to reviews section'
  ];
  
  try {
    const response = await agenticScraper(apiKey, url, steps, true);
    console.log('E-commerce automation started:', response.request_id);
    return response;
  } catch (error) {
    console.error('E-commerce automation error:', error.message);
  }
}

/**
 * Utility functions
 */
function calculateProcessingTime(startTime, endTime) {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const diffMs = end - start;
  const diffSeconds = Math.round(diffMs / 1000);
  return `${diffSeconds} seconds`;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main execution
 */
async function main() {
  if (!apiKey) {
    console.error('❌ Error: SGAI_APIKEY environment variable not set');
    console.log('Please set your API key in the .env file:');
    console.log('SGAI_APIKEY=your-api-key-here');
    process.exit(1);
  }
  
  try {
    console.log('🚀 Running Agentic Scraper Examples');
    
    // Run the complete login automation example
    await completeAgenticScrapingExample();
    
    // Uncomment to run the e-commerce example
    // await ecommerceAutomationExample();
    
    console.log('\n✅ All examples completed successfully!');
    
  } catch (error) {
    console.error('\n💥 Example failed:', error.message);
    process.exit(1);
  }
}

// Run the examples
main();
