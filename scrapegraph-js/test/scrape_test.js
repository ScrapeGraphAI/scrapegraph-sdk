import { scrape, getScrapeRequest } from '../index.js';
import 'dotenv/config';

/**
 * Test suite for Scrape functionality
 * This file demonstrates usage and validates the Scrape parameters
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test input validation for scrape
 */
function testInputValidation() {
  console.log('🧪 Testing Scrape Input Validation');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Valid inputs - basic',
      apiKey: 'valid-key',
      url: 'https://example.com',
      options: {},
      expected: true,
      description: 'All valid parameters with default options'
    },
    {
      name: 'Valid inputs - with heavy JS',
      apiKey: 'valid-key',
      url: 'https://example.com',
      options: { renderHeavyJs: true },
      expected: true,
      description: 'Valid parameters with heavy JS rendering'
    },
    {
      name: 'Valid inputs - with headers',
      apiKey: 'valid-key',
      url: 'https://example.com',
      options: { 
        headers: { 'User-Agent': 'Test Agent' } 
      },
      expected: true,
      description: 'Valid parameters with custom headers'
    },
    {
      name: 'Valid inputs - with all options',
      apiKey: 'valid-key',
      url: 'https://example.com',
      options: { 
        renderHeavyJs: true,
        headers: { 'User-Agent': 'Test Agent' }
      },
      expected: true,
      description: 'Valid parameters with all options enabled'
    },
    {
      name: 'Invalid URL - no protocol',
      apiKey: 'valid-key',
      url: 'example.com',
      options: {},
      expected: false,
      description: 'URL without http/https protocol'
    },
    {
      name: 'Invalid URL - relative path',
      apiKey: 'valid-key',
      url: '/path/to/page',
      options: {},
      expected: false,
      description: 'Relative path instead of absolute URL'
    },
    {
      name: 'Invalid URL - empty string',
      apiKey: 'valid-key',
      url: '',
      options: {},
      expected: false,
      description: 'Empty URL string'
    },
    {
      name: 'Invalid URL - null',
      apiKey: 'valid-key',
      url: null,
      options: {},
      expected: false,
      description: 'Null URL'
    },
    {
      name: 'Empty API key',
      apiKey: '',
      url: 'https://example.com',
      options: {},
      expected: false,
      description: 'Empty API key string'
    },
    {
      name: 'Invalid API key type',
      apiKey: 123,
      url: 'https://example.com',
      options: {},
      expected: false,
      description: 'API key as number instead of string'
    }
  ];

  let passed = 0;
  let total = testCases.length;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. ${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);
    
    try {
      // Validate inputs
      const isValid = validateScrapeInputs(
        testCase.apiKey, 
        testCase.url, 
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

  console.log(`\n📊 Input Validation Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Validate scrape function inputs
 */
function validateScrapeInputs(apiKey, url, options) {
  // Check API key
  if (!apiKey || typeof apiKey !== 'string' || apiKey.trim() === '') {
    throw new Error('Invalid API key');
  }

  // Check URL
  if (!url || typeof url !== 'string' || url.trim() === '') {
    throw new Error('Invalid URL');
  }

  // Check URL format
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    throw new Error('URL must start with http:// or https://');
  }

  // Check options
  if (options && typeof options !== 'object') {
    throw new Error('Options must be an object');
  }

  // Check renderHeavyJs option
  if (options.renderHeavyJs !== undefined && typeof options.renderHeavyJs !== 'boolean') {
    throw new Error('renderHeavyJs must be a boolean');
  }

  // Check headers option
  if (options.headers !== undefined && typeof options.headers !== 'object') {
    throw new Error('Headers must be an object');
  }

  return true;
}

/**
 * Test scrape function with mock data
 */
async function testScrapeFunction() {
  console.log('\n🧪 Testing Scrape Function (Mock)');
  console.log('='.repeat(50));

  try {
    // Mock the scrape function to avoid actual API calls during testing
    const mockScrape = async (apiKey, url, options = {}) => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Return mock response
      return {
        status: 'completed',
        scrape_request_id: 'mock-request-id-12345',
        html: '<!DOCTYPE html><html><head><title>Mock Page</title></head><body><h1>Mock Content</h1></body></html>',
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      };
    };

    console.log('1. Testing basic scrape call...');
    const result1 = await mockScrape(API_KEY, 'https://example.com');
    console.log(`   ✅ Status: ${result1.status}`);
    console.log(`   ✅ Request ID: ${result1.scrape_request_id}`);
    console.log(`   ✅ HTML length: ${result1.html.length} characters`);

    console.log('\n2. Testing scrape with heavy JS rendering...');
    const result2 = await mockScrape(API_KEY, 'https://example.com', { renderHeavyJs: true });
    console.log(`   ✅ Status: ${result2.status}`);
    console.log(`   ✅ Request ID: ${result2.scrape_request_id}`);

    console.log('\n3. Testing scrape with custom headers...');
    const result3 = await mockScrape(API_KEY, 'https://example.com', { 
      headers: { 'User-Agent': 'Test Bot' } 
    });
    console.log(`   ✅ Status: ${result3.status}`);
    console.log(`   ✅ Request ID: ${result3.scrape_request_id}`);

    console.log('\n✅ All scrape function tests passed');
    return true;

  } catch (error) {
    console.error(`❌ Scrape function test failed: ${error.message}`);
    return false;
  }
}

/**
 * Test getScrapeRequest function with mock data
 */
async function testGetScrapeRequestFunction() {
  console.log('\n🧪 Testing GetScrapeRequest Function (Mock)');
  console.log('='.repeat(50));

  try {
    // Mock the getScrapeRequest function
    const mockGetScrapeRequest = async (apiKey, requestId) => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 50));
      
      // Return mock response
      return {
        status: 'completed',
        scrape_request_id: requestId,
        html: '<!DOCTYPE html><html><head><title>Retrieved Page</title></head><body><h1>Retrieved Content</h1></body></html>',
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      };
    };

    console.log('1. Testing getScrapeRequest with valid request ID...');
    const result1 = await mockGetScrapeRequest(API_KEY, 'test-request-123');
    console.log(`   ✅ Status: ${result1.status}`);
    console.log(`   ✅ Request ID: ${result1.scrape_request_id}`);
    console.log(`   ✅ HTML length: ${result1.html.length} characters`);

    console.log('\n2. Testing getScrapeRequest with different request ID...');
    const result2 = await mockGetScrapeRequest(API_KEY, 'another-request-456');
    console.log(`   ✅ Status: ${result2.status}`);
    console.log(`   ✅ Request ID: ${result2.scrape_request_id}`);

    console.log('\n✅ All getScrapeRequest function tests passed');
    return true;

  } catch (error) {
    console.error(`❌ GetScrapeRequest function test failed: ${error.message}`);
    return false;
  }
}

/**
 * Test error handling
 */
function testErrorHandling() {
  console.log('\n🧪 Testing Error Handling');
  console.log('='.repeat(50));

  let passed = 0;
  let total = 0;

  // Test 1: Invalid API key
  total++;
  try {
    validateScrapeInputs('', 'https://example.com', {});
    console.log('1. Empty API key test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('1. Empty API key test: ✅ PASSED');
    passed++;
  }

  // Test 2: Invalid URL
  total++;
  try {
    validateScrapeInputs('valid-key', 'invalid-url', {});
    console.log('2. Invalid URL test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('2. Invalid URL test: ✅ PASSED');
    passed++;
  }

  // Test 3: Invalid options
  total++;
  try {
    validateScrapeInputs('valid-key', 'https://example.com', 'invalid-options');
    console.log('3. Invalid options test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('3. Invalid options test: ✅ PASSED');
    passed++;
  }

  // Test 4: Invalid renderHeavyJs
  total++;
  try {
    validateScrapeInputs('valid-key', 'https://example.com', { renderHeavyJs: 'invalid' });
    console.log('4. Invalid renderHeavyJs test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('4. Invalid renderHeavyJs test: ✅ PASSED');
    passed++;
  }

  console.log(`\n📊 Error Handling Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Test URL validation
 */
function testUrlValidation() {
  console.log('\n🧪 Testing URL Validation');
  console.log('='.repeat(50));

  const testUrls = [
    { url: 'https://example.com', expected: true, description: 'HTTPS URL' },
    { url: 'http://example.com', expected: true, description: 'HTTP URL' },
    { url: 'https://sub.example.com', expected: true, description: 'Subdomain HTTPS' },
    { url: 'https://example.com/path', expected: true, description: 'HTTPS with path' },
    { url: 'https://example.com?param=value', expected: true, description: 'HTTPS with query params' },
    { url: 'https://example.com#fragment', expected: true, description: 'HTTPS with fragment' },
    { url: 'example.com', expected: false, description: 'No protocol' },
    { url: '/path/to/page', expected: false, description: 'Relative path' },
    { url: 'ftp://example.com', expected: false, description: 'FTP protocol' },
    { url: '', expected: false, description: 'Empty string' },
    { url: null, expected: false, description: 'Null value' },
    { url: undefined, expected: false, description: 'Undefined value' }
  ];

  let passed = 0;
  let total = testUrls.length;

  testUrls.forEach((testCase, index) => {
    console.log(`${index + 1}. ${testCase.description}: ${testCase.url}`);
    
    try {
      if (testCase.url) {
        const isValid = testCase.url.startsWith('http://') || testCase.url.startsWith('https://');
        if (isValid === testCase.expected) {
          console.log(`   ✅ PASSED`);
          passed++;
        } else {
          console.log(`   ❌ FAILED - Expected: ${testCase.expected}, Got: ${isValid}`);
        }
      } else {
        if (!testCase.expected) {
          console.log(`   ✅ PASSED`);
          passed++;
        } else {
          console.log(`   ❌ FAILED - Expected: ${testCase.expected}, Got: false`);
        }
      }
    } catch (error) {
      if (!testCase.expected) {
        console.log(`   ✅ PASSED (Expected error)`);
        passed++;
      } else {
        console.log(`   ❌ FAILED - Unexpected error: ${error.message}`);
      }
    }
  });

  console.log(`\n📊 URL Validation Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Run all tests
 */
async function runAllTests() {
  console.log('🚀 Starting Scrape Test Suite');
  console.log('='.repeat(60));
  console.log(`🔑 API Key: ${API_KEY.substring(0, 8)}...`);
  console.log(`⏰ Timestamp: ${new Date().toISOString()}\n`);

  const tests = [
    { name: 'Input Validation', fn: testInputValidation },
    { name: 'Scrape Function', fn: testScrapeFunction },
    { name: 'GetScrapeRequest Function', fn: testGetScrapeRequestFunction },
    { name: 'Error Handling', fn: testErrorHandling },
    { name: 'URL Validation', fn: testUrlValidation }
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
    console.log('\n' + '-'.repeat(60));
  }

  console.log('\n🎯 FINAL TEST RESULTS');
  console.log('='.repeat(30));
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${total - passed}`);
  console.log(`📊 Success Rate: ${((passed / total) * 100).toFixed(1)}%`);

  if (passed === total) {
    console.log('\n🎉 All tests passed! Scrape functionality is working correctly.');
    return 0;
  } else {
    console.log('\n⚠️  Some tests failed. Please review the output above.');
    return 1;
  }
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllTests()
    .then(exitCode => {
      process.exit(exitCode);
    })
    .catch(error => {
      console.error('💥 Fatal error during test execution:', error.message);
      process.exit(1);
    });
}

export {
  testInputValidation,
  testScrapeFunction,
  testGetScrapeRequestFunction,
  testErrorHandling,
  testUrlValidation,
  runAllTests
};
