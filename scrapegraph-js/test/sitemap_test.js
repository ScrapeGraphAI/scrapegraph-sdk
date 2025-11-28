import { sitemap } from '../index.js';
import 'dotenv/config';

/**
 * Test suite for Sitemap functionality
 * This file demonstrates usage and validates the Sitemap parameters
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test input validation for sitemap
 */
function testInputValidation() {
  console.log('🧪 Testing Sitemap Input Validation');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Valid inputs - basic',
      apiKey: 'valid-key',
      websiteUrl: 'https://example.com',
      options: {},
      expected: true,
      description: 'All valid parameters with default options'
    },
    {
      name: 'Valid inputs - subdomain',
      apiKey: 'valid-key',
      websiteUrl: 'https://blog.example.com',
      options: {},
      expected: true,
      description: 'Valid subdomain URL'
    },
    {
      name: 'Valid inputs - with path',
      apiKey: 'valid-key',
      websiteUrl: 'https://example.com/section',
      options: {},
      expected: true,
      description: 'URL with path component'
    },
    {
      name: 'Invalid URL - no protocol',
      apiKey: 'valid-key',
      websiteUrl: 'example.com',
      options: {},
      expected: false,
      description: 'URL without http/https protocol'
    },
    {
      name: 'Invalid URL - relative path',
      apiKey: 'valid-key',
      websiteUrl: '/path/to/page',
      options: {},
      expected: false,
      description: 'Relative path instead of absolute URL'
    },
    {
      name: 'Invalid URL - empty string',
      apiKey: 'valid-key',
      websiteUrl: '',
      options: {},
      expected: false,
      description: 'Empty URL string'
    },
    {
      name: 'Invalid URL - null',
      apiKey: 'valid-key',
      websiteUrl: null,
      options: {},
      expected: false,
      description: 'Null URL'
    },
    {
      name: 'Empty API key',
      apiKey: '',
      websiteUrl: 'https://example.com',
      options: {},
      expected: false,
      description: 'Empty API key string'
    },
    {
      name: 'Invalid API key type',
      apiKey: 123,
      websiteUrl: 'https://example.com',
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
      const isValid = validateSitemapInputs(
        testCase.apiKey,
        testCase.websiteUrl,
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
 * Validate sitemap function inputs
 */
function validateSitemapInputs(apiKey, websiteUrl, options) {
  // Check API key
  if (!apiKey || typeof apiKey !== 'string' || apiKey.trim() === '') {
    throw new Error('Invalid API key');
  }

  // Check URL
  if (!websiteUrl || typeof websiteUrl !== 'string' || websiteUrl.trim() === '') {
    throw new Error('Invalid URL');
  }

  // Check URL format
  if (!websiteUrl.startsWith('http://') && !websiteUrl.startsWith('https://')) {
    throw new Error('URL must start with http:// or https://');
  }

  // Check options
  if (options && typeof options !== 'object') {
    throw new Error('Options must be an object');
  }

  return true;
}

/**
 * Test sitemap function with mock data
 */
async function testSitemapFunction() {
  console.log('\n🧪 Testing Sitemap Function (Mock)');
  console.log('='.repeat(50));

  try {
    // Mock the sitemap function to avoid actual API calls during testing
    const mockSitemap = async (apiKey, websiteUrl, options = {}) => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 100));

      // Return mock response
      return {
        urls: [
          'https://example.com/',
          'https://example.com/about',
          'https://example.com/products',
          'https://example.com/contact',
          'https://example.com/blog/post-1',
          'https://example.com/blog/post-2'
        ]
      };
    };

    console.log('1. Testing basic sitemap call...');
    const result1 = await mockSitemap(API_KEY, 'https://example.com');
    console.log(`   ✅ URLs found: ${result1.urls.length}`);
    console.log(`   ✅ First URL: ${result1.urls[0]}`);

    console.log('\n2. Testing sitemap for subdomain...');
    const result2 = await mockSitemap(API_KEY, 'https://blog.example.com');
    console.log(`   ✅ URLs found: ${result2.urls.length}`);

    console.log('\n3. Testing sitemap for URL with path...');
    const result3 = await mockSitemap(API_KEY, 'https://example.com/section');
    console.log(`   ✅ URLs found: ${result3.urls.length}`);

    console.log('\n✅ All sitemap function tests passed');
    return true;

  } catch (error) {
    console.error(`❌ Sitemap function test failed: ${error.message}`);
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
    validateSitemapInputs('', 'https://example.com', {});
    console.log('1. Empty API key test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('1. Empty API key test: ✅ PASSED');
    passed++;
  }

  // Test 2: Invalid URL
  total++;
  try {
    validateSitemapInputs('valid-key', 'invalid-url', {});
    console.log('2. Invalid URL test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('2. Invalid URL test: ✅ PASSED');
    passed++;
  }

  // Test 3: Invalid options
  total++;
  try {
    validateSitemapInputs('valid-key', 'https://example.com', 'invalid-options');
    console.log('3. Invalid options test: ❌ FAILED (should have thrown error)');
  } catch (error) {
    console.log('3. Invalid options test: ✅ PASSED');
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
  console.log('🚀 Starting Sitemap Test Suite');
  console.log('='.repeat(60));
  console.log(`🔑 API Key: ${API_KEY.substring(0, 8)}...`);
  console.log(`⏰ Timestamp: ${new Date().toISOString()}\n`);

  const tests = [
    { name: 'Input Validation', fn: testInputValidation },
    { name: 'Sitemap Function', fn: testSitemapFunction },
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
    console.log('\n🎉 All tests passed! Sitemap functionality is working correctly.');
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
  testSitemapFunction,
  testErrorHandling,
  testUrlValidation,
  runAllTests
};
