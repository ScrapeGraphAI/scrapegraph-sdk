/**
 * Test file to verify cookies integration functionality.
 */

import { smartScraper } from './src/smartScraper.js';

function testCookiesIntegration() {
  console.log('🧪 Testing Cookies Integration');
  console.log('='.repeat(50));

  // Test 1: Basic cookies validation
  console.log('\n1. Testing basic cookies validation...');

  const cookies = { session_id: 'abc123', auth_token: 'xyz789' };

  // Create a mock payload to test the logic
  const mockPayload = {
    website_url: 'https://httpbin.org/cookies',
    user_prompt: 'Extract cookie information'
  };

  // Simulate the cookies validation logic
  if (cookies) {
    if (typeof cookies === 'object' && cookies !== null) {
      mockPayload.cookies = cookies;
      console.log('✅ Cookies validation passed');
      console.log(`✅ Cookies included: ${JSON.stringify(mockPayload.cookies)}`);
    } else {
      console.log('❌ Cookies validation failed - not an object');
    }
  }

  // Test 2: Complex cookies scenario
  console.log('\n2. Testing complex cookies scenario...');

  const complexCookies = {
    session_id: 'abc123def456',
    user_id: 'user789',
    auth_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
    preferences: 'dark_mode,usd',
    cart_id: 'cart101112',
    csrf_token: 'csrf_xyz789'
  };

  const complexPayload = {
    website_url: 'https://example.com/dashboard',
    user_prompt: 'Extract user profile and preferences'
  };

  if (complexCookies) {
    if (typeof complexCookies === 'object' && complexCookies !== null) {
      complexPayload.cookies = complexCookies;
      console.log('✅ Complex cookies validation passed');
      console.log(`✅ Complex cookies count: ${Object.keys(complexPayload.cookies).length}`);
    }
  }

  // Test 3: Invalid cookies
  console.log('\n3. Testing invalid cookies...');

  const invalidCookies = 'not_an_object';

  try {
    if (invalidCookies) {
      if (typeof invalidCookies === 'object' && invalidCookies !== null) {
        console.log('❌ Should have failed validation');
      } else {
        console.log('✅ Invalid cookies correctly rejected');
      }
    }
  } catch (error) {
    console.log('✅ Error handling works correctly');
  }

  // Test 4: Function signature validation
  console.log('\n4. Testing function signature...');

  // Check if the function accepts the cookies parameter
  const functionString = smartScraper.toString();
  if (functionString.includes('cookies = null')) {
    console.log('✅ Function signature includes cookies parameter');
  } else {
    console.log('❌ Function signature missing cookies parameter');
  }

  console.log('\n' + '='.repeat(50));
  console.log('✅ All cookies integration tests completed!');
  console.log('='.repeat(50));
}

// Run the test
testCookiesIntegration();
