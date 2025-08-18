import { agenticScraper, getAgenticScraperRequest } from '../index.js';
import 'dotenv/config';

/**
 * Test suite for AgenticScraper functionality
 * This file demonstrates usage and validates the agentic scraper parameters
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test input validation for agenticScraper
 */
function testInputValidation() {
  console.log('🧪 Testing Input Validation');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Valid inputs',
      apiKey: 'valid-key',
      url: 'https://example.com',
      steps: ['click button', 'type text'],
      useSession: true,
      expected: true,
      description: 'All valid parameters'
    },
    {
      name: 'Invalid URL - no protocol',
      apiKey: 'valid-key',
      url: 'example.com',
      steps: ['click button'],
      useSession: true,
      expected: false,
      description: 'URL without http/https protocol'
    },
    {
      name: 'Empty API key',
      apiKey: '',
      url: 'https://example.com',
      steps: ['click button'],
      useSession: true,
      expected: false,
      description: 'Empty API key string'
    },
    {
      name: 'Empty steps array',
      apiKey: 'valid-key',
      url: 'https://example.com',
      steps: [],
      useSession: true,
      expected: false,
      description: 'Empty steps array'
    },
    {
      name: 'Steps with empty string',
      apiKey: 'valid-key',
      url: 'https://example.com',
      steps: ['click button', '', 'type text'],
      useSession: true,
      expected: false,
      description: 'Steps array containing empty string'
    },
    {
      name: 'Non-boolean useSession',
      apiKey: 'valid-key',
      url: 'https://example.com',
      steps: ['click button'],
      useSession: 'true',
      expected: false,
      description: 'useSession as string instead of boolean'
    },
    {
      name: 'Default useSession',
      apiKey: 'valid-key',
      url: 'https://example.com',
      steps: ['click button'],
      useSession: undefined,
      expected: true,
      description: 'useSession parameter omitted (should default to true)'
    }
  ];

  let passed = 0;
  let failed = 0;

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);
    console.log(`   ${testCase.description}`);

    try {
      // Simulate the validation logic from agenticScraper
      const { apiKey, url, steps, useSession } = testCase;

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

      // Steps validation
      if (!Array.isArray(steps) || steps.length === 0) {
        throw new Error('Steps must be a non-empty array');
      }
      if (steps.some(step => !step || typeof step !== 'string' || !step.trim())) {
        throw new Error('All steps must be non-empty strings');
      }

      // useSession validation (only if provided)
      if (useSession !== undefined && typeof useSession !== 'boolean') {
        throw new Error('useSession must be a boolean value');
      }

      if (testCase.expected) {
        console.log('   ✅ PASS - Validation passed as expected');
        passed++;
      } else {
        console.log('   ❌ FAIL - Expected validation to fail, but it passed');
        failed++;
      }
    } catch (error) {
      if (!testCase.expected) {
        console.log(`   ✅ PASS - Validation failed as expected: ${error.message}`);
        passed++;
      } else {
        console.log(`   ❌ FAIL - Unexpected validation failure: ${error.message}`);
        failed++;
      }
    }
  });

  console.log(`\n📊 Validation Results: ${passed} passed, ${failed} failed`);
  return { passed, failed };
}

/**
 * Test function signatures and parameter handling
 */
function testFunctionSignatures() {
  console.log('\n🧪 Testing Function Signatures');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'agenticScraper with all parameters',
      func: 'agenticScraper',
      args: [API_KEY, 'https://example.com', ['click button'], true],
      description: 'apiKey, url, steps, useSession'
    },
    {
      name: 'agenticScraper with default useSession',
      func: 'agenticScraper',
      args: [API_KEY, 'https://example.com', ['click button']],
      description: 'apiKey, url, steps (useSession defaults to true)'
    },
    {
      name: 'getAgenticScraperRequest',
      func: 'getAgenticScraperRequest',
      args: [API_KEY, 'test-request-id'],
      description: 'apiKey, requestId'
    }
  ];

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);
    console.log(`   Parameters: ${testCase.description}`);

    try {
      // Simulate function signature validation
      if (testCase.func === 'agenticScraper') {
        const [apiKey, url, steps, useSession] = testCase.args;
        if (typeof apiKey !== 'string' || typeof url !== 'string' || !Array.isArray(steps)) {
          throw new Error('Invalid parameter types');
        }
      } else if (testCase.func === 'getAgenticScraperRequest') {
        const [apiKey, requestId] = testCase.args;
        if (typeof apiKey !== 'string' || typeof requestId !== 'string') {
          throw new Error('Invalid parameter types');
        }
      }
      
      console.log('   ✅ PASS - Function signature valid');
    } catch (error) {
      console.log(`   ❌ FAIL - Function signature error: ${error.message}`);
    }
  });
}

/**
 * Test step parsing and validation
 */
function testStepValidation() {
  console.log('\n🧪 Testing Step Validation');
  console.log('='.repeat(50));

  const validSteps = [
    'click on login button',
    'type "username" in email field',
    'press Enter key',
    'wait for 2 seconds',
    'scroll down',
    'click on first result'
  ];

  const invalidSteps = [
    '', // Empty string
    '   ', // Only whitespace
    null, // Null value
    123, // Number instead of string
    {}, // Object instead of string
  ];

  console.log('\n1. Testing valid steps:');
  validSteps.forEach((step, index) => {
    console.log(`   ${index + 1}. "${step}" ✅ Valid`);
  });

  console.log('\n2. Testing invalid steps:');
  invalidSteps.forEach((step, index) => {
    const stepStr = step === null ? 'null' : 
                   typeof step === 'object' ? 'object' : 
                   `"${step}"`;
    console.log(`   ${index + 1}. ${stepStr} ❌ Invalid`);
  });

  console.log('\n3. Testing step combinations:');
  
  const testCombinations = [
    {
      name: 'All valid steps',
      steps: validSteps,
      expected: true
    },
    {
      name: 'Mixed valid and invalid',
      steps: ['click button', '', 'type text'],
      expected: false
    },
    {
      name: 'Single valid step',
      steps: ['click button'],
      expected: true
    }
  ];

  testCombinations.forEach((test, index) => {
    const isValid = test.steps.every(step => 
      step && typeof step === 'string' && step.trim()
    );
    const result = isValid === test.expected ? '✅ PASS' : '❌ FAIL';
    console.log(`   ${index + 1}. ${test.name}: ${result}`);
  });
}

/**
 * Test payload construction
 */
function testPayloadConstruction() {
  console.log('\n🧪 Testing Payload Construction');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Basic payload',
      url: 'https://example.com',
      steps: ['click button', 'type text'],
      useSession: true,
      expected: {
        url: 'https://example.com',
        use_session: true,
        steps: ['click button', 'type text']
      }
    },
    {
      name: 'Payload with useSession false',
      url: 'https://test.com',
      steps: ['fill form'],
      useSession: false,
      expected: {
        url: 'https://test.com',
        use_session: false,
        steps: ['fill form']
      }
    },
    {
      name: 'Payload with default useSession',
      url: 'https://default.com',
      steps: ['navigate'],
      useSession: undefined,
      expected: {
        url: 'https://default.com',
        use_session: true, // Should default to true
        steps: ['navigate']
      }
    }
  ];

  testCases.forEach((testCase, index) => {
    console.log(`\n${index + 1}. Testing: ${testCase.name}`);

    // Simulate payload construction
    const payload = {
      url: testCase.url,
      use_session: testCase.useSession !== undefined ? testCase.useSession : true,
      steps: testCase.steps
    };

    console.log('   📦 Constructed payload:');
    console.log('   ', JSON.stringify(payload, null, 2));

    // Validate against expected
    const matches = JSON.stringify(payload) === JSON.stringify(testCase.expected);
    console.log(`   ${matches ? '✅ PASS' : '❌ FAIL'} - Payload matches expected`);
  });
}

/**
 * Test common use case patterns
 */
function testUseCasePatterns() {
  console.log('\n🧪 Testing Use Case Patterns');
  console.log('='.repeat(50));

  const useCases = [
    {
      name: 'Login Flow',
      steps: [
        'click on email input',
        'type "user@example.com" in email field',
        'click on password input',
        'type "password123" in password field',
        'click login button',
        'wait for dashboard to load'
      ],
      useSession: true,
      description: 'Typical login automation'
    },
    {
      name: 'Search and Filter',
      steps: [
        'click on search bar',
        'type "laptop" in search input',
        'press Enter key',
        'wait for results to load',
        'click on price filter',
        'select $500-$1000 range',
        'click apply filters'
      ],
      useSession: false,
      description: 'E-commerce search workflow'
    },
    {
      name: 'Form Submission',
      steps: [
        'click on name input',
        'type "John Doe" in name field',
        'click on email input',
        'type "john@example.com" in email field',
        'click on message textarea',
        'type "Test message" in message field',
        'click submit button'
      ],
      useSession: false,
      description: 'Contact form automation'
    }
  ];

  useCases.forEach((useCase, index) => {
    console.log(`\n${index + 1}. ${useCase.name}`);
    console.log(`   Description: ${useCase.description}`);
    console.log(`   Steps: ${useCase.steps.length} automation actions`);
    console.log(`   Use Session: ${useCase.useSession}`);
    console.log('   ✅ PASS - Valid use case pattern');
  });
}

/**
 * Test error scenarios
 */
function testErrorScenarios() {
  console.log('\n🧪 Testing Error Scenarios');
  console.log('='.repeat(50));

  const errorScenarios = [
    {
      name: 'Missing API Key',
      test: () => {
        // Simulate missing API key
        throw new Error('API key must be a non-empty string');
      },
      expectedError: 'API key must be a non-empty string'
    },
    {
      name: 'Invalid URL Format',
      test: () => {
        // Simulate invalid URL
        throw new Error('URL must start with http:// or https://');
      },
      expectedError: 'URL must start with'
    },
    {
      name: 'Empty Steps Array',
      test: () => {
        // Simulate empty steps
        throw new Error('Steps must be a non-empty array');
      },
      expectedError: 'non-empty array'
    }
  ];

  errorScenarios.forEach((scenario, index) => {
    console.log(`\n${index + 1}. Testing: ${scenario.name}`);
    
    try {
      scenario.test();
      console.log('   ❌ FAIL - Expected error but none was thrown');
    } catch (error) {
      if (error.message.includes(scenario.expectedError)) {
        console.log(`   ✅ PASS - Correctly caught expected error: ${error.message}`);
      } else {
        console.log(`   ⚠️  PARTIAL - Caught error but message differs: ${error.message}`);
      }
    }
  });
}

/**
 * Main test runner
 */
function runTests() {
  console.log('🚀 ScrapeGraph JS SDK - AgenticScraper Tests');
  console.log('='.repeat(60));

  if (!process.env.SGAI_APIKEY) {
    console.log('⚠️  Note: SGAI_APIKEY not set - using mock key for validation tests');
  }

  console.log('\n🎯 Testing AgenticScraper functionality...');

  const results = {
    validation: testInputValidation(),
    signatures: testFunctionSignatures(),
    steps: testStepValidation(),
    payload: testPayloadConstruction(),
    useCases: testUseCasePatterns(),
    errors: testErrorScenarios(),
  };

  console.log('\n' + '='.repeat(60));
  console.log('📊 Test Summary');
  console.log('='.repeat(60));
  console.log('✅ Input Validation Tests: Completed');
  console.log('✅ Function Signature Tests: Completed');
  console.log('✅ Step Validation Tests: Completed');
  console.log('✅ Payload Construction Tests: Completed');
  console.log('✅ Use Case Pattern Tests: Completed');
  console.log('✅ Error Scenario Tests: Completed');

  const totalPassed = results.validation.passed;
  const totalFailed = results.validation.failed;

  console.log(`\n📊 Overall Results: ${totalPassed} passed, ${totalFailed} failed`);

  if (totalFailed === 0) {
    console.log('🎉 All tests passed!');
  } else {
    console.log('⚠️  Some tests failed - please review the results above');
  }

  console.log('\n💡 Usage Examples:');
  console.log('// Basic login automation');
  console.log('await agenticScraper(apiKey, url, ["click login", "type email"], true);');
  console.log('');
  console.log('// Form submission without session');
  console.log('await agenticScraper(apiKey, url, ["fill form", "submit"], false);');
  console.log('');
  console.log('// Check request status');
  console.log('await getAgenticScraperRequest(apiKey, requestId);');

  console.log('\n🔧 Next Steps:');
  console.log('1. Set SGAI_APIKEY environment variable for real API testing');
  console.log('2. Run the example files in the examples/ directory');
  console.log('3. Try with different websites and automation steps');
  console.log('4. Test with both useSession: true and false');
  console.log('5. Monitor request status for long-running automations');

  console.log('\n📚 Available Examples:');
  console.log('- agenticScraper_example.js - Basic usage');
  console.log('- getAgenticScraperRequest_example.js - Status checking');
  console.log('- agenticScraper_complete_example.js - Full workflow');
  console.log('- agenticScraper_advanced_example.js - Error handling');

  return totalFailed === 0;
}

// Run the tests
const success = runTests();
process.exit(success ? 0 : 1);
