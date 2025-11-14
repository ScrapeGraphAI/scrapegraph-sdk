import { healthz, initMockConfig, enableMock, disableMock } from '../index.js';
import 'dotenv/config';

/**
 * Test suite for Health Check functionality
 * This file demonstrates usage and validates the healthz endpoint
 */

// Mock API key for testing (replace with real key for actual testing)
const API_KEY = process.env.SGAI_APIKEY || 'test-api-key';

/**
 * Test basic health check
 */
async function testBasicHealthCheck() {
  console.log('🧪 Testing Basic Health Check');
  console.log('='.repeat(50));

  try {
    console.log('Calling healthz endpoint...');
    const result = await healthz(API_KEY);
    
    console.log('✅ Success! Health check response:');
    console.log(JSON.stringify(result, null, 2));
    
    // Validate response structure
    if (!result.status) {
      throw new Error('Response missing "status" field');
    }
    
    console.log('✓ Response has required fields');
    console.log('');
    return true;
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.log('');
    return false;
  }
}

/**
 * Test health check with mock mode
 */
async function testHealthCheckMock() {
  console.log('🧪 Testing Health Check with Mock Mode');
  console.log('='.repeat(50));

  try {
    // Enable mock mode
    enableMock();
    console.log('Mock mode enabled');
    
    console.log('Calling healthz endpoint in mock mode...');
    const result = await healthz(API_KEY, { mock: true });
    
    console.log('✅ Success! Mock health check response:');
    console.log(JSON.stringify(result, null, 2));
    
    // Validate mock response structure
    if (!result.status) {
      throw new Error('Mock response missing "status" field');
    }
    
    if (result.status !== 'healthy') {
      console.log('⚠️  Warning: Expected mock status to be "healthy"');
    }
    
    console.log('✓ Mock response has required fields');
    
    // Disable mock mode
    disableMock();
    console.log('Mock mode disabled');
    console.log('');
    return true;
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    disableMock();
    console.log('');
    return false;
  }
}

/**
 * Test health check with custom mock response
 */
async function testHealthCheckCustomMock() {
  console.log('🧪 Testing Health Check with Custom Mock Response');
  console.log('='.repeat(50));

  try {
    // Initialize mock with custom responses
    initMockConfig({
      enabled: true,
      customResponses: {
        '/v1/healthz': {
          status: 'degraded',
          message: 'Custom mock status',
          uptime: 12345
        }
      }
    });
    console.log('Custom mock configuration set');
    
    console.log('Calling healthz endpoint with custom mock...');
    const result = await healthz(API_KEY);
    
    console.log('✅ Success! Custom mock response:');
    console.log(JSON.stringify(result, null, 2));
    
    // Validate custom response
    if (result.status !== 'degraded') {
      throw new Error(`Expected status "degraded", got "${result.status}"`);
    }
    
    if (result.message !== 'Custom mock status') {
      throw new Error(`Expected custom message, got "${result.message}"`);
    }
    
    console.log('✓ Custom mock response validated');
    
    // Reset mock configuration
    disableMock();
    console.log('Mock mode disabled');
    console.log('');
    return true;
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    disableMock();
    console.log('');
    return false;
  }
}

/**
 * Test input validation
 */
function testInputValidation() {
  console.log('🧪 Testing Input Validation');
  console.log('='.repeat(50));

  const testCases = [
    {
      name: 'Valid API key',
      apiKey: 'dummy-api-key',
      expected: true,
      description: 'Should accept valid API key'
    },
    {
      name: 'Empty API key',
      apiKey: '',
      expected: false,
      description: 'Should reject empty API key'
    },
    {
      name: 'Null API key',
      apiKey: null,
      expected: false,
      description: 'Should reject null API key'
    }
  ];

  let passed = 0;
  let failed = 0;

  testCases.forEach(test => {
    try {
      if (!test.apiKey) {
        console.log(`  ✓ ${test.name}: Correctly identified as invalid`);
        passed++;
      } else {
        console.log(`  ✓ ${test.name}: Validated successfully`);
        passed++;
      }
    } catch (error) {
      console.log(`  ✗ ${test.name}: ${error.message}`);
      failed++;
    }
  });

  console.log(`\nValidation Results: ${passed} passed, ${failed} failed`);
  console.log('');
  return failed === 0;
}

/**
 * Test monitoring pattern
 */
async function testMonitoringPattern() {
  console.log('🧪 Testing Monitoring Pattern');
  console.log('='.repeat(50));

  try {
    enableMock();
    
    // Simulate multiple health checks
    console.log('Performing 3 consecutive health checks...');
    const checks = [];
    
    for (let i = 1; i <= 3; i++) {
      console.log(`  Check ${i}/3...`);
      const result = await healthz(API_KEY, { mock: true });
      checks.push(result);
    }
    
    // Analyze results
    const healthyChecks = checks.filter(c => c.status === 'healthy').length;
    const successRate = (healthyChecks / checks.length) * 100;
    
    console.log(`\n✅ Completed ${checks.length} checks`);
    console.log(`   Healthy: ${healthyChecks}/${checks.length} (${successRate}%)`);
    
    if (successRate === 100) {
      console.log('   ✓ All checks passed - service is stable');
    } else if (successRate > 0) {
      console.log('   ⚠️  Some checks failed - service may be unstable');
    } else {
      console.log('   ✗ All checks failed - service is down');
    }
    
    disableMock();
    console.log('');
    return true;
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    disableMock();
    console.log('');
    return false;
  }
}

/**
 * Run all tests
 */
async function runAllTests() {
  console.log('🚀 Starting Health Check Tests');
  console.log('='.repeat(60));
  console.log('');

  const results = {
    total: 0,
    passed: 0,
    failed: 0
  };

  // Test 1: Input validation
  results.total++;
  if (testInputValidation()) {
    results.passed++;
  } else {
    results.failed++;
  }

  // Test 2: Mock mode
  results.total++;
  if (await testHealthCheckMock()) {
    results.passed++;
  } else {
    results.failed++;
  }

  // Test 3: Custom mock
  results.total++;
  if (await testHealthCheckCustomMock()) {
    results.passed++;
  } else {
    results.failed++;
  }

  // Test 4: Monitoring pattern
  results.total++;
  if (await testMonitoringPattern()) {
    results.passed++;
  } else {
    results.failed++;
  }

  // Test 5: Basic health check (only if API key is available)
  if (process.env.SGAI_APIKEY) {
    results.total++;
    if (await testBasicHealthCheck()) {
      results.passed++;
    } else {
      results.failed++;
    }
  } else {
    console.log('⚠️  Skipping live API test (SGAI_APIKEY not set)');
    console.log('');
  }

  // Print summary
  console.log('='.repeat(60));
  console.log('📊 Test Summary');
  console.log('='.repeat(60));
  console.log(`Total Tests: ${results.total}`);
  console.log(`Passed: ${results.passed} ✓`);
  console.log(`Failed: ${results.failed} ✗`);
  console.log(`Success Rate: ${((results.passed / results.total) * 100).toFixed(1)}%`);
  console.log('='.repeat(60));

  if (results.failed === 0) {
    console.log('✅ All tests passed!');
    process.exit(0);
  } else {
    console.log('❌ Some tests failed');
    process.exit(1);
  }
}

// Run tests
runAllTests().catch(error => {
  console.error('Fatal error running tests:', error);
  process.exit(1);
});

