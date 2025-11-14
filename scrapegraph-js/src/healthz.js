import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Check the health status of the ScrapeGraphAI API service.
 * 
 * This endpoint is useful for monitoring and ensuring the service is operational.
 * It returns a JSON response indicating the service's health status.
 * 
 * Use cases:
 * - Production monitoring and alerting
 * - Health checks in containerized environments (Kubernetes, Docker)
 * - Ensuring service availability before making API calls
 * - Integration with monitoring tools (Prometheus, Datadog, etc.)
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @param {Object} options - Optional configuration
 * @param {boolean} options.mock - Whether to use mock mode for this request
 * @returns {Promise<Object>} Health status response with status and message
 * 
 * @example
 * import { healthz } from 'scrapegraph-sdk';
 * 
 * const health = await healthz('your-api-key');
 * console.log(health);
 * // { status: 'healthy', message: 'Service is operational' }
 */
export async function healthz(apiKey, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for healthz');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', 'https://api.scrapegraphai.com/v1/healthz', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/healthz';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
  };

  try {
    const response = await axios.get(endpoint, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}

