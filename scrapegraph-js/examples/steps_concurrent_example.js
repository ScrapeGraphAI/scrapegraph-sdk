import { smartScraper, markdownify } from 'scrapegraph-js';
import fs from 'fs';
import 'dotenv/config';

/**
 * Example demonstrating concurrent usage of SmartScraper and Markdownify with interactive steps.
 * This example shows how to use both functions together with different step configurations.
 */

const apiKey = process.env.SGAI_APIKEY;

// Configuration for different concurrent requests
const requests = [
  {
    type: 'smartScraper',
    name: 'GitHub User Profile Extraction',
    url: 'https://github.com/',
    prompt: 'Extract user profile information',
    steps: [
      'click on search bar',
      'wait for 500ms',
      'fill search with "javascript"',
      'wait for 1 second',
      'click on first user result'
    ]
  },
  {
    type: 'markdownify',
    name: 'ScrapeGraph Documentation',
    url: 'https://scrapegraphai.com/',
    steps: [
      'click on documentation menu',
      'wait for 1 second',
      'scroll down to getting started',
      'wait for 500ms',
      'click on quick start guide'
    ]
  },
  {
    type: 'smartScraper',
    name: 'Repository Details',
    url: 'https://github.com/explore',
    prompt: 'Extract trending repository information',
    steps: [
      'click on trending repositories',
      'wait for 2 seconds',
      'scroll to first repository',
      'wait for 500ms',
      'click on repository link'
    ]
  },
  {
    type: 'markdownify',
    name: 'Blog Content Access',
    url: 'https://scrapegraphai.com/blog/',
    steps: [
      'click on latest blog post',
      'wait for 2 seconds',
      'scroll to full content',
      'wait for 1 second',
      'click read more if available'
    ]
  }
];

console.log('🚀 Starting Concurrent Requests with Interactive Steps...');
console.log(`🔄 Processing ${requests.length} requests concurrently`);
console.log('\n' + '='.repeat(60));

// Display request configurations
console.log('📋 Request Configurations:');
requests.forEach((request, index) => {
  console.log(`\n${index + 1}. ${request.name} [${request.type.toUpperCase()}]`);
  console.log(`   🌐 URL: ${request.url}`);
  if (request.prompt) {
    console.log(`   🎯 Prompt: ${request.prompt}`);
  }
  console.log(`   📝 Steps: ${request.steps.length}`);
  request.steps.forEach((step, stepIndex) => {
    console.log(`       ${stepIndex + 1}. ${step}`);
  });
});

console.log('\n' + '='.repeat(60));

// Start timer
const startTime = Date.now();
console.log(`⏱️  Timer started at: ${new Date(startTime).toLocaleTimeString()}`);
console.log('🔄 Processing concurrent requests...');

try {
  // Create promises for concurrent execution
  const promises = requests.map(async (request, index) => {
    const requestStartTime = Date.now();
    
    let result;
    if (request.type === 'smartScraper') {
      result = await smartScraper(apiKey, request.url, request.prompt, null, null, request.steps);
    } else {
      result = await markdownify(apiKey, request.url, request.steps);
    }
    
    const requestEndTime = Date.now();
    const requestExecutionTime = (requestEndTime - requestStartTime) / 1000;
    
    return {
      index,
      name: request.name,
      type: request.type,
      url: request.url,
      steps: request.steps,
      result,
      executionTime: requestExecutionTime
    };
  });
  
  // Execute all requests concurrently
  const results = await Promise.all(promises);
  
  // Calculate total execution time
  const endTime = Date.now();
  const totalExecutionTime = (endTime - startTime) / 1000;
  
  console.log(`⏱️  Timer stopped at: ${new Date(endTime).toLocaleTimeString()}`);
  console.log(`⚡ Total concurrent execution time: ${totalExecutionTime.toFixed(2)} seconds`);
  console.log(`📊 Average per request: ${(totalExecutionTime / requests.length).toFixed(2)} seconds`);
  console.log(`🚀 Speedup vs sequential: ~${(results.reduce((sum, r) => sum + r.executionTime, 0) / totalExecutionTime).toFixed(1)}x`);
  
  // Display results
  console.log('\n📋 CONCURRENT RESULTS:');
  console.log('='.repeat(60));
  
  results.forEach((result, index) => {
    console.log(`\n${index + 1}. ${result.name}:`);
    console.log(`   🔧 Type: ${result.type.toUpperCase()}`);
    console.log(`   🌐 URL: ${result.url}`);
    console.log(`   📝 Steps: ${result.steps.length}`);
    console.log(`   ⏱️  Execution Time: ${result.executionTime.toFixed(2)}s`);
    
    if (result.result.error) {
      console.log(`   ❌ Error: ${result.result.error}`);
    } else {
      console.log(`   ✅ Status: ${result.result.status || 'N/A'}`);
      console.log(`   📊 Request ID: ${result.result.request_id || 'N/A'}`);
      
      if (result.result.result) {
        if (result.type === 'smartScraper') {
          const dataSize = JSON.stringify(result.result.result).length;
          console.log(`   📝 Data size: ${dataSize} characters`);
          console.log(`   🔗 Data keys: ${typeof result.result.result === 'object' ? Object.keys(result.result.result).length : 'N/A'}`);
        } else {
          const contentLength = result.result.result.length;
          console.log(`   📝 Content size: ${contentLength} characters`);
          
          // Quick content analysis for markdown
          const lines = result.result.result.split('\n');
          const headers = lines.filter(line => line.trim().startsWith('#'));
          console.log(`   📑 Headers found: ${headers.length}`);
          
          // Save markdown to file
          if (result.type === 'markdownify') {
            const filename = `concurrent_${result.name.replace(/\s+/g, '_').toLowerCase()}_${Date.now()}.md`;
            saveMarkdownToFile(result.result.result, filename);
          }
        }
      }
      
      console.log(`   ⚡ Processing speed: ${result.type === 'smartScraper' ? 
        Math.round(JSON.stringify(result.result.result || {}).length / result.executionTime) : 
        Math.round((result.result.result || '').length / result.executionTime)} chars/second`);
      console.log(`   🎯 Steps efficiency: ${(result.executionTime / result.steps.length).toFixed(2)}s per step`);
    }
    
    console.log('-'.repeat(40));
  });
  
  // Summary statistics
  console.log('\n📊 SUMMARY STATISTICS:');
  console.log('='.repeat(60));
  
  const smartScraperResults = results.filter(r => r.type === 'smartScraper');
  const markdownifyResults = results.filter(r => r.type === 'markdownify');
  
  console.log(`📈 Total requests processed: ${results.length}`);
  console.log(`🤖 SmartScraper requests: ${smartScraperResults.length}`);
  console.log(`📝 Markdownify requests: ${markdownifyResults.length}`);
  console.log(`⏱️  Fastest request: ${Math.min(...results.map(r => r.executionTime)).toFixed(2)}s`);
  console.log(`⏱️  Slowest request: ${Math.max(...results.map(r => r.executionTime)).toFixed(2)}s`);
  console.log(`📊 Average execution time: ${(results.reduce((sum, r) => sum + r.executionTime, 0) / results.length).toFixed(2)}s`);
  
  const totalSteps = results.reduce((sum, r) => sum + r.steps.length, 0);
  console.log(`🎯 Total steps executed: ${totalSteps}`);
  console.log(`📈 Average steps per request: ${(totalSteps / results.length).toFixed(1)}`);
  
  if (smartScraperResults.length > 0) {
    const avgSmartScraperTime = smartScraperResults.reduce((sum, r) => sum + r.executionTime, 0) / smartScraperResults.length;
    console.log(`🤖 SmartScraper average time: ${avgSmartScraperTime.toFixed(2)}s`);
  }
  
  if (markdownifyResults.length > 0) {
    const avgMarkdownifyTime = markdownifyResults.reduce((sum, r) => sum + r.executionTime, 0) / markdownifyResults.length;
    console.log(`📝 Markdownify average time: ${avgMarkdownifyTime.toFixed(2)}s`);
  }
  
} catch (error) {
  const endTime = Date.now();
  const executionTime = (endTime - startTime) / 1000;
  
  console.log(`⏱️  Timer stopped at: ${new Date(endTime).toLocaleTimeString()}`);
  console.log(`⚡ Execution time before error: ${executionTime.toFixed(2)} seconds`);
  console.log(`💥 Error occurred: ${error.message}`);
  console.log('\n🛠️  Troubleshooting:');
  console.log('1. Make sure your .env file contains SGAI_APIKEY');
  console.log('2. Check your internet connection');
  console.log('3. Verify the target websites are accessible');
  console.log('4. Ensure you have sufficient credits in your account');
  
  console.log('\n🎯 CONCURRENT STEPS EXAMPLE TERMINATED');
  console.log('='.repeat(60));
  console.log('This example demonstrates the power of concurrent execution with interactive steps.');
  console.log('Both SmartScraper and Markdownify can be used together for comprehensive web processing.');
  console.log('Interactive steps enable sophisticated navigation patterns for better data extraction.');
  return;
}

/**
 * Save markdown content to a file.
 * @param {string} content - The markdown content to save
 * @param {string} filename - The filename to save to
 */
function saveMarkdownToFile(content, filename) {
  try {
    fs.writeFileSync(filename, content, 'utf8');
    console.log(`   💾 Saved to: ${filename}`);
  } catch (error) {
    console.log(`   ❌ Error saving file: ${error.message}`);
  }
}

console.log('\n🎯 CONCURRENT STEPS EXAMPLE COMPLETED');
console.log('='.repeat(60));
console.log('This example demonstrates the power of concurrent execution with interactive steps.');
console.log('Both SmartScraper and Markdownify can be used together for comprehensive web processing.');
console.log('Interactive steps enable sophisticated navigation patterns for better data extraction.'); 