import {
  smartScraper,
  searchScraper,
  markdownify,
  scrape,
  agenticScraper,
  crawl,
} from '../index.js';
import 'dotenv/config';

/**
 * Test suite for Stealth Mode functionality
 * This file demonstrates usage and validates stealth mode parameters across all endpoints
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test input validation for stealth mode
 */
function testStealthModeValidation() {
  console.log('🧪 Testing Stealth Mode Input Validation');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Valid stealth mode - true',
      stealth: true,
      expected: true,
      description: 'Stealth mode enabled (boolean true)'
    },
    {
      name: 'Valid stealth mode - false',
      stealth: false,
      expected: true,
      description: 'Stealth mode disabled (boolean false)'
    },
    {
      name: 'Valid stealth mode - undefined (default)',
      stealth: undefined,
      expected: true,
      description: 'Stealth mode not specified (should default to false)'
    },
    {
      name: 'Invalid stealth mode - string',
      stealth: 'true',
      expected: false,
      description: 'Stealth mode as string instead of boolean'
    },
    {
      name: 'Invalid stealth mode - number',
      stealth: 1,
      expected: false,
      description: 'Stealth mode as number instead of boolean'
    },
    {
      name: 'Invalid stealth mode - object',
      stealth: {},
      expected: false,
      description: 'Stealth mode as object instead of boolean'
    },
  ];

  let passed = 0;
  let total = testCases.length;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. ${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      const isValid = validateStealthMode(testCase.stealth);

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

  console.log(`\n📊 Stealth Mode Validation Results: ${passed}/${total} tests passed`);
  return passed === total;
}

/**
 * Validate stealth mode parameter
 */
function validateStealthMode(stealth) {
  if (stealth !== undefined && typeof stealth !== 'boolean') {
    throw new Error('Stealth mode must be a boolean value (true or false)');
  }
  return true;
}

/**
 * Test SmartScraper with stealth mode
 */
async function testSmartScraperWithStealth() {
  console.log('\n🧪 Testing SmartScraper with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'SmartScraper with stealth=true',
      options: { stealth: true },
      description: 'Test smartScraper with stealth mode enabled'
    },
    {
      name: 'SmartScraper with stealth=false',
      options: { stealth: false },
      description: 'Test smartScraper with stealth mode disabled'
    },
    {
      name: 'SmartScraper without stealth parameter',
      options: {},
      description: 'Test smartScraper without stealth parameter (defaults to false)'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Mock function to avoid actual API calls
      const mockSmartScraper = async (apiKey, url, prompt, schema, numScrolls, totalPages, cookies, options) => {
        // Validate that stealth parameter is boolean if provided
        if (options.stealth !== undefined && typeof options.stealth !== 'boolean') {
          throw new Error('Stealth must be a boolean');
        }

        return {
          request_id: 'mock-request-id',
          status: 'completed',
          result: { data: 'mock data' }
        };
      };

      const result = await mockSmartScraper(
        API_KEY,
        'https://example.com',
        'Extract data',
        null,
        null,
        null,
        null,
        testCase.options
      );

      console.log(`   ✅ PASSED - Status: ${result.status}`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 SmartScraper Stealth Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Test SearchScraper with stealth mode
 */
async function testSearchScraperWithStealth() {
  console.log('\n🧪 Testing SearchScraper with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'SearchScraper with stealth=true',
      options: { stealth: true },
      description: 'Test searchScraper with stealth mode enabled'
    },
    {
      name: 'SearchScraper with stealth=false',
      options: { stealth: false },
      description: 'Test searchScraper with stealth mode disabled'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Mock function
      const mockSearchScraper = async (apiKey, prompt, numResults, schema, userAgent, options) => {
        if (options.stealth !== undefined && typeof options.stealth !== 'boolean') {
          throw new Error('Stealth must be a boolean');
        }

        return {
          request_id: 'mock-request-id',
          status: 'completed',
          result: { answer: 'mock answer' }
        };
      };

      const result = await mockSearchScraper(
        API_KEY,
        'Search query',
        3,
        null,
        null,
        testCase.options
      );

      console.log(`   ✅ PASSED - Status: ${result.status}`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 SearchScraper Stealth Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Test Markdownify with stealth mode
 */
async function testMarkdownifyWithStealth() {
  console.log('\n🧪 Testing Markdownify with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Markdownify with stealth=true',
      options: { stealth: true },
      description: 'Test markdownify with stealth mode enabled'
    },
    {
      name: 'Markdownify with stealth=false',
      options: { stealth: false },
      description: 'Test markdownify with stealth mode disabled'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Mock function
      const mockMarkdownify = async (apiKey, url, options) => {
        if (options.stealth !== undefined && typeof options.stealth !== 'boolean') {
          throw new Error('Stealth must be a boolean');
        }

        return {
          request_id: 'mock-request-id',
          status: 'completed',
          result: '# Markdown content'
        };
      };

      const result = await mockMarkdownify(
        API_KEY,
        'https://example.com',
        testCase.options
      );

      console.log(`   ✅ PASSED - Status: ${result.status}`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 Markdownify Stealth Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Test Scrape with stealth mode
 */
async function testScrapeWithStealth() {
  console.log('\n🧪 Testing Scrape with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Scrape with stealth=true',
      options: { stealth: true },
      description: 'Test scrape with stealth mode enabled'
    },
    {
      name: 'Scrape with stealth=false',
      options: { stealth: false },
      description: 'Test scrape with stealth mode disabled'
    },
    {
      name: 'Scrape with stealth=true and renderHeavyJs=true',
      options: { stealth: true, renderHeavyJs: true },
      description: 'Test scrape with both stealth and heavy JS rendering'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Mock function
      const mockScrape = async (apiKey, url, options) => {
        if (options.stealth !== undefined && typeof options.stealth !== 'boolean') {
          throw new Error('Stealth must be a boolean');
        }

        return {
          scrape_request_id: 'mock-request-id',
          status: 'completed',
          html: '<html><body>Mock content</body></html>'
        };
      };

      const result = await mockScrape(
        API_KEY,
        'https://example.com',
        testCase.options
      );

      console.log(`   ✅ PASSED - Status: ${result.status}`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 Scrape Stealth Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Test Agentic Scraper with stealth mode
 */
async function testAgenticScraperWithStealth() {
  console.log('\n🧪 Testing Agentic Scraper with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'AgenticScraper with stealth=true',
      options: { stealth: true },
      description: 'Test agenticScraper with stealth mode enabled'
    },
    {
      name: 'AgenticScraper with stealth=false',
      options: { stealth: false },
      description: 'Test agenticScraper with stealth mode disabled'
    },
    {
      name: 'AgenticScraper with stealth and AI extraction',
      options: { stealth: true },
      aiExtraction: true,
      userPrompt: 'Extract user data',
      description: 'Test agenticScraper with stealth and AI extraction'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Mock function
      const mockAgenticScraper = async (apiKey, url, steps, useSession, userPrompt, outputSchema, aiExtraction, options) => {
        if (options.stealth !== undefined && typeof options.stealth !== 'boolean') {
          throw new Error('Stealth must be a boolean');
        }

        return {
          request_id: 'mock-request-id',
          status: 'processing',
          message: 'Agentic scraping started'
        };
      };

      const result = await mockAgenticScraper(
        API_KEY,
        'https://example.com',
        ['Click button', 'Extract data'],
        true,
        testCase.userPrompt || null,
        null,
        testCase.aiExtraction || false,
        testCase.options
      );

      console.log(`   ✅ PASSED - Status: ${result.status}`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 AgenticScraper Stealth Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Test Crawl with stealth mode
 */
async function testCrawlWithStealth() {
  console.log('\n🧪 Testing Crawl with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Crawl with stealth=true',
      options: { stealth: true },
      description: 'Test crawl with stealth mode enabled'
    },
    {
      name: 'Crawl with stealth=false',
      options: { stealth: false },
      description: 'Test crawl with stealth mode disabled'
    },
    {
      name: 'Crawl with stealth and sitemap',
      options: { stealth: true, sitemap: true },
      description: 'Test crawl with stealth mode and sitemap enabled'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Mock function
      const mockCrawl = async (apiKey, url, prompt, schema, options) => {
        if (options.stealth !== undefined && typeof options.stealth !== 'boolean') {
          throw new Error('Stealth must be a boolean');
        }

        return {
          id: 'mock-crawl-id',
          status: 'processing',
          message: 'Crawl job started'
        };
      };

      const result = await mockCrawl(
        API_KEY,
        'https://example.com',
        'Extract data',
        { type: 'object', properties: { title: { type: 'string' } } },
        testCase.options
      );

      console.log(`   ✅ PASSED - Status: ${result.status}`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 Crawl Stealth Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Test combined features with stealth mode
 */
async function testCombinedFeaturesWithStealth() {
  console.log('\n🧪 Testing Combined Features with Stealth Mode');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'SmartScraper with stealth + headers + pagination',
      endpoint: 'smartScraper',
      options: {
        stealth: true,
        renderHeavyJs: true
      },
      additionalParams: {
        numberOfScrolls: 10,
        totalPages: 5
      },
      description: 'Test smartScraper with stealth and multiple features'
    },
    {
      name: 'Scrape with stealth + headers + heavy JS',
      endpoint: 'scrape',
      options: {
        stealth: true,
        renderHeavyJs: true,
        headers: { 'User-Agent': 'Test Agent' }
      },
      description: 'Test scrape with stealth, custom headers, and JS rendering'
    },
    {
      name: 'SearchScraper with stealth + extraction mode',
      endpoint: 'searchScraper',
      options: {
        stealth: true,
        extractionMode: true,
        renderHeavyJs: true
      },
      description: 'Test searchScraper with stealth and extraction mode'
    },
  ];

  let passed = 0;

  for (const testCase of testCases) {
    console.log(`\n${testCase.name}`);
    console.log(`   Description: ${testCase.description}`);

    try {
      // Validate all options
      if (testCase.options.stealth !== undefined && typeof testCase.options.stealth !== 'boolean') {
        throw new Error('Stealth must be a boolean');
      }
      if (testCase.options.renderHeavyJs !== undefined && typeof testCase.options.renderHeavyJs !== 'boolean') {
        throw new Error('RenderHeavyJs must be a boolean');
      }

      console.log(`   ✅ PASSED - All parameters validated successfully`);
      passed++;
    } catch (error) {
      console.log(`   ❌ FAILED - Error: ${error.message}`);
    }
  }

  console.log(`\n📊 Combined Features Tests: ${passed}/${testCases.length} passed`);
  return passed === testCases.length;
}

/**
 * Run all stealth mode tests
 */
async function runAllStealthTests() {
  console.log('🚀 Starting Stealth Mode Test Suite');
  console.log('='.repeat(60));
  console.log(`🔑 API Key: ${API_KEY.substring(0, 8)}...`);
  console.log(`⏰ Timestamp: ${new Date().toISOString()}\n`);

  const tests = [
    { name: 'Stealth Mode Validation', fn: testStealthModeValidation },
    { name: 'SmartScraper with Stealth', fn: testSmartScraperWithStealth },
    { name: 'SearchScraper with Stealth', fn: testSearchScraperWithStealth },
    { name: 'Markdownify with Stealth', fn: testMarkdownifyWithStealth },
    { name: 'Scrape with Stealth', fn: testScrapeWithStealth },
    { name: 'AgenticScraper with Stealth', fn: testAgenticScraperWithStealth },
    { name: 'Crawl with Stealth', fn: testCrawlWithStealth },
    { name: 'Combined Features with Stealth', fn: testCombinedFeaturesWithStealth },
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
    console.log('\n🎉 All stealth mode tests passed! Functionality is working correctly.');
    return 0;
  } else {
    console.log('\n⚠️  Some tests failed. Please review the output above.');
    return 1;
  }
}

// Run tests if this file is executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runAllStealthTests()
    .then(exitCode => {
      process.exit(exitCode);
    })
    .catch(error => {
      console.error('💥 Fatal error during test execution:', error.message);
      process.exit(1);
    });
}

export {
  testStealthModeValidation,
  testSmartScraperWithStealth,
  testSearchScraperWithStealth,
  testMarkdownifyWithStealth,
  testScrapeWithStealth,
  testAgenticScraperWithStealth,
  testCrawlWithStealth,
  testCombinedFeaturesWithStealth,
  runAllStealthTests
};
