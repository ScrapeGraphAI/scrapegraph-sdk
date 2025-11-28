import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse, createMockAxiosResponse } from './utils/mockResponse.js';

/**
 * Retrieve credits from the API.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key
 * @returns {Promise<string>} Response from the API in JSON format
 */
export async function getCredits(apiKey, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();
  
  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for getCredits');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('GET', 'https://api.scrapegraphai.com/v1/credits', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/credits';
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
