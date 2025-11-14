import { agenticScraper, getAgenticScraperRequest } from 'scrapegraph-js';
import 'dotenv/config';

const apiKey = process.env.SGAI_APIKEY;

/**
 * Advanced example with input validation and error handling
 */
async function advancedAgenticScrapingExample() {
  console.log('🚀 Advanced Agentic Scraping Example');
  console.log('='.repeat(45));
  
  // Example configurations for different scenarios
  const scenarios = [
    {
      name: 'Social Media Login (No AI)',
      url: 'https://twitter.com/login',
      steps: [
        'click on email input field',
        'type "user@example.com" in email field',
        'click on password input field', 
        'type "password123" in password field',
        'click login button',
        'wait for 3 seconds'
      ],
      useSession: true,
      aiExtraction: false
    },
    {
      name: 'Form Submission with AI Extraction',
      url: 'https://example.com/contact',
      steps: [
        'click on name input',
        'type "John Doe" in name field',
        'click on email input',
        'type "john@example.com" in email field',
        'click on message textarea',
        'type "Hello, this is a test message" in message field',
        'click submit button',
        'wait for confirmation message'
      ],
      useSession: false,
      aiExtraction: true,
      userPrompt: 'Extract the form submission result, confirmation message, and any reference numbers provided',
      outputSchema: {
        submission: {
          type: "object",
          properties: {
            status: { type: "string" },
            message: { type: "string" },
            reference_id: { type: "string" }
          },
          required: ["status", "message"]
        }
      }
    },
    {
      name: 'E-commerce Search with Product Extraction',
      url: 'https://example-store.com',
      steps: [
        'wait for page to load',
        'click on search bar',
        'type "wireless headphones" in search',
        'press Enter key',
        'wait for 2 seconds',
        'click on filter button',
        'select price range $50-$100',
        'click apply filters',
        'scroll down to see more products'
      ],
      useSession: true,
      aiExtraction: true,
      userPrompt: 'Extract product information including names, prices, ratings, and availability from the search results',
      outputSchema: {
        search_results: {
          type: "object",
          properties: {
            products: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  name: { type: "string" },
                  price: { type: "string" },
                  rating: { type: "number" },
                  availability: { type: "string" }
                }
              }
            },
            total_results: { type: "number" },
            current_page: { type: "number" }
          }
        }
      }
    }
  ];
  
  // Run a specific scenario (change index to test different ones)
  const scenario = scenarios[0]; // Social Media Login
  
  try {
    console.log(`\n📋 Running Scenario: ${scenario.name}`);
    console.log(`URL: ${scenario.url}`);
    console.log(`Steps: ${scenario.steps.length} automation actions`);
    console.log(`Use Session: ${scenario.useSession}`);
    console.log(`AI Extraction: ${scenario.aiExtraction}`);
    if (scenario.aiExtraction) {
      console.log(`User Prompt: ${scenario.userPrompt}`);
      console.log(`Output Schema: ${scenario.outputSchema ? 'Provided' : 'None'}`);
    }
    
    // Validate inputs before making the request
    validateInputs(scenario.url, scenario.steps);
    
    console.log('\n✅ Input validation passed');
    console.log('🚀 Submitting agentic scraper request...');
    
    const response = await agenticScraper(
      apiKey, 
      scenario.url, 
      scenario.steps, 
      scenario.useSession,
      scenario.userPrompt || null,
      scenario.outputSchema || null,
      scenario.aiExtraction || false
    );
    
    console.log('✅ Request submitted successfully!');
    console.log(`Request ID: ${response.request_id}`);
    console.log(`Status: ${response.status}`);
    
    // Monitor the request with timeout
    const result = await monitorRequest(response.request_id, 120); // 2 minute timeout
    
    console.log('\n🎉 Automation completed!');
    
    if (scenario.aiExtraction && result.result) {
      console.log('🎯 Extracted Structured Data:');
      console.log(JSON.stringify(result.result, null, 2));
    } else if (result.markdown) {
      console.log('📄 Raw Content (markdown):');
      const preview = result.markdown.length > 500 
        ? result.markdown.substring(0, 500) + '...'
        : result.markdown;
      console.log(preview);
    } else {
      console.log('Final Result:', JSON.stringify(result.result, null, 2));
    }
    
    return result;
    
  } catch (error) {
    console.error(`\n❌ Error in ${scenario.name}:`, error.message);
    
    // Provide helpful error context
    if (error.message.includes('validation')) {
      console.log('\n💡 Validation Tips:');
      console.log('- Ensure URL starts with http:// or https://');
      console.log('- Make sure all steps are non-empty strings');
      console.log('- Check that the steps array is not empty');
    } else if (error.message.includes('timeout')) {
      console.log('\n💡 Timeout Tips:');
      console.log('- Complex automations may take longer');
      console.log('- Consider breaking down into smaller steps');
      console.log('- Check if the target website is responsive');
    }
    
    throw error;
  }
}

/**
 * Input validation function
 */
function validateInputs(url, steps) {
  // Validate URL
  if (!url || typeof url !== 'string') {
    throw new Error('validation: URL must be a non-empty string');
  }
  
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    throw new Error('validation: URL must start with http:// or https://');
  }
  
  // Validate steps
  if (!Array.isArray(steps) || steps.length === 0) {
    throw new Error('validation: Steps must be a non-empty array');
  }
  
  steps.forEach((step, index) => {
    if (!step || typeof step !== 'string' || !step.trim()) {
      throw new Error(`validation: Step ${index + 1} must be a non-empty string`);
    }
  });
  
  console.log(`✅ Validated URL and ${steps.length} steps`);
}

/**
 * Monitor request with timeout and progress updates
 */
async function monitorRequest(requestId, timeoutSeconds = 120) {
  const startTime = Date.now();
  const timeoutMs = timeoutSeconds * 1000;
  let attempts = 0;
  
  console.log(`\n🔄 Monitoring request ${requestId}`);
  console.log(`Timeout: ${timeoutSeconds} seconds`);
  
  while (Date.now() - startTime < timeoutMs) {
    attempts++;
    const elapsed = Math.round((Date.now() - startTime) / 1000);
    
    try {
      console.log(`\n⏳ Check ${attempts} (${elapsed}s elapsed)`);
      
      const status = await getAgenticScraperRequest(apiKey, requestId);
      console.log(`Status: ${status.status}`);
      
      if (status.status === 'completed') {
        const totalTime = Math.round((Date.now() - startTime) / 1000);
        console.log(`✅ Completed in ${totalTime} seconds`);
        return status;
      } else if (status.status === 'failed') {
        throw new Error(`Automation failed: ${status.error}`);
      }
      
      // Wait before next check (progressive backoff)
      const waitTime = Math.min(5000 + (attempts * 1000), 15000); // 5-15 seconds
      console.log(`⏸️  Waiting ${waitTime/1000}s before next check...`);
      await sleep(waitTime);
      
    } catch (error) {
      if (error.message.includes('Automation failed')) {
        throw error;
      }
      console.log(`⚠️  Check failed: ${error.message}`);
      await sleep(5000);
    }
  }
  
  throw new Error(`timeout: Request did not complete within ${timeoutSeconds} seconds`);
}

/**
 * Demonstrate error handling scenarios
 */
async function errorHandlingExamples() {
  console.log('\n🛡️  Error Handling Examples');
  console.log('='.repeat(30));
  
  const errorScenarios = [
    {
      name: 'Invalid URL',
      url: 'not-a-valid-url',
      steps: ['click button'],
      expectedError: 'URL must start with'
    },
    {
      name: 'Empty Steps',
      url: 'https://example.com',
      steps: [],
      expectedError: 'non-empty array'
    },
    {
      name: 'Invalid Step',
      url: 'https://example.com',
      steps: ['valid step', '', 'another valid step'],
      expectedError: 'non-empty string'
    }
  ];
  
  for (const scenario of errorScenarios) {
    try {
      console.log(`\n🧪 Testing: ${scenario.name}`);
      await agenticScraper(apiKey, scenario.url, scenario.steps);
      console.log('❌ Expected error but request succeeded');
    } catch (error) {
      if (error.message.includes(scenario.expectedError)) {
        console.log(`✅ Correctly caught error: ${error.message}`);
      } else {
        console.log(`⚠️  Unexpected error: ${error.message}`);
      }
    }
  }
}

/**
 * Utility function
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Main execution
 */
async function main() {
  if (!apiKey) {
    console.error('❌ Error: SGAI_APIKEY environment variable not set');
    console.log('\nPlease create a .env file with:');
    console.log('SGAI_APIKEY=your-api-key-here');
    process.exit(1);
  }
  
  try {
    // Run the advanced example
    await advancedAgenticScrapingExample();
    
    // Uncomment to test error handling
    // await errorHandlingExamples();
    
    console.log('\n✨ Advanced example completed successfully!');
    
  } catch (error) {
    console.error('\n💥 Advanced example failed:', error.message);
    process.exit(1);
  }
}

// Run the advanced example
main();
