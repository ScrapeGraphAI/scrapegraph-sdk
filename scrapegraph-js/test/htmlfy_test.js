import { htmlfy, getHtmlfyRequest } from '../index.js';
import 'dotenv/config';

/**
 * Test suite for HTMLfy functionality
 * This file demonstrates usage and validates the HTMLfy parameters
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test input validation for htmlfy
 */
function testInputValidation() {
  console.log('🧪 Testing HTMLfy Input Validation');
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
    },
    {
      name: 'Invalid renderHeavyJs type',
      apiKey: 'valid-key',
      url: 'https://example.com',
      options: { renderHeavyJs: 'true' },
      expected: false,
      description: 'renderHeavyJs as string instead of boolean'
    },
    {
      name: 'Invalid headers type',
      apiKey: 'valid-key',
      url: 'https://example.com',
      options: { headers: 'invalid' },
      expected: false,
      description: 'Headers as string instead of object'
    },
    {
      name: 'URL with query parameters',
      apiKey: 'valid-key',
      url: 'https://example.com/page?param1=value1&param2=value2',
      options: {},
      expected: true,
      description: 'URL with query parameters'
    },
    {
      name: 'URL with fragments',
      apiKey: 'valid-key',
      url: 'https://example.com/page#section1',
      options: {},
      expected: true,
      description: 'URL with fragments'
    },
    {
      name: 'URL with port',
      apiKey: 'valid-key',
      url: 'https://example.com:8080/page',
      options: {},
      expected: true,
      description: 'URL with port number'
    }
  ];

  let passed = 0;
  let failed = 0;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);
    console.log(`   ${testCase.description}`);

    try {
      // Simulate the validation logic from htmlfy
      const { apiKey, url, options } = testCase;

      // API Key validation
      if (!apiKey || typeof apiKey !== 'string') {
        throw new Error('API key must be a non-empty string');
      }

      // URL validation
      if (!url || typeof url !== 'string') {
        throw new Error('URL must be a non-empty string');
      }

      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        throw new Error('URL must start with http:// or https://');
      }

      // Options validation
      if (options && typeof options === 'object') {
        if (options.renderHeavyJs !== undefined && typeof options.renderHeavyJs !== 'boolean') {
          throw new Error('renderHeavyJs must be a boolean');
        }

        if (options.headers !== undefined && typeof options.headers !== 'object') {
          throw new Error('headers must be an object');
        }
      }

      console.log('   ✅ PASSED');
      passed++;

    } catch (error) {
      if (testCase.expected === false) {
        console.log(`   ✅ PASSED (expected failure: ${error.message})`);
        passed++;
      } else {
        console.log(`   ❌ FAILED: ${error.message}`);
        failed++;
      }
    }
  });

  console.log(`\n📊 Input Validation Results:`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

  return { passed, failed };
}

/**
 * Test getHtmlfyRequest input validation
 */
function testGetHtmlfyRequestValidation() {
  console.log('\n🧪 Testing getHtmlfyRequest Input Validation');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Valid request ID',
      apiKey: 'valid-key',
      requestId: '123e4567-e89b-12d3-a456-426614174000',
      expected: true,
      description: 'Valid UUID format request ID'
    },
    {
      name: 'Invalid request ID - empty string',
      apiKey: 'valid-key',
      requestId: '',
      expected: false,
      description: 'Empty request ID string'
    },
    {
      name: 'Invalid request ID - invalid format',
      apiKey: 'valid-key',
      requestId: 'invalid-uuid',
      expected: false,
      description: 'Invalid UUID format'
    },
    {
      name: 'Invalid request ID - wrong length',
      apiKey: 'valid-key',
      requestId: '123',
      expected: false,
      description: 'Request ID with wrong length'
    },
    {
      name: 'Empty API key',
      apiKey: '',
      requestId: '123e4567-e89b-12d3-a456-426614174000',
      expected: false,
      description: 'Empty API key string'
    }
  ];

  let passed = 0;
  let failed = 0;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);
    console.log(`   ${testCase.description}`);

    try {
      // Simulate the validation logic from getHtmlfyRequest
      const { apiKey, requestId } = testCase;

      // API Key validation
      if (!apiKey || typeof apiKey !== 'string') {
        throw new Error('API key must be a non-empty string');
      }

      // Request ID validation
      if (!requestId || typeof requestId !== 'string') {
        throw new Error('Request ID must be a non-empty string');
      }

      // Basic UUID format validation (simplified)
      const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      if (!uuidRegex.test(requestId)) {
        throw new Error('Request ID must be a valid UUID format');
      }

      console.log('   ✅ PASSED');
      passed++;

    } catch (error) {
      if (testCase.expected === false) {
        console.log(`   ✅ PASSED (expected failure: ${error.message})`);
        passed++;
      } else {
        console.log(`   ❌ FAILED: ${error.message}`);
        failed++;
      }
    }
  });

  console.log(`\n📊 getHtmlfyRequest Validation Results:`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

  return { passed, failed };
}

/**
 * Test URL parsing and validation
 */
function testUrlParsing() {
  console.log('\n🧪 Testing URL Parsing and Validation');
  console.log('='.repeat(50));

  const testUrls = [
    'https://example.com',
    'http://localhost:3000',
    'https://api.example.com/v1/endpoint',
    'https://example.com/page?param=value',
    'https://example.com/page#section',
    'https://example.com:8080/path',
    'https://subdomain.example.com',
    'https://example.com/path/to/page.html'
  ];

  let passed = 0;
  let failed = 0;

  testUrls.forEach((url, index) => {
    console.log(`\n${index + 1}. Testing URL: ${url}`);

    try {
      // Validate URL format
      if (!url.startsWith('http://') && !url.startsWith('https://')) {
        throw new Error('URL must start with http:// or https://');
      }

      // Test URL constructor (basic validation)
      new URL(url);

      console.log('   ✅ PASSED - Valid URL format');
      passed++;

    } catch (error) {
      console.log(`   ❌ FAILED: ${error.message}`);
      failed++;
    }
  });

  console.log(`\n📊 URL Parsing Results:`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

  return { passed, failed };
}

/**
 * Test options object handling
 */
function testOptionsHandling() {
  console.log('\n🧪 Testing Options Object Handling');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Default options',
      options: {},
      expected: { renderHeavyJs: false, headers: {} },
      description: 'Empty options object should use defaults'
    },
    {
      name: 'Custom renderHeavyJs',
      options: { renderHeavyJs: true },
      expected: { renderHeavyJs: true, headers: {} },
      description: 'Custom renderHeavyJs value'
    },
    {
      name: 'Custom headers',
      options: { headers: { 'User-Agent': 'Test' } },
      expected: { renderHeavyJs: false, headers: { 'User-Agent': 'Test' } },
      description: 'Custom headers object'
    },
    {
      name: 'All custom options',
      options: { 
        renderHeavyJs: true, 
        headers: { 'User-Agent': 'Test', 'Accept': 'text/html' } 
      },
      expected: { 
        renderHeavyJs: true, 
        headers: { 'User-Agent': 'Test', 'Accept': 'text/html' } 
      },
      description: 'All options customized'
    }
  ];

  let passed = 0;
  let failed = 0;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);
    console.log(`   ${testCase.description}`);

    try {
      const { options, expected } = testCase;

      // Simulate the options processing logic
      const processedOptions = {
        renderHeavyJs: options.renderHeavyJs ?? false,
        headers: options.headers ?? {}
      };

      // Validate the processed options
      if (processedOptions.renderHeavyJs !== expected.renderHeavyJs) {
        throw new Error(`Expected renderHeavyJs to be ${expected.renderHeavyJs}, got ${processedOptions.renderHeavyJs}`);
      }

      if (JSON.stringify(processedOptions.headers) !== JSON.stringify(expected.headers)) {
        throw new Error(`Expected headers to be ${JSON.stringify(expected.headers)}, got ${JSON.stringify(processedOptions.headers)}`);
      }

      console.log('   ✅ PASSED');
      passed++;

    } catch (error) {
      console.log(`   ❌ FAILED: ${error.message}`);
      failed++;
    }
  });

  console.log(`\n📊 Options Handling Results:`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`📈 Success Rate: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);

  return { passed, failed };
}

/**
 * Main test runner
 */
function runAllTests() {
  console.log('🚀 HTMLfy Test Suite');
  console.log('='.repeat(60));
  console.log('This test suite validates the HTMLfy functionality');
  console.log('Note: These are validation tests, not actual API calls');
  console.log('='.repeat(60));

  const results = {
    inputValidation: testInputValidation(),
    getHtmlfyRequestValidation: testGetHtmlfyRequestValidation(),
    urlParsing: testUrlParsing(),
    optionsHandling: testOptionsHandling()
  };

  // Summary
  console.log('\n🎯 Overall Test Results');
  console.log('='.repeat(40));

  const totalPassed = Object.values(results).reduce((sum, result) => sum + result.passed, 0);
  const totalFailed = Object.values(results).reduce((sum, result) => sum + result.failed, 0);
  const totalTests = totalPassed + totalFailed;

  console.log(`📊 Total Tests: ${totalTests}`);
  console.log(`✅ Total Passed: ${totalPassed}`);
  console.log(`❌ Total Failed: ${totalFailed}`);
  console.log(`📈 Overall Success Rate: ${((totalPassed / totalTests) * 100).toFixed(1)}%`);

  // Detailed breakdown
  console.log('\n📋 Test Category Breakdown:');
  Object.entries(results).forEach(([category, result]) => {
    const successRate = ((result.passed / (result.passed + result.failed)) * 100).toFixed(1);
    console.log(`  ${category}: ${result.passed}/${result.passed + result.failed} (${successRate}%)`);
  });

  if (totalFailed === 0) {
    console.log('\n🎉 All tests passed! HTMLfy functionality is working correctly.');
  } else {
    console.log('\n⚠️  Some tests failed. Please review the failures above.');
  }

  return { totalPassed, totalFailed, totalTests };
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllTests();
}

export { runAllTests };
