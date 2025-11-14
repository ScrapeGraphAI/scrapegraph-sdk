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

  // Health check endpoint
  if (path.endsWith('/healthz') && upperMethod === 'GET') {
    return {
      status: 'healthy',
      message: 'Service is operational'
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
    if (path.endsWith('/scheduled-jobs')) {
      return {
        id: generateMockId('mock-job'),
        user_id: generateMockId('mock-user'),
        job_name: 'Mock Scheduled Job',
        service_type: 'smartscraper',
        cron_expression: '0 9 * * 1',
        job_config: { mock: 'config' },
        is_active: true,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
        next_run_at: '2024-01-08T09:00:00Z'
      };
    }
    if (path.includes('/pause')) {
      return {
        message: 'Job paused successfully',
        job_id: generateMockId('mock-job'),
        is_active: false
      };
    }
    if (path.includes('/resume')) {
      return {
        message: 'Job resumed successfully',
        job_id: generateMockId('mock-job'),
        is_active: true,
        next_run_at: '2024-01-08T09:00:00Z'
      };
    }
    if (path.includes('/trigger')) {
      const taskId = generateMockId('mock-task');
      return {
        execution_id: taskId,
        scheduled_job_id: generateMockId('mock-job'),
        triggered_at: '2024-01-01T00:00:00Z',
        message: `Job triggered successfully. Task ID: ${taskId}`
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
    if (path.includes('scheduled-jobs')) {
      if (path.includes('/executions')) {
        return {
          executions: [
            {
              id: generateMockId('mock-exec'),
              scheduled_job_id: generateMockId('mock-job'),
              execution_id: generateMockId('mock-task'),
              status: 'completed',
              started_at: '2024-01-01T00:00:00Z',
              completed_at: '2024-01-01T00:01:00Z',
              result: { mock: 'result' },
              credits_used: 10
            }
          ],
          total: 1,
          page: 1,
          page_size: 20
        };
      } else if (path.endsWith('/scheduled-jobs')) {
        // List jobs endpoint
        return {
          jobs: [
            {
              id: generateMockId('mock-job'),
              user_id: generateMockId('mock-user'),
              job_name: 'Mock Scheduled Job',
              service_type: 'smartscraper',
              cron_expression: '0 9 * * 1',
              job_config: { mock: 'config' },
              is_active: true,
              created_at: '2024-01-01T00:00:00Z',
              updated_at: '2024-01-01T00:00:00Z',
              next_run_at: '2024-01-08T09:00:00Z'
            }
          ],
          total: 1,
          page: 1,
          page_size: 20
        };
      } else {
        // Single job endpoint
        return {
          id: generateMockId('mock-job'),
          user_id: generateMockId('mock-user'),
          job_name: 'Mock Scheduled Job',
          service_type: 'smartscraper',
          cron_expression: '0 9 * * 1',
          job_config: { mock: 'config' },
          is_active: true,
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
          next_run_at: '2024-01-08T09:00:00Z'
        };
      }
    }
  }

  // Update operations (PATCH/PUT)
  if (upperMethod === 'PATCH' || upperMethod === 'PUT') {
    if (path.includes('scheduled-jobs')) {
      return {
        id: generateMockId('mock-job'),
        user_id: generateMockId('mock-user'),
        job_name: 'Updated Mock Scheduled Job',
        service_type: 'smartscraper',
        cron_expression: '0 10 * * 1',
        job_config: { mock: 'updated_config' },
        is_active: true,
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T01:00:00Z',
        next_run_at: '2024-01-08T10:00:00Z'
      };
    }
  }

  // Delete operations
  if (upperMethod === 'DELETE') {
    if (path.includes('scheduled-jobs')) {
      return {
        message: 'Scheduled job deleted successfully'
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
