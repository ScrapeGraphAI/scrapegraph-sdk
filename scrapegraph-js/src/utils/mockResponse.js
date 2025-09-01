/**
 * Mock response utility for ScrapeGraph AI SDK
 * Provides deterministic mock responses when mock mode is enabled
 */

/**
 * Generate a mock UUID with a prefix
 * @param {string} prefix - Prefix for the mock ID
 * @returns {string} Mock UUID
 */
function generateMockId(prefix = 'mock') {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 8);
  return `${prefix}-${timestamp}-${random}`;
}

/**
 * Get mock response based on endpoint and method
 * @param {string} method - HTTP method (GET, POST, etc.)
 * @param {string} url - Full URL
 * @param {Object} customResponses - Custom response overrides
 * @param {Function} customHandler - Custom handler function
 * @returns {Object} Mock response data
 */
export function getMockResponse(method, url, customResponses = {}, customHandler = null) {
  // Custom handler takes precedence
  if (customHandler && typeof customHandler === 'function') {
    try {
      return customHandler(method, url);
    } catch (error) {
      console.warn('Custom mock handler failed, falling back to defaults:', error.message);
    }
  }

  // Parse URL to get path
  const urlObj = new URL(url);
  const path = urlObj.pathname;

  // Check for custom response override
  if (customResponses[path]) {
    const override = customResponses[path];
    return typeof override === 'function' ? override() : override;
  }

  const upperMethod = method.toUpperCase();

  // Credits endpoint
  if (path.endsWith('/credits') && upperMethod === 'GET') {
    return {
      remaining_credits: 1000,
      total_credits_used: 0
    };
  }

  // Feedback endpoint
  if (path.endsWith('/feedback') && upperMethod === 'POST') {
    return {
      status: 'success'
    };
  }

  // Create-like endpoints (POST)
  if (upperMethod === 'POST') {
    if (path.endsWith('/crawl')) {
      return {
        crawl_id: generateMockId('mock-crawl')
      };
    }
    // All other POST endpoints return a request id
    return {
      request_id: generateMockId('mock-req')
    };
  }

  // Status-like endpoints (GET)
  if (upperMethod === 'GET') {
    if (path.includes('markdownify')) {
      return {
        status: 'completed',
        content: '# Mock markdown\n\nThis is a mock markdown response...'
      };
    }
    if (path.includes('smartscraper')) {
      return {
        status: 'completed',
        result: [{ field: 'value', title: 'Mock Title' }]
      };
    }
    if (path.includes('searchscraper')) {
      return {
        status: 'completed',
        results: [{ url: 'https://example.com', title: 'Mock Result' }]
      };
    }
    if (path.includes('crawl')) {
      return {
        status: 'completed',
        pages: []
      };
    }
    if (path.includes('agentic-scrapper')) {
      return {
        status: 'completed',
        actions: []
      };
    }
    if (path.includes('scrape')) {
      return {
        status: 'completed',
        html: '<!DOCTYPE html><html><head><title>Mock HTML</title></head><body><h1>Mock Content</h1></body></html>'
      };
    }
  }

  // Generic fallback
  return {
    status: 'mock',
    url: url,
    method: method,
    message: 'Mock response generated'
  };
}

/**
 * Create a mock axios response object
 * @param {Object} data - Response data
 * @returns {Object} Mock axios response
 */
export function createMockAxiosResponse(data) {
  return {
    data,
    status: 200,
    statusText: 'OK',
    headers: {
      'content-type': 'application/json'
    },
    config: {
      url: 'mock-url',
      method: 'mock'
    }
  };
}
