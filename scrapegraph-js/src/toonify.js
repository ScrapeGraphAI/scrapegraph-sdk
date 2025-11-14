import axios from 'axios';
import handleError from './utils/handleError.js';
import { isMockEnabled, getMockConfig } from './utils/mockConfig.js';
import { getMockResponse } from './utils/mockResponse.js';

/**
 * Converts data to toon format.
 *
 * @param {string} apiKey - Your ScrapeGraph AI API key.
 * @param {Object} data - The data object to be converted to toon format.
 * @param {Object} options - Optional configuration options.
 * @param {boolean} options.mock - Override mock mode for this request
 * @returns {Promise<Object>} A promise that resolves to the toonified data response.
 * @throws {Error} Throws an error if the HTTP request fails.
 *
 * @example
 * // Example usage:
 * const apiKey = 'your-api-key';
 * const data = {
 *   products: [
 *     { sku: "LAP-001", name: "Gaming Laptop", price: 1299.99 },
 *     { sku: "MOU-042", name: "Wireless Mouse", price: 29.99 }
 *   ]
 * };
 *
 * try {
 *   const result = await toonify(apiKey, data);
 *   console.log('Toonified result:', result);
 * } catch (error) {
 *   console.error('Error toonifying data:', error);
 * }
 */
export async function toonify(apiKey, data, options = {}) {
  const { mock = null } = options;

  // Check if mock mode is enabled
  const useMock = mock !== null ? mock : isMockEnabled();

  if (useMock) {
    console.log('🧪 Mock mode active. Returning stub for toonify request');
    const mockConfig = getMockConfig();
    const mockData = getMockResponse('POST', 'https://api.scrapegraphai.com/v1/toonify', mockConfig.customResponses, mockConfig.customHandler);
    return mockData;
  }

  const endpoint = 'https://api.scrapegraphai.com/v1/toonify';
  const headers = {
    'accept': 'application/json',
    'SGAI-APIKEY': apiKey,
    'Content-Type': 'application/json',
  };

  try {
    const response = await axios.post(endpoint, data, { headers });
    return response.data;
  } catch (error) {
    handleError(error);
  }
}
