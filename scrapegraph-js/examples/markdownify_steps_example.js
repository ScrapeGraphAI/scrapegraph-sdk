import { markdownify, getMarkdownifyRequest } from 'scrapegraph-js';
import fs from 'fs';
import 'dotenv/config';

/**
 * Example demonstrating how to use the Markdownify with interactive steps.
 * This example shows how to navigate websites before converting to markdown.
 * 
 * Interactive steps allow you to:
 * - Navigate to specific sections before conversion
 * - Click on elements to expand content
 * - Fill forms to access gated content
 * - Wait for dynamic content to load
 * - Perform authentication flows
 */

// Configuration
const apiKey = process.env.SGAI_APIKEY;
const url = 'https://scrapegraphai.com/';

// Interactive steps for website navigation before markdown conversion
const steps = [
  'click on search bar',
  'wait for 500ms',
  'fill email input box with mdehsan873@gmail.com',
  'wait a sec',
  'click on the first result of search',
  'wait for 2 seconds to load the result of search'
];

console.log('🚀 Starting Markdownify with Interactive Steps...');
console.log(`🌐 Website URL: ${url}`);
console.log(`🎯 Interactive Steps: ${steps.length} steps configured`);
console.log('📝 Goal: Convert website to clean markdown format after navigation');
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
console.log('🔄 Processing markdown conversion with interactive steps...');

try {
  // Make request with interactive steps
  const response = await markdownify(apiKey, url, steps);
  
  // Calculate execution time
  const endTime = Date.now();
  const executionTime = (endTime - startTime) / 1000;
  const executionMinutes = executionTime / 60;
  
  console.log(`⏱️  Timer stopped at: ${new Date(endTime).toLocaleTimeString()}`);
  console.log(`⚡ Total execution time: ${executionTime.toFixed(2)} seconds (${executionMinutes.toFixed(2)} minutes)`);
  console.log(`📊 Performance: ${executionTime.toFixed(1)}s (${executionMinutes.toFixed(1)}m) for markdown conversion with ${steps.length} steps`);
  
  // Display results
  const markdownContent = response.result || '';
  console.log('✅ Request completed successfully!');
  console.log(`📊 Request ID: ${response.request_id || 'N/A'}`);
  console.log(`🔄 Status: ${response.status || 'N/A'}`);
  console.log(`📝 Content Length: ${markdownContent.length} characters`);
  
  if (response.error) {
    console.log(`❌ Error: ${response.error}`);
  } else {
    console.log('\n📋 MARKDOWN CONVERSION RESULTS:');
    console.log('='.repeat(60));
    
    // Display markdown statistics
    const lines = markdownContent.split('\n');
    const words = markdownContent.split(/\s+/).filter(word => word.length > 0);
    console.log('📊 Statistics:');
    console.log(`   - Total Lines: ${lines.length}`);
    console.log(`   - Total Words: ${words.length}`);
    console.log(`   - Total Characters: ${markdownContent.length}`);
    console.log(`   - Processing Speed: ${Math.round(markdownContent.length / executionTime)} chars/second`);
    console.log(`   - Steps Efficiency: ${(executionTime / steps.length).toFixed(2)}s per step`);
    
    // Display first 500 characters
    console.log('\n🔍 First 500 characters:');
    console.log('-'.repeat(50));
    console.log(markdownContent.substring(0, 500));
    if (markdownContent.length > 500) {
      console.log('...');
    }
    console.log('-'.repeat(50));
    
    // Save to file
    const filename = `markdownify_steps_output_${Date.now()}.md`;
    saveMarkdownToFile(markdownContent, filename);
    
    // Display content analysis
    analyzeMarkdownContent(markdownContent, steps);
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

/**
 * Save markdown content to a file with enhanced error handling.
 * @param {string} markdownContent - The markdown content to save
 * @param {string} filename - The name of the file to save to
 */
function saveMarkdownToFile(markdownContent, filename) {
  try {
    fs.writeFileSync(filename, markdownContent, 'utf8');
    console.log(`💾 Markdown saved to: ${filename}`);
  } catch (error) {
    console.log(`❌ Error saving file: ${error.message}`);
  }
}

/**
 * Analyze the markdown content and provide insights.
 * @param {string} markdownContent - The markdown content to analyze
 * @param {string[]} steps - The interactive steps that were executed
 */
function analyzeMarkdownContent(markdownContent, steps) {
  console.log('\n🔍 CONTENT ANALYSIS:');
  console.log('-'.repeat(50));
  
  // Count different markdown elements
  const lines = markdownContent.split('\n');
  const headers = lines.filter(line => line.trim().startsWith('#'));
  const links = lines.filter(line => line.includes('[') && line.includes(']('));
  const codeBlocks = (markdownContent.match(/```/g) || []).length / 2; // Divide by 2 since each block has opening and closing
  
  console.log(`📑 Headers found: ${headers.length}`);
  console.log(`🔗 Links found: ${links.length}`);
  console.log(`💻 Code blocks: ${Math.floor(codeBlocks)}`);
  console.log(`🎯 Interactive steps executed: ${steps.length}`);
  
  // Show first few headers if they exist
  if (headers.length > 0) {
    console.log('\n📋 First few headers:');
    headers.slice(0, 3).forEach((header, index) => {
      console.log(`   ${index + 1}. ${header.trim()}`);
    });
    if (headers.length > 3) {
      console.log(`   ... and ${headers.length - 3} more`);
    }
  }
  
  // Show which steps might have contributed to content
  console.log('\n🔧 Steps Analysis:');
  steps.forEach((step, index) => {
    const stepType = step.includes('click') ? 'Navigation' : 
                     step.includes('wait') ? 'Wait' : 
                     step.includes('fill') ? 'Input' : 
                     step.includes('scroll') ? 'Action' : 'Other';
    console.log(`   ${index + 1}. ${step} [${stepType}]`);
  });
}

// Multiple scenarios demonstration
console.log('\n🎯 MULTIPLE SCENARIOS DEMONSTRATION');
console.log('='.repeat(60));

const scenarios = [
  {
    name: 'Documentation Navigation',
    url: 'https://docs.scrapegraphai.com/',
    steps: [
      'click on getting started menu',
      'wait for 1 second',
      'scroll down to examples section',
      'wait for 500ms',
      'click on first example'
    ]
  },
  {
    name: 'Blog Content Access',
    url: 'https://scrapegraphai.com/blog/',
    steps: [
      'click on latest blog post',
      'wait for 2 seconds',
      'scroll to full content',
      'wait for 1 second',
      'click read more if available'
    ]
  },
  {
    name: 'Product Information',
    url: 'https://scrapegraphai.com/',
    steps: [
      'click on features menu',
      'wait for 500ms',
      'scroll to pricing section',
      'wait for 1 second',
      'click on enterprise plan'
    ]
  }
];

scenarios.forEach((scenario, index) => {
  console.log(`\n📋 Scenario ${index + 1}: ${scenario.name}`);
  console.log(`🌐 URL: ${scenario.url}`);
  console.log(`📝 Steps: ${scenario.steps.length}`);
  scenario.steps.forEach((step, stepIndex) => {
    console.log(`    ${stepIndex + 1}. ${step}`);
  });
  console.log('-'.repeat(40));
});

// Step patterns demonstration
console.log('\n🎯 MARKDOWNIFY STEP PATTERNS DEMONSTRATION');
console.log('='.repeat(60));

const stepPatterns = [
  {
    name: 'SPA Navigation',
    description: 'Steps for navigating Single Page Applications',
    steps: [
      'wait for 2 seconds for page load',
      'click on main menu',
      'wait for 1 second',
      'click on about section',
      'wait for 1 second',
      'scroll to footer'
    ]
  },
  {
    name: 'Content Expansion',
    description: 'Steps for expanding collapsible content',
    steps: [
      'click on show more button',
      'wait for 500ms',
      'click on expand all',
      'wait for 1 second',
      'click on details tab',
      'wait for 1 second'
    ]
  },
  {
    name: 'Cookie Consent & Content Access',
    description: 'Steps for handling cookie consent before content access',
    steps: [
      'wait for 1 second',
      'click on accept cookies',
      'wait for 500ms',
      'click on continue reading',
      'wait for 2 seconds',
      'scroll to main content'
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

console.log('\n🎯 MARKDOWNIFY INTERACTIVE STEPS EXAMPLE COMPLETED');
console.log('='.repeat(60));
console.log('This example demonstrates how to use interactive steps with Markdownify.');
console.log('Interactive steps allow you to navigate to specific content before conversion.');
console.log('This is useful for accessing gated content, expanding sections, or navigating SPAs.'); 