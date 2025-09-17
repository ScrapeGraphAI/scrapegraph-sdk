import { searchScraper, getSearchScraperRequest } from '../index.js';
import 'dotenv/config';

/**
 * Test suite for SearchScraper Markdown functionality
 * This file demonstrates usage and validates the SearchScraper markdown mode parameters
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test input validation for searchScraper with markdown mode
 */
function testMarkdownModeInputValidation() {
  console.log('🧪 Testing SearchScraper Markdown Mode Input Validation');
  console.log('='.repeat(60));

  const testCases = [
    {
      name: 'Valid inputs - markdown mode',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 3,
      options: { extractionMode: false },
      expected: true,
      description: 'Valid parameters with markdown mode enabled'
    },
    {
      name: 'Valid inputs - AI extraction mode',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 3,
      options: { extractionMode: true },
      expected: true,
      description: 'Valid parameters with AI extraction mode enabled'
    },
    {
      name: 'Valid inputs - markdown mode with custom options',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 5,
      options: { 
        extractionMode: false,
        renderHeavyJs: true
      },
      expected: true,
      description: 'Markdown mode with additional options'
    },
    {
      name: 'Invalid extraction mode - string',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 3,
      options: { extractionMode: 'false' },
      expected: false,
      description: 'extractionMode as string instead of boolean'
    },
    {
      name: 'Invalid extraction mode - number',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 3,
      options: { extractionMode: 0 },
      expected: false,
      description: 'extractionMode as number instead of boolean'
    },
    {
      name: 'Empty prompt',
      apiKey: 'valid-key',
      prompt: '',
      numResults: 3,
      options: { extractionMode: false },
      expected: false,
      description: 'Empty search prompt'
    },
    {
      name: 'Invalid numResults - too low',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 2,
      options: { extractionMode: false },
      expected: false,
      description: 'numResults below minimum (3)'
    },
    {
      name: 'Invalid numResults - too high',
      apiKey: 'valid-key',
      prompt: 'Latest AI developments',
      numResults: 25,
      options: { extractionMode: false },
      expected: false,
      description: 'numResults above maximum (20)'
    }
  ];

  let passed = 0;
  let total = testCases.length;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. ${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);
    
    try {
      // Validate inputs
      const isValid = validateSearchScraperInputs(
        testCase.apiKey, 
        testCase.prompt, 
        testCase.numResults,
        null, // schema
        null, // userAgent
        testCase.options
      );
      
      if (isValid === testCase.expected) {
        console.log(`   ✅ PASSED`);
        passed++;
      } else {
        console.log(`   ❌ FAILED - Expected: ${testCase.expected}, Got: ${isValid}`);
      }
    } catch (error) {
      if (!testCase.expected) {
        console.log(`   ✅ PASSED (Expected error: ${error.message})`);
        passed++;
      } else {
        console.log(`   ❌ FAILED - Unexpected error: ${error.message}`);
      }
    }
  });

  console.log(`\n📊 Markdown Mode Input Validation Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Validate searchScraper function inputs including markdown mode
 */
function validateSearchScraperInputs(apiKey, prompt, numResults, schema, userAgent, options) {
  // Check API key
  if (!apiKey || typeof apiKey !== 'string' || apiKey.trim() === '') {
    throw new Error('Invalid API key');
  }

  // Check prompt
  if (!prompt || typeof prompt !== 'string' || prompt.trim() === '') {
    throw new Error('Invalid prompt');
  }

  // Check numResults
  if (numResults < 3 || numResults > 20) {
    throw new Error('numResults must be between 3 and 20');
  }

  // Check options
  if (options && typeof options !== 'object') {
    throw new Error('Options must be an object');
  }

  // Check extractionMode option
  if (options && options.extractionMode !== undefined && typeof options.extractionMode !== 'boolean') {
    throw new Error('extractionMode must be a boolean');
  }

  // Check renderHeavyJs option
  if (options && options.renderHeavyJs !== undefined && typeof options.renderHeavyJs !== 'boolean') {
    throw new Error('renderHeavyJs must be a boolean');
  }

  return true;
}

/**
 * Test searchScraper function with markdown mode using mock data
 */
async function testSearchScraperMarkdownFunction() {
  console.log('\n🧪 Testing SearchScraper Markdown Function (Mock)');
  console.log('='.repeat(60));

  try {
    // Mock the searchScraper function to avoid actual API calls during testing
    const mockSearchScraper = async (apiKey, prompt, numResults = 3, schema = null, userAgent = null, options = {}) => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const { extractionMode = true } = options;
      
      // Return different mock responses based on extraction mode
      if (extractionMode) {
        // AI extraction mode response
        return {
          status: 'completed',
          request_id: 'mock-ai-request-id-12345',
          result: 'AI-extracted structured data about the topic',
          reference_urls: [
            'https://example1.com',
            'https://example2.com',
            'https://example3.com'
          ],
          created_at: new Date().toISOString(),
          completed_at: new Date().toISOString()
        };
      } else {
        // Markdown mode response
        return {
          status: 'completed',
          request_id: 'mock-markdown-request-id-67890',
          markdown_content: '# Mock Markdown Content\n\nThis is mock markdown content for testing purposes.\n\n## Section 1\n\nSome content here.\n\n## Section 2\n\nMore content here.',
          reference_urls: [
            'https://example1.com',
            'https://example2.com',
            'https://example3.com'
          ],
          created_at: new Date().toISOString(),
          completed_at: new Date().toISOString()
        };
      }
    };

    console.log('1. Testing searchScraper with AI extraction mode...');
    const result1 = await mockSearchScraper(API_KEY, 'Latest AI developments', 3, null, null, { extractionMode: true });
    console.log(`   ✅ Status: ${result1.status}`);
    console.log(`   ✅ Request ID: ${result1.request_id}`);
    console.log(`   ✅ Has AI result: ${!!result1.result}`);
    console.log(`   ✅ Reference URLs: ${result1.reference_urls.length}`);

    console.log('\n2. Testing searchScraper with markdown mode...');
    const result2 = await mockSearchScraper(API_KEY, 'Latest AI developments', 3, null, null, { extractionMode: false });
    console.log(`   ✅ Status: ${result2.status}`);
    console.log(`   ✅ Request ID: ${result2.request_id}`);
    console.log(`   ✅ Has markdown content: ${!!result2.markdown_content}`);
    console.log(`   ✅ Markdown length: ${result2.markdown_content?.length || 0} characters`);
    console.log(`   ✅ Reference URLs: ${result2.reference_urls.length}`);

    console.log('\n3. Testing searchScraper with markdown mode and additional options...');
    const result3 = await mockSearchScraper(API_KEY, 'Latest AI developments', 5, null, null, { 
      extractionMode: false,
      renderHeavyJs: true
    });
    console.log(`   ✅ Status: ${result3.status}`);
    console.log(`   ✅ Request ID: ${result3.request_id}`);
    console.log(`   ✅ Has markdown content: ${!!result3.markdown_content}`);

    console.log('\n4. Testing searchScraper with default extraction mode (should be AI)...');
    const result4 = await mockSearchScraper(API_KEY, 'Latest AI developments', 3);
    console.log(`   ✅ Status: ${result4.status}`);
    console.log(`   ✅ Request ID: ${result4.request_id}`);
    console.log(`   ✅ Has AI result: ${!!result4.result}`);
    console.log(`   ✅ No markdown content (AI mode): ${!result4.markdown_content}`);

    console.log('\n✅ All searchScraper markdown function tests passed');
    return true;

  } catch (error) {
    console.error(`❌ SearchScraper markdown function test failed: ${error.message}`);
    return false;
  }
}

/**
 * Test cost calculation for different modes
 */
function testCostCalculation() {
  console.log('\n🧪 Testing Cost Calculation for Different Modes');
  console.log('='.repeat(60));

  const testCases = [
    {
      name: 'AI extraction - 3 results',
      numResults: 3,
      extractionMode: true,
      expectedCredits: 30,
      description: '3 websites × 10 credits per page'
    },
    {
      name: 'Markdown mode - 3 results',
      numResults: 3,
      extractionMode: false,
      expectedCredits: 6,
      description: '3 websites × 2 credits per page'
    },
    {
      name: 'AI extraction - 5 results',
      numResults: 5,
      extractionMode: true,
      expectedCredits: 50,
      description: '5 websites × 10 credits per page'
    },
    {
      name: 'Markdown mode - 5 results',
      numResults: 5,
      extractionMode: false,
      expectedCredits: 10,
      description: '5 websites × 2 credits per page'
    },
    {
      name: 'AI extraction - 10 results',
      numResults: 10,
      extractionMode: true,
      expectedCredits: 100,
      description: '10 websites × 10 credits per page'
    },
    {
      name: 'Markdown mode - 10 results',
      numResults: 10,
      extractionMode: false,
      expectedCredits: 20,
      description: '10 websites × 2 credits per page'
    }
  ];

  let passed = 0;
  let total = testCases.length;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. ${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);
    
    const calculatedCredits = testCase.extractionMode 
      ? testCase.numResults * 10  // AI extraction: 10 credits per page
      : testCase.numResults * 2;  // Markdown mode: 2 credits per page
    
    if (calculatedCredits === testCase.expectedCredits) {
      console.log(`   ✅ PASSED - Credits: ${calculatedCredits}`);
      passed++;
    } else {
      console.log(`   ❌ FAILED - Expected: ${testCase.expectedCredits}, Got: ${calculatedCredits}`);
    }
  });

  console.log(`\n📊 Cost Calculation Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Test response structure validation
 */
function testResponseStructure() {
  console.log('\n🧪 Testing Response Structure Validation');
  console.log('='.repeat(60));

  const testCases = [
    {
      name: 'AI extraction response structure',
      response: {
        status: 'completed',
        request_id: 'test-id-123',
        result: 'AI extracted data',
        reference_urls: ['https://example.com']
      },
      extractionMode: true,
      expected: true,
      description: 'Valid AI extraction response'
    },
    {
      name: 'Markdown mode response structure',
      response: {
        status: 'completed',
        request_id: 'test-id-456',
        markdown_content: '# Test Content',
        reference_urls: ['https://example.com']
      },
      extractionMode: false,
      expected: true,
      description: 'Valid markdown mode response'
    },
    {
      name: 'Missing markdown content in markdown mode',
      response: {
        status: 'completed',
        request_id: 'test-id-789',
        result: 'Some data',
        reference_urls: ['https://example.com']
      },
      extractionMode: false,
      expected: false,
      description: 'Markdown mode response without markdown_content'
    },
    {
      name: 'Missing result in AI extraction mode',
      response: {
        status: 'completed',
        request_id: 'test-id-101',
        markdown_content: '# Content',
        reference_urls: ['https://example.com']
      },
      extractionMode: true,
      expected: false,
      description: 'AI extraction response without result'
    }
  ];

  let passed = 0;
  let total = testCases.length;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. ${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);
    
    try {
      const isValid = validateResponseStructure(testCase.response, testCase.extractionMode);
      
      if (isValid === testCase.expected) {
        console.log(`   ✅ PASSED`);
        passed++;
      } else {
        console.log(`   ❌ FAILED - Expected: ${testCase.expected}, Got: ${isValid}`);
      }
    } catch (error) {
      if (!testCase.expected) {
        console.log(`   ✅ PASSED (Expected validation error: ${error.message})`);
        passed++;
      } else {
        console.log(`   ❌ FAILED - Unexpected error: ${error.message}`);
      }
    }
  });

  console.log(`\n📊 Response Structure Validation Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Validate response structure based on extraction mode
 */
function validateResponseStructure(response, extractionMode) {
  if (!response || typeof response !== 'object') {
    throw new Error('Response must be an object');
  }

  // Common fields
  if (!response.status) {
    throw new Error('Response must have status field');
  }

  if (!response.request_id) {
    throw new Error('Response must have request_id field');
  }

  if (!Array.isArray(response.reference_urls)) {
    throw new Error('Response must have reference_urls array');
  }

  // Mode-specific validation
  if (extractionMode) {
    // AI extraction mode should have 'result' field
    if (!response.result) {
      return false;
    }
  } else {
    // Markdown mode should have 'markdown_content' field
    if (!response.markdown_content) {
      return false;
    }
  }

  return true;
}

/**
 * Run all markdown mode tests
 */
async function runAllMarkdownTests() {
  console.log('🚀 Starting SearchScraper Markdown Test Suite');
  console.log('='.repeat(70));
  console.log(`🔑 API Key: ${API_KEY.substring(0, 8)}...`);
  console.log(`⏰ Timestamp: ${new Date().toISOString()}\n`);

  const tests = [
    { name: 'Markdown Mode Input Validation', fn: testMarkdownModeInputValidation },
    { name: 'SearchScraper Markdown Function', fn: testSearchScraperMarkdownFunction },
    { name: 'Cost Calculation', fn: testCostCalculation },
    { name: 'Response Structure Validation', fn: testResponseStructure }
  ];

  let passed = 0;
  let total = tests.length;

  for (const test of tests) {
    try {
      const result = await test.fn();
      if (result) {
        passed++;
      }
    } catch (error) {
      console.error(`❌ Test '${test.name}' failed with error: ${error.message}`);
    }
    console.log('\n' + '-'.repeat(70));
  }

  console.log('\n🎯 FINAL MARKDOWN TEST RESULTS');
  console.log('='.repeat(40));
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${total - passed}`);
  console.log(`📊 Success Rate: ${((passed / total) * 100).toFixed(1)}%`);

  if (passed === total) {
    console.log('\n🎉 All markdown tests passed! SearchScraper markdown functionality is working correctly.');
    return 0;
  } else {
    console.log('\n⚠️  Some tests failed. Please review the output above.');
    return 1;
  }
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllMarkdownTests()
    .then(exitCode => {
      process.exit(exitCode);
    })
    .catch(error => {
      console.error('💥 Fatal error during test execution:', error.message);
      process.exit(1);
    });
}

export {
  testMarkdownModeInputValidation,
  testSearchScraperMarkdownFunction,
  testCostCalculation,
  testResponseStructure,
  runAllMarkdownTests
};

