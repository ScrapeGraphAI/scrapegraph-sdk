import { smartScraper } from 'scrapegraph-js';
import 'dotenv/config';

/**
 * Example demonstrating how to use the SmartScraper with interactive steps.
 * This example shows how to navigate websites like a human user before extracting data.
 * 
 * Interactive steps allow you to:
 * - Click on elements
 * - Fill input fields
 * - Wait for page loads
 * - Navigate through multiple pages
 * - Perform complex user interactions
 */

// Configuration
const apiKey = process.env.SGAI_APIKEY;
const url = 'https://github.com/';
const prompt = 'Extract user profile information';

// Interactive steps for website navigation
const steps = [
  'click on search bar',
  'wait for 500ms',
  'fill email input box with mdehsan873@gmail.com',
  'wait a sec',
  'click on the first result of search',
  'wait for 2 seconds to load the result of search'
];

console.log('🚀 Starting SmartScraper with Interactive Steps...');
console.log(`🌐 Website URL: ${url}`);
console.log(`🎯 User Prompt: ${prompt}`);
console.log(`📋 Interactive Steps: ${steps.length} steps configured`);
console.log('\n' + '='.repeat(60));

// Display interactive steps
console.log('🎯 Interactive Steps to Execute:');
steps.forEach((step, index) => {
  console.log(`  ${index + 1}. ${step}`);
});
console.log('\n' + '='.repeat(60));

// Start timer
const startTime = Date.now();
console.log(`⏱️  Timer started at: ${new Date(startTime).toLocaleTimeString()}`);
console.log('🔄 Processing request with interactive steps...');

try {
  // Make request with interactive steps
  const response = await smartScraper(apiKey, url, prompt, null, null, steps);
  
  // Calculate execution time
  const endTime = Date.now();
  const executionTime = (endTime - startTime) / 1000;
  const executionMinutes = executionTime / 60;
  
  console.log(`⏱️  Timer stopped at: ${new Date(endTime).toLocaleTimeString()}`);
  console.log(`⚡ Total execution time: ${executionTime.toFixed(2)} seconds (${executionMinutes.toFixed(2)} minutes)`);
  console.log(`📊 Performance: ${executionTime.toFixed(1)}s (${executionMinutes.toFixed(1)}m) for ${steps.length} interactive steps`);
  
  // Display results
  console.log('✅ Request completed successfully!');
  console.log(`📊 Request ID: ${response.request_id || 'N/A'}`);
  console.log(`🔄 Status: ${response.status || 'N/A'}`);
  
  if (response.error) {
    console.log(`❌ Error: ${response.error}`);
  } else {
    console.log('\n📋 EXTRACTED DATA:');
    console.log('='.repeat(60));
    
    // Pretty print the result
    if (response.result) {
      console.log(JSON.stringify(response.result, null, 2));
      
      // Display extraction statistics
      console.log('\n📊 EXTRACTION STATISTICS:');
      console.log('-'.repeat(50));
      const resultStr = JSON.stringify(response.result);
      console.log(`📝 Data size: ${resultStr.length} characters`);
      console.log(`🔗 JSON keys: ${typeof response.result === 'object' ? Object.keys(response.result).length : 'N/A'}`);
      console.log(`⚡ Processing speed: ${Math.round(resultStr.length / executionTime)} chars/second`);
      console.log(`🎯 Steps efficiency: ${(executionTime / steps.length).toFixed(2)}s per step`);
    } else {
      console.log('No result data found');
    }
  }
  
} catch (error) {
  const endTime = Date.now();
  const executionTime = (endTime - startTime) / 1000;
  const executionMinutes = executionTime / 60;
  
  console.log(`⏱️  Timer stopped at: ${new Date(endTime).toLocaleTimeString()}`);
  console.log(`⚡ Execution time before error: ${executionTime.toFixed(2)} seconds (${executionMinutes.toFixed(2)} minutes)`);
  console.log(`💥 Error occurred: ${error.message}`);
  console.log('\n🛠️  Troubleshooting:');
  console.log('1. Make sure your .env file contains SGAI_APIKEY');
  console.log('2. Check your internet connection');
  console.log('3. Verify the target website is accessible');
  console.log('4. Ensure you have sufficient credits in your account');
}

// Additional examples of different step patterns
console.log('\n🎯 ADDITIONAL STEP PATTERN EXAMPLES:');
console.log('='.repeat(60));

const stepPatterns = [
  {
    name: 'Authentication Flow',
    description: 'Steps for logging into a website',
    steps: [
      'click on login button',
      'wait for 1 second',
      'fill username field with user@example.com',
      'wait for 200ms',
      'fill password field with password123',
      'wait for 300ms',
      'click submit button',
      'wait for 3 seconds'
    ]
  },
  {
    name: 'Form Interaction',
    description: 'Steps for filling and submitting a form',
    steps: [
      'scroll to contact form',
      'wait for 500ms',
      'fill name field with John Doe',
      'wait for 200ms',
      'fill email field with john@example.com',
      'wait for 200ms',
      'fill message field with Hello World',
      'wait for 300ms',
      'click submit button'
    ]
  },
  {
    name: 'Dynamic Content Loading',
    description: 'Steps for loading more content dynamically',
    steps: [
      'scroll to bottom of page',
      'wait for 1 second',
      'click load more button',
      'wait for 2 seconds',
      'scroll down again',
      'wait for 1 second',
      'click show details button'
    ]
  }
];

stepPatterns.forEach((pattern, index) => {
  console.log(`\n📋 Pattern ${index + 1}: ${pattern.name}`);
  console.log(`📝 Description: ${pattern.description}`);
  console.log(`🎯 Steps (${pattern.steps.length}):`);
  pattern.steps.forEach((step, stepIndex) => {
    const stepType = step.includes('click') ? 'Navigation' : 
                     step.includes('wait') ? 'Wait' : 
                     step.includes('fill') ? 'Input' : 
                     step.includes('scroll') ? 'Action' : 'Other';
    console.log(`   ${stepIndex + 1}. ${step} [${stepType}]`);
  });
  console.log('-'.repeat(40));
});

console.log('\n🎯 SMART SCRAPER INTERACTIVE STEPS EXAMPLE COMPLETED');
console.log('='.repeat(60));
console.log('This example demonstrates how to use interactive steps with SmartScraper.');
console.log('Interactive steps allow you to navigate websites like a human user.');
console.log('This enables more sophisticated data extraction from complex web applications.'); 